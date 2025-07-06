import pytest
from unittest.mock import patch
from src.lib.json_logic import jsonLogic


class TestJsonLogic:
    """Testes unitários para a função jsonLogic"""

    def test_basic_comparison_operations(self):
        """Testa operações básicas de comparação"""
        # Igualdade
        assert jsonLogic({"==": [1, 1]})
        assert not jsonLogic({"==": [1, 2]})

        # Identidade
        assert jsonLogic({"===": [1, 1]})
        assert jsonLogic({"===": ["hello", "hello"]})

        # Diferença
        assert jsonLogic({"!=": [1, 2]})
        assert not jsonLogic({"!=": [1, 1]})

        # Não identidade
        assert jsonLogic({"!==": [1, 2]})
        assert not jsonLogic({"!==": [1, 1]})

        # Maior que
        assert jsonLogic({">": [2, 1]})
        assert not jsonLogic({">": [1, 2]})

        # Maior ou igual
        assert jsonLogic({">=": [2, 1]})
        assert jsonLogic({">=": [1, 1]})
        assert not jsonLogic({">=": [1, 2]})

    def test_less_than_operations(self):
        """Testa operações de menor que"""
        # Menor que - dois valores
        assert jsonLogic({"<": [1, 2]})
        assert not jsonLogic({"<": [2, 1]})
        assert not jsonLogic({"<": [1, 1]})

        # Menor que - múltiplos valores (ordem crescente)
        assert jsonLogic({"<": [1, 2, 3, 4]})
        assert not jsonLogic({"<": [1, 3, 2, 4]})

        # Menor que - tipos incomparáveis
        assert not jsonLogic({"<": ["string", 1]})

        assert not jsonLogic({"<": [None, 1]})

    def test_less_than_or_equal_operations(self):
        """Testa operações de menor ou igual"""
        # Menor ou igual - dois valores
        assert jsonLogic({"<=": [1, 2]})
        assert jsonLogic({"<=": [1, 1]})
        assert not jsonLogic({"<=": [2, 1]})

        # Menor ou igual - múltiplos valores
        assert jsonLogic({"<=": [1, 2, 2, 3]})
        assert not jsonLogic({"<=": [1, 3, 2, 4]})

        # Menor ou igual - tipos incomparáveis
        assert not jsonLogic({"<=": ["string", 1]})

    def test_logical_operations(self):
        """Testa operações lógicas"""
        # Negação

        assert not jsonLogic({"!": [True]})
        assert jsonLogic({"!": [False]})
        assert jsonLogic({"!": [0]})
        assert not jsonLogic({"!": [1]})

        # And
        assert jsonLogic({"and": [True, True]})
        assert not jsonLogic({"and": [True, False]})
        assert jsonLogic({"and": [True, True, True]})
        assert not jsonLogic({"and": [True, True, False]})

        # Or
        assert not jsonLogic({"or": [False, False]})
        assert jsonLogic({"or": [True, False]})
        assert jsonLogic({"or": [False, False, True]})
        assert not jsonLogic({"or": [False, False, False]})

    def test_ternary_operator(self):
        """Testa operador ternário"""
        # Operador ternário básico
        assert jsonLogic({"?:": [True, "yes", "no"]}) == "yes"
        assert jsonLogic({"?:": [False, "yes", "no"]}) == "no"

        # Alias "if"
        assert jsonLogic({"if": [True, "yes", "no"]}) == "yes"
        assert jsonLogic({"if": [False, "yes", "no"]}) == "no"

    def test_arithmetic_operations(self):
        """Testa operações aritméticas"""
        # Soma
        assert jsonLogic({"+": [1, 2, 3]}) == 6.0
        assert jsonLogic({"+": [1.5, 2.5]}) == 4.0

        # Multiplicação
        assert jsonLogic({"*": [2, 3, 4]}) == 24.0
        assert jsonLogic({"*": [1.5, 2]}) == 3.0

        # Subtração
        assert jsonLogic({"-": [5, 3]}) == 2
        assert jsonLogic({"-": [5]}) == -5  # Negação unária

        # Divisão
        assert jsonLogic({"/": [10, 2]}) == 5.0
        assert jsonLogic({"/": [10]}) == 10  # Identidade

        # Módulo
        assert jsonLogic({"%": [10, 3]}) == 1
        assert jsonLogic({"%": [8, 4]}) == 0

    def test_string_operations(self):
        """Testa operações com strings"""
        # Concatenação
        assert jsonLogic({"cat": ["Hello", " ", "World"]}) == "Hello World"
        assert jsonLogic({"cat": ["A", 1, "B"]}) == "A1B"

        # In - string
        assert jsonLogic({"in": ["ell", "Hello"]})
        assert not jsonLogic({"in": ["xyz", "Hello"]})

    def test_array_operations(self):
        """Testa operações com arrays"""
        # In - array
        assert jsonLogic({"in": [1, [1, 2, 3]]})
        assert not jsonLogic({"in": [4, [1, 2, 3]]})

        # Min/Max
        assert jsonLogic({"min": [1, 5, 3, 2]}) == 1
        assert jsonLogic({"max": [1, 5, 3, 2]}) == 5

        # Count
        assert jsonLogic({"count": [True, False, True, 1, 0]}) == 3
        assert jsonLogic({"count": [False, 0, None, ""]}) == 0

    def test_variable_access(self):
        """Testa acesso a variáveis"""
        data = {
            "name": "João",
            "age": 30,
            "address": {"street": "Rua das Flores", "number": 123},
            "hobbies": ["leitura", "cinema", "culinária"],
        }

        # Acesso básico
        assert jsonLogic({"var": "name"}, data) == "João"
        assert jsonLogic({"var": "age"}, data) == 30

        # Acesso aninhado
        assert jsonLogic({"var": "address.street"}, data) == "Rua das Flores"
        assert jsonLogic({"var": "address.number"}, data) == 123

        # Acesso a array
        assert jsonLogic({"var": "hobbies.0"}, data) == "leitura"
        assert jsonLogic({"var": "hobbies.2"}, data) == "culinária"

        # Valor padrão
        assert jsonLogic({"var": ["nonexistent", "default"]}, data) == "default"
        assert jsonLogic({"var": "nonexistent"}, data) is None

    def test_variable_access_edge_cases(self):
        """Testa casos especiais de acesso a variáveis"""
        data = {"numbers": [10, 20, 30], "nested": {"deep": {"value": 42}}}

        # Índice fora do range
        assert jsonLogic({"var": "numbers.5"}, data) is None

        # Acesso profundo
        assert jsonLogic({"var": "nested.deep.value"}, data) == 42

        # Acesso com chave inexistente no meio do caminho
        assert jsonLogic({"var": "nested.nonexistent.value"}, data) is None

    def test_function_application(self):
        """Testa aplicação de funções"""

        def uppercase(text):
            return text.upper()

        def add_numbers(a, b):
            return a + b

        def format_name(first, last):
            return f"{last.upper()}, {first.capitalize()}"

        functions = {
            "uppercase": uppercase,
            "add": add_numbers,
            "format_name": format_name,
        }

        # Função simples
        result = jsonLogic({"apply": ["uppercase", "hello"]}, functions=functions)
        assert result == "HELLO"

        # Função com múltiplos argumentos
        result = jsonLogic({"apply": ["add", 5, 3]}, functions=functions)
        assert result == 8

        # Função com dados de contexto
        data = {"user": {"first": "joão", "last": "silva"}}
        rule = {"apply": ["format_name", {"var": "user.first"}, {"var": "user.last"}]}
        result = jsonLogic(rule, data, functions)
        assert result == "SILVA, João"

    def test_function_application_errors(self):
        """Testa erros na aplicação de funções"""
        # Função não registrada
        with pytest.raises(
            NameError,
            match="Função pura não registrada ou não permitida: 'nonexistent'",
        ):
            jsonLogic({"apply": ["nonexistent", "arg"]}, functions={})

        # Apply sem argumentos
        with pytest.raises(
            ValueError, match="A operação 'apply' requer pelo menos um argumento"
        ):
            jsonLogic({"apply": []}, functions={})

    def test_complex_nested_logic(self):
        """Testa lógica complexa aninhada"""
        data = {
            "user": {"name": "João", "age": 25, "premium": True},
            "product": {"price": 100, "category": "electronics"},
        }

        # Lógica complexa: usuário premium E (idade > 18 OU preço < 50)
        rule = {
            "and": [
                {"var": "user.premium"},
                {
                    "or": [
                        {">": [{"var": "user.age"}, 18]},
                        {"<": [{"var": "product.price"}, 50]},
                    ]
                },
            ]
        }

        assert jsonLogic(rule, data)

        # Modificando dados para testar False
        data["user"]["premium"] = False
        assert not jsonLogic(rule, data)

    def test_log_operation(self):
        """Testa operação de log"""
        with patch("sys.stdout") as mock_stdout:
            result = jsonLogic({"log": "test message"})
            assert result == "test message"
            # Verifica se print foi chamado
            mock_stdout.write.assert_called()

    def test_non_dict_input(self):
        """Testa entrada que não é dicionário"""
        # Valores primitivos devem ser retornados como estão
        assert jsonLogic("string") == "string"
        assert jsonLogic(42) == 42
        assert jsonLogic(True)
        assert jsonLogic([1, 2, 3]) == [1, 2, 3]

    def test_empty_dict_input(self):
        """Testa entrada com dicionário vazio"""
        assert jsonLogic({}) is None

    def test_unknown_operation(self):
        """Testa operação não reconhecida"""
        with pytest.raises(RuntimeError, match="Operação não reconhecida: unknown_op"):
            jsonLogic({"unknown_op": ["arg1", "arg2"]})

    def test_single_value_operations(self):
        """Testa operações com valores únicos (não em lista)"""
        # Operações que normalmente recebem listas devem funcionar com valores únicos
        assert not jsonLogic({"!": True})
        assert jsonLogic({"+": 5}) == 5.0
        assert jsonLogic({"*": 3}) == 3.0

    def test_comprehensive_example(self):
        """Teste abrangente com exemplo do docstring"""

        def formatar_nome_completo(primeiro, ultimo):
            return f"{ultimo.upper()}, {primeiro.capitalize()}"

        def calcular_area(largura, altura):
            return largura * altura

        funcoes_permitidas = {
            "format_name": formatar_nome_completo,
            "get_area": calcular_area,
        }

        dados = {
            "usuario": {"nome": "joão", "sobrenome": "silva"},
            "retangulo": {"l": 10, "a": 5},
        }

        regra_nome = {
            "apply": [
                "format_name",
                {"var": "usuario.nome"},
                {"var": "usuario.sobrenome"},
            ]
        }

        regra_area = {
            ">": [
                {"apply": ["get_area", {"var": "retangulo.l"}, {"var": "retangulo.a"}]},
                40,
            ]
        }

        nome_formatado = jsonLogic(regra_nome, dados, funcoes_permitidas)
        area_e_grande = jsonLogic(regra_area, dados, funcoes_permitidas)

        assert nome_formatado == "SILVA, João"
        assert area_e_grande

    def test_edge_cases_with_none_values(self):
        """Testa casos especiais com valores None"""
        # Operações com None
        assert jsonLogic({"==": [None, None]})
        assert not jsonLogic({"==": [None, 0]})
        assert jsonLogic({"!=": [None, 0]})

        # Var com None como padrão
        assert jsonLogic({"var": ["nonexistent", None]}, {}) is None

    def test_division_by_zero(self):
        """Testa divisão por zero"""
        with pytest.raises(ZeroDivisionError):
            jsonLogic({"/": [10, 0]})

    def test_type_conversion_in_arithmetic(self):
        """Testa conversão de tipos em operações aritméticas"""
        # String para número
        assert jsonLogic({"+": ["10", "20"]}) == 30.0
        assert jsonLogic({"*": ["3", "4"]}) == 12.0

        # Mix de tipos
        assert jsonLogic({"+": [10, "5", 2.5]}) == 17.5
