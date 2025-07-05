from motor_regras import MotorDeRegrasCustom

if __name__ == "__main__":
    motor = MotorDeRegrasCustom()

    # Cenário 1: Cliente aprovado
    solicitacao_1 = {
        "id": "REQ-101",
        "pontuacao_credito": 800,
        "renda_mensal": 7000,
        "valor_solicitado": 10000,
        "possui_divida_ativa": False
    }
    resultado_1 = motor.executar(solicitacao_1)
    print("\nResultado final do objeto:", resultado_1)
    print("-" * 50)

    # Cenário 2: Cliente com score baixo para recusa
    solicitacao_2 = {
        "id": "REQ-102",
        "pontuacao_credito": 450,
        "renda_mensal": 2500,
        "valor_solicitado": 5000,
        "possui_divida_ativa": True
    }
    resultado_2 = motor.executar(solicitacao_2)
    print("\nResultado final do objeto:", resultado_2)
    print("-" * 50)
    
    # Cenário 3: Cliente que vai para análise manual
    solicitacao_3 = {
        "id": "REQ-103",
        "pontuacao_credito": 650,
        "renda_mensal": 5000,
        "valor_solicitado": 15000,
        "possui_divida_ativa": True
    }
    resultado_3 = motor.executar(solicitacao_3)
    print("\nResultado final do objeto:", resultado_3)
    print("-" * 50)

    # Cenário 4: Dados inválidos
    solicitacao_4 = {
        "id": "REQ-104",
        "pontuacao_credito": None,
        "renda_mensal": 4000,
        "valor_solicitado": 12000,
        "possui_divida_ativa": False
    }
    resultado_4 = motor.executar(solicitacao_4)
    print("\nResultado final do objeto:", resultado_4)
    print("-" * 50)
