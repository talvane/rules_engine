# file: regras.py

# A lógica foi aninhada para evitar a comparação de um valor None com um número.


REGRAS_VALIDACAO = [
    {"if": [{"==": [{"var": "pontuacao_credito"}, None]}, "ERRO_SCORE_INVALIDO", None]}
]

# Regra de processamento
REGRA_PROCESSAMENTO = {
    "if": [
        {"<": [{"var": "idade"}, 18]},
        "RECUSADO",
        {
            "if": [
                {"var": "possui_divida_ativa"},
                "ANALISE_MANUAL",
                {
                    "if": [
                        {
                            "and": [
                                {"<": [{"var": "pontuacao_credito"}, 500]},
                                {"<": [{"var": "renda_mensal"}, 1000]},
                            ]
                        },
                        "ANALISE_MANUAL",
                        "APROVADO",
                    ]
                },
            ]
        },
    ]
}
