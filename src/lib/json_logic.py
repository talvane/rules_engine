import sys
from functools import reduce


def jsonLogic(tests, data=None, functions=None):
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
    # Inicializa o registro de funções  como um dicionário vazio se não for fornecido
    functions = functions if functions is not None else {}

    try:
        op = next(iter(tests))
        values = tests[op]
    except StopIteration:
        return None 
    
    
    def _less_than(*v):
        """
        Verifica se todos os valores em v estão em ordem crescente.
        Retorna False se os tipos não forem comparáveis.
        """
        try:
            return len(v) >= 2 and all(v[i] < v[i+1] for i in range(len(v)-1))
        except TypeError:
            return False

    
    def _less_than_or_equal(*v):
        """
        Verifica se todos os valores em v estão em ordem crescente ou igual.
        Retorna False se os tipos não forem comparáveis.
        """
        try:
            return len(v) >= 2 and all(v[i] <= v[i+1] for i in range(len(v)-1))
        except TypeError:
            return False


    def _apply_function(*args):
        """
        Executa uma função registrada.
        O primeiro argumento é o nome da função, e o restante são seus parâmetros.
        """
        if not args:
            raise ValueError("A operação 'apply' requer pelo menos um argumento (o nome da função).")
        
        func_name = args[0]
        if func_name not in functions:
            raise NameError(f"Função pura não registrada ou não permitida: '{func_name}'")
        
        # Obtém a função do registro e a chama com os argumentos restantes
        func = functions[func_name]
        return func(*args[1:])

    # Define as operações suportadas
    operations = {
        "==":   lambda a, b: a == b,
        "===":  lambda a, b: a is b,
        "!=":   lambda a, b: a != b,
        "!==":  lambda a, b: a is not b,
        ">":    lambda a, b: a > b,
        ">=":   lambda a, b: a >= b,
        "<":    _less_than,
        "<=":   _less_than_or_equal,
        "!":    lambda a: not a,
        "%":    lambda a, b: a % b,
        "and":  lambda *args: all(args),
        "or":   lambda *args: any(args),
        "?:":   lambda a, b, c: b if a else c,
        "log":  lambda a: print(a, file=sys.stdout) or a,
        "in":   lambda a, b: (a in b) if isinstance(b, (list, tuple, dict, str)) else False,
        "var":  lambda a, not_found=None:
        reduce(
            lambda d, key: (
            d.get(str(key), not_found) if isinstance(d, dict)
            else d[int(key)] if isinstance(d, (list, tuple)) and str(key).lstrip("-").isdigit() and int(key) < len(d)
            else not_found
            ),
            str(a).split("."),
            data
        ),
        "cat":  lambda *args: "".join(map(str, args)),
        "+":    lambda *args: sum(map(float, args)),
        "*":    lambda *args: reduce(lambda total, arg: total * float(arg), args, 1.0),
        "-":    lambda a, b=None: -a if b is None else a - b,
        "/":    lambda a, b=None: a if b is None else float(a) / float(b),
        "min":  lambda *args: min(args),
        "max":  lambda *args: max(args),
        "count": lambda *args: sum(1 for a in args if a),
        "apply": _apply_function,
    }
    
    # "if" é um alias comum para o operador ternário "?:"
    operations["if"] = operations["?:"]

    if op not in operations:
        raise RuntimeError(f"Operação não reconhecida: {op}")

    if not isinstance(values, (list, tuple)):
        values = [values]
    
    # Passa o registro 'functions' para as chamadas recursivas
    processed_values = map(lambda val: jsonLogic(val, data, functions), values)    

    return operations[op](*processed_values)
