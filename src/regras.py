# file: regras.py

# A lógica foi aninhada para evitar a comparação de um valor None com um número.


REGRAS_VALIDACAO = [
    {"if": [{"==": [{"var": "pontuacao_credito"}, None]}, "ERRO_SCORE_INVALIDO", None]}
]

# Regra de processamento
REGRA_PROCESSAMENTO = {
    "if": [
        {"<": [{"var": "Idade"}, 18]},
        "RECUSADO",
        {
            "if": [
                {"<": [{"var": "pontuacao_credito"}, 750]},
                "ANALISE_MANUAL",
                {
                    "if": [
                        {"!=": [{"var": "possui_divida_ativa"}, False]},
                        "ANALISE_MANUAL",
                        "APROVADO",
                    ]
                },
            ]
        },
    ]
}
