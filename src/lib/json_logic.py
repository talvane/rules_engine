import sys
from functools import reduce
from typing import Any, Dict, List, Union, Optional, Callable


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
        return None

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
