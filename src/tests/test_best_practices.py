"""
Teste demonstrando as melhores práticas do JSON Logic
- Como evitar objetos literais nas regras
- Focar em operações lógicas puras
"""

from src.lib.json_logic import jsonLogic


def demonstrar_anti_pattern():
    """Demonstra o que NÃO deve ser feito - objetos literais nas regras"""
    print("❌ ANTI-PATTERN: Objetos literais nas regras")
    print("-" * 50)
    
    # Dados de exemplo
    dados = {
        "usuario": {"idade": 17, "tipo": "regular"},
        "produto": {"categoria": "bebidas_alcoolicas", "preco": 25.0}
    }
    
    # ❌ ERRADO: Objeto literal como valor de retorno
    regra_incorreta = {
        "if": [
            {">": [{"var": "usuario.idade"}, 18]},
            True,  # ✅ Correto: valor simples
            {"aprovado": False, "motivo": "Menor de idade"}  # ❌ Objeto literal
        ]
    }
    
    try:
        resultado = jsonLogic(regra_incorreta, dados)
        print(f"Resultado incorreto: {resultado}")
        print("⚠️  O JSON Logic teve que processar um objeto literal como dados")
    except Exception as e:
        print(f"Erro: {e}")


def demonstrar_best_practice():
    """Demonstra as melhores práticas - operações lógicas puras"""
    print("\n✅ BEST PRACTICE: Operações lógicas puras")
    print("-" * 50)
    
    # Função para validação de idade
    def pode_comprar_bebida(idade, categoria):
        if categoria == "bebidas_alcoolicas":
            return idade >= 18
        return True
    
    def calcular_desconto(tipo_usuario, valor_compra):
        if tipo_usuario == "vip":
            return valor_compra * 0.15
        elif tipo_usuario == "premium":
            return valor_compra * 0.10
        elif valor_compra > 100:
            return valor_compra * 0.05
        return 0
    
    funcoes = {
        "pode_comprar": pode_comprar_bebida,
        "calcular_desconto": calcular_desconto
    }
    
    # Dados de exemplo
    dados = {
        "usuario": {"idade": 25, "tipo": "vip"},
        "produto": {"categoria": "bebidas_alcoolicas", "preco": 150.0}
    }
    
    # ✅ CORRETO: Apenas operações lógicas
    regras_corretas = [
        # Regra 1: Verificação de idade (retorna boolean)
        {
            "apply": [
                "pode_comprar",
                {"var": "usuario.idade"},
                {"var": "produto.categoria"}
            ]
        },
        
        # Regra 2: Verificação se é maior de idade (operação pura)
        {
            ">=": [
                {"var": "usuario.idade"},
                18
            ]
        },
        
        # Regra 3: Cálculo de desconto (retorna número)
        {
            "apply": [
                "calcular_desconto",
                {"var": "usuario.tipo"},
                {"var": "produto.preco"}
            ]
        },
        
        # Regra 4: Verificação se tem desconto (operação lógica)
        {
            ">": [
                {
                    "apply": [
                        "calcular_desconto",
                        {"var": "usuario.tipo"},
                        {"var": "produto.preco"}
                    ]
                },
                0
            ]
        },
        
        # Regra 5: Lógica complexa combinando condições
        {
            "and": [
                {
                    "apply": [
                        "pode_comprar",
                        {"var": "usuario.idade"},
                        {"var": "produto.categoria"}
                    ]
                },
                {
                    "or": [
                        {"==": [{"var": "usuario.tipo"}, "vip"]},
                        {">": [{"var": "produto.preco"}, 100]}
                    ]
                }
            ]
        }
    ]
    
    print("Executando regras corretas:")
    for i, regra in enumerate(regras_corretas, 1):
        resultado = jsonLogic(regra, dados, funcoes)
        print(f"Regra {i}: {resultado}")
    
    print("\n✅ Todas as regras retornam valores simples (boolean, number, string)")
    print("✅ Nenhum objeto literal foi incluído nas regras")
    print("✅ A lógica fica mais clara e focada")


def demonstrar_separacao_responsabilidades():
    """Demonstra a separação entre lógica e apresentação"""
    print("\n🎯 SEPARAÇÃO DE RESPONSABILIDADES")
    print("-" * 50)
    
    def avaliar_credito(renda, idade, score):
        """Função pura que retorna apenas o resultado da avaliação"""
        if score < 300:
            return "rejeitado"
        elif score < 600:
            return "analise_manual"
        elif renda < 2000:
            return "limite_baixo"
        else:
            return "aprovado"
    
    funcoes = {"avaliar_credito": avaliar_credito}
    
    dados = {
        "cliente": {"renda": 5000, "idade": 30, "score": 750}
    }
    
    # ✅ CORRETO: Regra retorna apenas o status
    regra_avaliacao = {
        "apply": [
            "avaliar_credito",
            {"var": "cliente.renda"},
            {"var": "cliente.idade"},
            {"var": "cliente.score"}
        ]
    }
    
    status = jsonLogic(regra_avaliacao, dados, funcoes)
    print(f"Status da avaliação: {status}")
    
    # ✅ CORRETO: Mapeamento de apresentação fica FORA do JSON Logic
    mensagens = {
        "aprovado": {
            "texto": "Parabéns! Seu crédito foi aprovado.",
            "cor": "verde",
            "acao": "mostrar_ofertas"
        },
        "rejeitado": {
            "texto": "Infelizmente não foi possível aprovar seu crédito.",
            "cor": "vermelho", 
            "acao": "mostrar_alternativas"
        },
        "analise_manual": {
            "texto": "Sua solicitação está em análise.",
            "cor": "amarelo",
            "acao": "agendar_contato"
        },
        "limite_baixo": {
            "texto": "Aprovado com limite reduzido.",
            "cor": "azul",
            "acao": "mostrar_limite"
        }
    }
    
    resposta_final = mensagens.get(status, {"texto": "Status desconhecido"})
    print(f"Resposta ao cliente: {resposta_final}")
    
    print("\n✅ JSON Logic foca apenas na LÓGICA")
    print("✅ Apresentação e mapeamento ficam na APLICAÇÃO")
    print("✅ Cada responsabilidade no seu lugar")


def main():
    """Executa todos os exemplos de boas práticas"""
    print("🎯 MELHORES PRÁTICAS DO JSON LOGIC")
    print("=" * 60)
    print("Demonstração do que fazer e o que evitar")
    print("=" * 60)
    
    demonstrar_anti_pattern()
    demonstrar_best_practice()
    demonstrar_separacao_responsabilidades()
    
    print("\n" + "=" * 60)
    print("📋 RESUMO DAS MELHORES PRÁTICAS:")
    print("✅ Use apenas operações lógicas puras")
    print("✅ Retorne valores simples (boolean, number, string)")
    print("✅ Evite objetos literais nas regras")
    print("✅ Separe lógica de apresentação")
    print("✅ Use funções para cálculos complexos")
    print("❌ Não inclua objetos de resposta nas regras")
    print("❌ Não misture lógica com formatação")
    print("=" * 60)


if __name__ == "__main__":
    main()
