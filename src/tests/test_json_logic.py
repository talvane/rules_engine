import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.lib.json_logic import jsonLogic, _get_nested_value


def test_basic_operations():
    """Testa operações básicas"""
    print("=== Testando operações básicas ===")

    # Teste de comparação
    assert jsonLogic({"==": [1, 1]}) == True
    assert jsonLogic({">": [5, 3]}) == True
    assert jsonLogic({"<": [1, 2, 3]}) == True
    print("✓ Comparações funcionando")

    # Teste de lógica
    assert jsonLogic({"and": [True, True]}) == True
    assert jsonLogic({"or": [False, True]}) == True
    assert jsonLogic({"!": [False]}) == True
    print("✓ Operações lógicas funcionando")

    # Teste de matemática
    assert jsonLogic({"+": [1, 2, 3]}) == 6.0
    assert jsonLogic({"*": [2, 3, 4]}) == 24.0
    assert jsonLogic({"-": [10, 3]}) == 7
    print("✓ Operações matemáticas funcionando")


def test_nested_value_access():
    """Testa acesso a valores aninhados"""
    print("\n=== Testando acesso a valores aninhados ===")

    data = {"usuario": {"nome": "João", "idade": 30, "enderecos": ["Rua A", "Rua B"]}}

    # Teste da função auxiliar
    assert _get_nested_value("usuario.nome", data) == "João"
    assert _get_nested_value("usuario.idade", data) == 30
    assert _get_nested_value("usuario.enderecos.0", data) == "Rua A"
    assert _get_nested_value("usuario.inexistente", data, "default") == "default"
    print("✓ Função _get_nested_value funcionando")

    # Teste via jsonLogic
    assert jsonLogic({"var": "usuario.nome"}, data) == "João"
    assert jsonLogic({"var": "usuario.enderecos.1"}, data) == "Rua B"
    print("✓ Operação 'var' funcionando")


def test_custom_functions():
    """Testa funções customizadas"""
    print("\n=== Testando funções customizadas ===")

    def somar(a, b):
        return a + b

    def formatar_nome(primeiro, ultimo):
        return f"{ultimo.upper()}, {primeiro.capitalize()}"

    functions = {"somar": somar, "formatar_nome": formatar_nome}

    data = {"a": 5, "b": 3, "nome": "joão", "sobrenome": "silva"}

    # Teste de função simples
    result = jsonLogic(
        {"apply": ["somar", {"var": "a"}, {"var": "b"}]}, data, functions
    )
    assert result == 8
    print("✓ Função de soma funcionando")

    # Teste de função de formatação
    result = jsonLogic(
        {"apply": ["formatar_nome", {"var": "nome"}, {"var": "sobrenome"}]},
        data,
        functions,
    )
    assert result == "SILVA, João"
    print("✓ Função de formatação funcionando")


def test_complex_rules():
    """Testa regras complexas"""
    print("\n=== Testando regras complexas ===")

    data = {"usuario": {"idade": 25, "ativo": True, "tipo": "premium"}}

    # Regra complexa: usuário ativo E (idade >= 18 OU tipo premium)
    rule = {
        "and": [
            {"var": "usuario.ativo"},
            {
                "or": [
                    {">=": [{"var": "usuario.idade"}, 18]},
                    {"==": [{"var": "usuario.tipo"}, "premium"]},
                ]
            },
        ]
    }

    assert jsonLogic(rule, data) == True
    print("✓ Regra complexa funcionando")


def main():
    """Executa todos os testes"""
    print("Iniciando testes...")

    try:
        test_basic_operations()
        test_nested_value_access()
        test_custom_functions()
        test_complex_rules()

        print("\n🎉 Todos os testes passaram!")

    except Exception as e:
        print(f"\n❌ Erro nos testes: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
