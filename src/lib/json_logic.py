import sys
import inspect
from functools import reduce
from typing import Any, Dict, Union, Optional, Callable, Awaitable


def _get_nested_value(path: str, data: Dict[str, Any], not_found: Any = None) -> Any:
    """
    Navega através de estruturas de dados aninhadas usando notação de ponto.

    Args:
        path: Caminho usando notação de ponto (ex: "usuario.nome")
        data: Dados para navegar
        not_found: Valor retornado quando o caminho não é encontrado

    Returns:
        Valor encontrado ou not_found
    """

    def _navigate(current_data: Any, key: str) -> Any:
        if isinstance(current_data, dict):
            return current_data.get(str(key), not_found)
        elif isinstance(current_data, (list, tuple)):
            if str(key).lstrip("-").isdigit() and int(key) < len(current_data):
                return current_data[int(key)]
        return not_found

    return reduce(_navigate, str(path).split("."), data)


def _parse_operation(tests: Dict[str, Any]) -> tuple:
    """
    Extrai a operação e seus valores de um teste JSON Logic.

    Args:
        tests: Dicionário contendo a operação e valores

    Returns:
        Tupla com (operação, valores)
    """
    try:
        op = next(iter(tests))
        values = tests[op]
        return op, values
    except StopIteration:
        return None, None


def _execute_operation(
    op: str,
    values: Any,
    data: Dict[str, Any],
    functions: Dict[str, Callable],
    operations: Dict[str, Callable],
) -> Any:
    """
    Executa uma operação específica com os valores fornecidos.

    Args:
        op: Nome da operação
        values: Valores para a operação
        data: Dados de contexto
        functions: Funções registradas
        operations: Dicionário de operações disponíveis

    Returns:
        Resultado da operação
    """
    if op not in operations:
        raise RuntimeError(f"Operação não reconhecida: {op}")

    if not isinstance(values, (list, tuple)):
        values = [values]

    # Processa valores recursivamente
    processed_values = map(lambda val: jsonLogic(val, data, functions), values)

    return operations[op](*processed_values)


async def _execute_operation_async(
    op: str,
    values: Any,
    data: Dict[str, Any],
    functions: Dict[str, Callable],
    operations: Dict[str, Callable],
) -> Any:
    """
    Versão assíncrona de _execute_operation.
    Executa uma operação específica com os valores fornecidos de forma assíncrona.

    Args:
        op: Nome da operação
        values: Valores para a operação
        data: Dados de contexto
        functions: Funções registradas
        operations: Dicionário de operações disponíveis

    Returns:
        Resultado da operação
    """
    if op not in operations:
        raise RuntimeError(f"Operação não reconhecida: {op}")

    if not isinstance(values, (list, tuple)):
        values = [values]

    # Processa valores recursivamente de forma assíncrona
    processed_values = []
    for val in values:
        result = await jsonLogicAsync(val, data, functions)
        processed_values.append(result)

    # Verifica se a operação é assíncrona
    operation_func = operations[op]
    if inspect.iscoroutinefunction(operation_func):
        return await operation_func(*processed_values)
    else:
        return operation_func(*processed_values)


def jsonLogic(
    tests: Any,
    data: Optional[Dict[str, Any]] = None,
    functions: Optional[Dict[str, Callable]] = None,
) -> Any:
    """
    Executa a lógica definida em uma estrutura de testes (JSON/dict)
    sobre um conjunto de dados, com suporte a chamadas de funções .

    Exemplo de uso:
    ```python
    # 1. Defina suas funções em Python
    def formatar_nome_completo(primeiro, ultimo):
        return f"{ultimo.upper()}, {primeiro.capitalize()}"

    def calcular_area(largura, altura):
        return largura * altura

    # 2. Crie o registro de funções permitidas
    funcoes_permitidas = {
        "format_name": formatar_nome_completo,
        "get_area": calcular_area,
    }

    # 3. Defina os dados e as regras lógicas
    dados = {
        "usuario": {
            "nome": "joão",
            "sobrenome": "silva"
        },
        "retangulo": {
            "l": 10,
            "a": 5
        }
    }

    # Regra para formatar o nome usando a função pura
    regra_nome = {
        "apply": [
            "format_name",
            {"var": "usuario.nome"},
            {"var": "usuario.sobrenome"}
        ]
    }

    # Regra para verificar se a área é maior que 40
    regra_area = {
        ">": [
            {
                "apply": [
                    "get_area",
                    {"var": "retangulo.l"},
                    {"var": "retangulo.a"}
                ]
            },
            40
        ]
    }

    # 4. Execute o jsonLogic passando os dados e as funções
    nome_formatado = jsonLogic(regra_nome, dados, funcoes_permitidas)
    area_e_grande = jsonLogic(regra_area, dados, funcoes_permitidas)

    print(f"Nome formatado: {nome_formatado}")
    print(f"A área é maior que 40? {area_e_grande}")

    # --- Saída Esperada ---
    # Nome formatado: SILVA, João
    # A área é maior que 40? True
    """

    if not isinstance(tests, dict):
        return tests

    data = data if data is not None else {}
    functions = functions if functions is not None else {}

    # Extrai operação e valores
    op, values = _parse_operation(tests)
    if op is None:
        return tests

    def _less_than(*v):
        """
        Verifica se todos os valores em v estão em ordem crescente.
        Retorna False se os tipos não forem comparáveis.
        """
        try:
            return len(v) >= 2 and all(v[i] < v[i + 1] for i in range(len(v) - 1))
        except TypeError:
            return False

    def _less_than_or_equal(*v):
        """
        Verifica se todos os valores em v estão em ordem crescente ou igual.
        Retorna False se os tipos não forem comparáveis.
        """
        try:
            return len(v) >= 2 and all(v[i] <= v[i + 1] for i in range(len(v) - 1))
        except TypeError:
            return False

    def _apply_function(*args):
        """
        Executa uma função registrada.
        O primeiro argumento é o nome da função, e o restante são seus parâmetros.
        """
        if not args:
            raise ValueError(
                "A operação 'apply' requer pelo menos um argumento (o nome da função)."
            )

        func_name = args[0]
        if func_name not in functions:
            raise NameError(
                f"Função pura não registrada ou não permitida: '{func_name}'"
            )

        # Obtém a função do registro e a chama com os argumentos restantes
        func = functions[func_name]
        return func(*args[1:])

    async def _apply_function_async(*args):
        """
        Versão assíncrona de _apply_function.
        Executa uma função registrada de forma assíncrona.
        O primeiro argumento é o nome da função, e o restante são seus parâmetros.
        """
        if not args:
            raise ValueError(
                "A operação 'apply' requer pelo menos um argumento (o nome da função)."
            )

        func_name = args[0]
        if func_name not in functions:
            raise NameError(
                f"Função pura não registrada ou não permitida: '{func_name}'"
            )

        # Obtém a função do registro
        func = functions[func_name]
        
        # Verifica se é uma função assíncrona
        if inspect.iscoroutinefunction(func):
            return await func(*args[1:])
        else:
            return func(*args[1:])

    # Define as operações suportadas organizadas por categoria

    # Operações de comparação
    comparison_ops = {
        "==": lambda a, b: a == b,
        "===": lambda a, b: a is b,
        "!=": lambda a, b: a != b,
        "!==": lambda a, b: a is not b,
        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
        "<": _less_than,
        "<=": _less_than_or_equal,
    }

    # Operações lógicas
    logical_ops = {
        "!": lambda a: not a,
        "and": lambda *args: all(args),
        "or": lambda *args: any(args),
        "?:": lambda a, b, c: b if a else c,
    }

    # Operações matemáticas
    math_ops = {
        "+": lambda *args: sum(map(float, args)),
        "-": lambda a, b=None: -a if b is None else a - b,
        "*": lambda *args: reduce(lambda total, arg: total * float(arg), args, 1.0),
        "/": lambda a, b=None: a if b is None else float(a) / float(b),
        "%": lambda a, b: a % b,
        "min": lambda *args: min(args),
        "max": lambda *args: max(args),
    }

    # Operações de manipulação de dados
    data_ops = {
        "var": lambda a, not_found=None: _get_nested_value(a, data, not_found),
        "in": lambda a, b: (
            (a in b) if isinstance(b, (list, tuple, dict, str)) else False
        ),
        "count": lambda *args: sum(1 for a in args if a),
        "some": lambda array, logic: any(jsonLogic(logic, item, functions) for item in (array if isinstance(array, (list, tuple)) else [])),
        "every": lambda array, logic: all(jsonLogic(logic, item, functions) for item in (array if isinstance(array, (list, tuple)) else [])),
        "none": lambda array, logic: not any(jsonLogic(logic, item, functions) for item in (array if isinstance(array, (list, tuple)) else [])),
        "merge": lambda *arrays: [item for array in arrays if isinstance(array, (list, tuple)) for item in array],
        "map": lambda array, logic: [jsonLogic(logic, item, functions) for item in (array if isinstance(array, (list, tuple)) else [])],
        "filter": lambda array, logic: [item for item in (array if isinstance(array, (list, tuple)) else []) if jsonLogic(logic, item, functions)],
        "reduce": lambda array, logic, initial=0: reduce(lambda acc, curr: jsonLogic(logic, {"current": curr, "accumulator": acc}, functions), array if isinstance(array, (list, tuple)) else [], initial),
    }

    # Operações de string
    string_ops = {
        "cat": lambda *args: "".join(map(str, args)),
    }

    # Operações de sistema
    system_ops = {
        "log": lambda a: print(a, file=sys.stdout) or a,
        "apply": _apply_function,
    }

    # Combina todas as operações
    operations = {
        **comparison_ops,
        **logical_ops,
        **math_ops,
        **data_ops,
        **string_ops,
        **system_ops,
    }

    # "if" é um alias comum para o operador ternário "?:"
    operations["if"] = operations["?:"]

    # Executa a operação
    return _execute_operation(op, values, data, functions, operations)


async def jsonLogicAsync(
    tests: Any,
    data: Optional[Dict[str, Any]] = None,
    functions: Optional[Dict[str, Callable]] = None,
) -> Any:
    """
    Versão assíncrona de jsonLogic.
    Executa a lógica definida em uma estrutura de testes (JSON/dict)
    sobre um conjunto de dados, com suporte a chamadas de funções assíncronas.

    Exemplo de uso:
    ```python
    import asyncio
    
    # 1. Defina suas funções em Python (síncronas e assíncronas)
    def formatar_nome_completo(primeiro, ultimo):
        return f"{ultimo.upper()}, {primeiro.capitalize()}"

    async def buscar_dados_usuario(user_id):
        # Simula uma chamada de API assíncrona
        await asyncio.sleep(0.1)
        return {"nome": "joão", "sobrenome": "silva", "idade": 30}

    async def calcular_area_async(largura, altura):
        # Simula um cálculo assíncrono
        await asyncio.sleep(0.05)
        return largura * altura

    # 2. Crie o registro de funções permitidas (síncronas e assíncronas)
    funcoes_permitidas = {
        "format_name": formatar_nome_completo,
        "fetch_user": buscar_dados_usuario,
        "get_area_async": calcular_area_async,
    }

    # 3. Defina os dados e as regras lógicas
    dados = {
        "usuario_id": 123,
        "retangulo": {
            "l": 10,
            "a": 5
        }
    }

    # Regra para buscar dados do usuário e formatar o nome
    regra_usuario = {
        "apply": [
            "format_name",
            {"var": "dados_usuario.nome"},
            {"var": "dados_usuario.sobrenome"}
        ]
    }

    # Regra para verificar se a área calculada assincronamente é maior que 40
    regra_area = {
        ">": [
            {
                "apply": [
                    "get_area_async",
                    {"var": "retangulo.l"},
                    {"var": "retangulo.a"}
                ]
            },
            40
        ]
    }

    # 4. Execute o jsonLogicAsync passando os dados e as funções
    async def main():
        # Primeiro busca os dados do usuário
        dados_usuario = await jsonLogicAsync(
            {"apply": ["fetch_user", {"var": "usuario_id"}]}, 
            dados, 
            funcoes_permitidas
        )
        
        # Adiciona os dados do usuário ao contexto
        dados_completos = {**dados, "dados_usuario": dados_usuario}
        
        # Executa as regras
        nome_formatado = await jsonLogicAsync(regra_usuario, dados_completos, funcoes_permitidas)
        area_e_grande = await jsonLogicAsync(regra_area, dados, funcoes_permitidas)
        
        print(f"Nome formatado: {nome_formatado}")
        print(f"A área é maior que 40? {area_e_grande}")

    # Para executar: asyncio.run(main())
    ```
    """

    if not isinstance(tests, dict):
        return tests

    data = data if data is not None else {}
    functions = functions if functions is not None else {}

    # Extrai operação e valores
    op, values = _parse_operation(tests)
    if op is None:
        return tests

    def _less_than(*v):
        """
        Verifica se todos os valores em v estão em ordem crescente.
        Retorna False se os tipos não forem comparáveis.
        """
        try:
            return len(v) >= 2 and all(v[i] < v[i + 1] for i in range(len(v) - 1))
        except TypeError:
            return False

    def _less_than_or_equal(*v):
        """
        Verifica se todos os valores em v estão em ordem crescente ou igual.
        Retorna False se os tipos não forem comparáveis.
        """
        try:
            return len(v) >= 2 and all(v[i] <= v[i + 1] for i in range(len(v) - 1))
        except TypeError:
            return False

    async def _apply_function_async(*args):
        """
        Versão assíncrona de _apply_function.
        Executa uma função registrada de forma assíncrona.
        O primeiro argumento é o nome da função, e o restante são seus parâmetros.
        """
        if not args:
            raise ValueError(
                "A operação 'apply' requer pelo menos um argumento (o nome da função)."
            )

        func_name = args[0]
        if func_name not in functions:
            raise NameError(
                f"Função pura não registrada ou não permitida: '{func_name}'"
            )

        # Obtém a função do registro
        func = functions[func_name]
        
        # Verifica se é uma função assíncrona
        if inspect.iscoroutinefunction(func):
            return await func(*args[1:])
        else:
            return func(*args[1:])

    # Define as operações suportadas organizadas por categoria

    # Operações de comparação
    comparison_ops = {
        "==": lambda a, b: a == b,
        "===": lambda a, b: a is b,
        "!=": lambda a, b: a != b,
        "!==": lambda a, b: a is not b,
        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
        "<": _less_than,
        "<=": _less_than_or_equal,
    }

    # Operações lógicas
    logical_ops = {
        "!": lambda a: not a,
        "and": lambda *args: all(args),
        "or": lambda *args: any(args),
        "?:": lambda a, b, c: b if a else c,
    }

    # Operações matemáticas
    math_ops = {
        "+": lambda *args: sum(map(float, args)),
        "-": lambda a, b=None: -a if b is None else a - b,
        "*": lambda *args: reduce(lambda total, arg: total * float(arg), args, 1.0),
        "/": lambda a, b=None: a if b is None else float(a) / float(b),
        "%": lambda a, b: a % b,
        "min": lambda *args: min(args),
        "max": lambda *args: max(args),
    }

    # Operações de manipulação de dados
    data_ops = {
        "var": lambda a, not_found=None: _get_nested_value(a, data, not_found),
        "in": lambda a, b: (
            (a in b) if isinstance(b, (list, tuple, dict, str)) else False
        ),
        "count": lambda *args: sum(1 for a in args if a),
        "some": lambda array, logic: any(jsonLogicAsync(logic, item, functions) for item in (array if isinstance(array, (list, tuple)) else [])),
        "every": lambda array, logic: all(jsonLogicAsync(logic, item, functions) for item in (array if isinstance(array, (list, tuple)) else [])),
        "none": lambda array, logic: not any(jsonLogicAsync(logic, item, functions) for item in (array if isinstance(array, (list, tuple)) else [])),
        "merge": lambda *arrays: [item for array in arrays if isinstance(array, (list, tuple)) for item in array],
        "map": lambda array, logic: [jsonLogicAsync(logic, item, functions) for item in (array if isinstance(array, (list, tuple)) else [])],
        "filter": lambda array, logic: [item for item in (array if isinstance(array, (list, tuple)) else []) if jsonLogicAsync(logic, item, functions)],
        "reduce": lambda array, logic, initial=0: reduce(lambda acc, curr: jsonLogicAsync(logic, {"current": curr, "accumulator": acc}, functions), array if isinstance(array, (list, tuple)) else [], initial),
    }

    # Operações de string
    string_ops = {
        "cat": lambda *args: "".join(map(str, args)),
    }

    # Operações de sistema
    system_ops = {
        "log": lambda a: print(a, file=sys.stdout) or a,
        "apply": _apply_function_async,  # Usa a versão assíncrona
    }

    # Combina todas as operações
    operations = {
        **comparison_ops,
        **logical_ops,
        **math_ops,
        **data_ops,
        **string_ops,
        **system_ops,
    }

    # "if" é um alias comum para o operador ternário "?:"
    operations["if"] = operations["?:"]

    # Executa a operação de forma assíncrona
    return await _execute_operation_async(op, values, data, functions, operations)


def has_async_functions(functions: Dict[str, Callable]) -> bool:
    """
    Verifica se alguma das funções registradas é assíncrona.
    
    Args:
        functions: Dicionário de funções registradas
        
    Returns:
        True se pelo menos uma função for assíncrona, False caso contrário
    """
    return any(inspect.iscoroutinefunction(func) for func in functions.values())


def jsonLogicAuto(
    tests: Any,
    data: Optional[Dict[str, Any]] = None,
    functions: Optional[Dict[str, Callable]] = None,
) -> Union[Any, Awaitable[Any]]:
    """
    Detecta automaticamente se deve usar jsonLogic ou jsonLogicAsync
    baseado na presença de funções assíncronas.
    
    Args:
        tests: Estrutura de testes JSON Logic
        data: Dados de contexto
        functions: Funções registradas (síncronas e/ou assíncronas)
        
    Returns:
        Resultado da execução ou corrotina se houver funções assíncronas
        
    Exemplo de uso:
    ```python
    import asyncio
    
    # Funções mistas
    def sync_func(x):
        return x * 2
        
    async def async_func(x):
        await asyncio.sleep(0.1)
        return x * 3
    
    functions = {"sync": sync_func, "async": async_func}
    
    # Auto-detecta e usa a versão correta
    result = jsonLogicAuto({"apply": ["sync", 5]}, {}, functions)
    # Como só usa funções síncronas, retorna 10 diretamente
    
    result_async = jsonLogicAuto({"apply": ["async", 5]}, {}, functions) 
    # Como usa função assíncrona, retorna uma corrotina
    # Para obter o resultado: await result_async ou asyncio.run(result_async)
    ```
    """
    functions = functions if functions is not None else {}
    
    # Verifica se há funções assíncronas registradas
    if has_async_functions(functions):
        return jsonLogicAsync(tests, data, functions)
    else:
        return jsonLogic(tests, data, functions)
