#!/usr/bin/env python3
"""
Script de exemplo para demonstrar como usar o backend Python do RuleTester.
"""

import requests
import json
import time

# Configuração do servidor
SERVER_URL = "http://localhost:5000"

def test_backend_connection():
    """Testa se o backend está rodando."""
    try:
        response = requests.get(f"{SERVER_URL}/api/health")
        if response.status_code == 200:
            print("✅ Backend está rodando!")
            return True
        else:
            print(f"❌ Backend retornou status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao backend.")
        print("   Certifique-se de que o servidor está rodando: python src/api_server.py")
        return False

def test_rule_processing():
    """Testa o processamento de regras."""
    print("\n🧪 Testando processamento de regras...")
    
    # Exemplo 1: Regra simples
    rule1 = {
        ">": [
            {"var": "idade"},
            18
        ]
    }
    
    data1 = {
        "idade": 25
    }
    
    result1 = process_rule(rule1, data1)
    print(f"Teste 1 - Idade > 18: {result1}")
    
    # Exemplo 2: Regra complexa
    rule2 = {
        "and": [
            {">": [{"var": "score"}, 600]},
            {">": [{"var": "renda"}, 3000]},
            {"!": {"var": "possui_divida"}}
        ]
    }
    
    data2 = {
        "score": 750,
        "renda": 5000,
        "possui_divida": False
    }
    
    result2 = process_rule(rule2, data2)
    print(f"Teste 2 - Aprovação empréstimo: {result2}")
    
    # Exemplo 3: Regra com resultado condicional
    rule3 = {
        "if": [
            {">": [{"var": "score"}, 800]},
            "Premium",
            {
                "if": [
                    {">": [{"var": "score"}, 600]},
                    "Regular",
                    "Básico"
                ]
            }
        ]
    }
    
    data3 = {
        "score": 720
    }
    
    result3 = process_rule(rule3, data3)
    print(f"Teste 3 - Categoria cliente: {result3}")

def process_rule(rule, data):
    """Processa uma regra usando o backend."""
    try:
        response = requests.post(
            f"{SERVER_URL}/api/process-rule",
            json={"rule": rule, "data": data},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                return result["result"]
            else:
                return f"Erro: {result.get('error')}"
        else:
            return f"Erro HTTP {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Erro de conexão: {str(e)}"

def validate_rule(rule):
    """Valida uma regra sem processar dados."""
    try:
        response = requests.post(
            f"{SERVER_URL}/api/validate-rule",
            json={"rule": rule},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("valid", False), result.get("error", "")
        else:
            return False, f"Erro HTTP {response.status_code}"
            
    except Exception as e:
        return False, f"Erro de conexão: {str(e)}"

def test_rule_validation():
    """Testa a validação de regras."""
    print("\n✅ Testando validação de regras...")
    
    # Regra válida
    valid_rule = {
        "and": [
            {">": [{"var": "x"}, 10]},
            {"<": [{"var": "x"}, 100]}
        ]
    }
    
    is_valid, error = validate_rule(valid_rule)
    print(f"Regra válida: {is_valid}")
    if error:
        print(f"  Erro: {error}")
    
    # Regra inválida
    invalid_rule = {
        "invalid_operator": [{"var": "x"}, 10]
    }
    
    is_valid, error = validate_rule(invalid_rule)
    print(f"Regra inválida: {is_valid}")
    if error:
        print(f"  Erro: {error}")

def interactive_test():
    """Permite testar regras interativamente."""
    print("\n🎮 Modo interativo - Digite suas regras e dados:")
    print("Digite 'quit' para sair\n")
    
    while True:
        try:
            print("Digite a regra JSON Logic:")
            rule_input = input("> ")
            
            if rule_input.lower() == 'quit':
                break
                
            rule = json.loads(rule_input)
            
            print("Digite os dados JSON:")
            data_input = input("> ")
            
            if data_input.lower() == 'quit':
                break
                
            data = json.loads(data_input)
            
            result = process_rule(rule, data)
            print(f"Resultado: {result}\n")
            
        except json.JSONDecodeError:
            print("❌ JSON inválido. Tente novamente.\n")
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
            break

def main():
    """Função principal."""
    print("🚀 Testador do Backend Python - JSON Logic")
    print("=" * 50)
    
    # Testa conexão
    if not test_backend_connection():
        return
    
    # Executa testes automáticos
    test_rule_processing()
    test_rule_validation()
    
    # Pergunta se quer modo interativo
    print("\n" + "=" * 50)
    choice = input("Deseja testar regras interativamente? (s/n): ").lower()
    
    if choice in ['s', 'sim', 'y', 'yes']:
        interactive_test()
    
    print("\n👋 Teste concluído!")

if __name__ == "__main__":
    main()
