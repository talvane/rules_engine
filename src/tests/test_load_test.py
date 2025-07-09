#!/usr/bin/env python3
"""
Teste massivo de carga com diferentes cenários e payloads para JSON Logic
"""

import sys
import os
import time
import random
from typing import List, Dict, Callable

# Adiciona o path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.lib.json_logic import jsonLogic


# ========== CENÁRIOS DE TESTE ==========


class TestScenario:
    """Classe para representar um cenário de teste"""

    def __init__(
        self,
        nome: str,
        regras: List[Dict],
        dados: List[Dict],
        funcoes: Dict[str, Callable],
    ):
        self.nome = nome
        self.regras = regras
        self.dados = dados
        self.funcoes = funcoes


def criar_cenario_ecommerce():
    """Cenário de e-commerce com regras de negócio"""

    def calcular_frete(peso, cep_destino):
        """Simula cálculo de frete"""
        base = 10.0
        if peso > 5:
            base *= 1.5
        if cep_destino.startswith("0") or cep_destino.startswith("1"):
            base *= 1.2  # Região mais cara
        return round(base, 2)

    def validar_cupom(codigo, valor_minimo):
        """Valida cupom de desconto"""
        cupons_validos = {
            "SAVE10": {"desconto": 0.1, "minimo": 100},
            "SAVE20": {"desconto": 0.2, "minimo": 200},
            "FRETEGRATIS": {"desconto": 0.0, "minimo": 150, "frete_gratis": True},
            "PRIMEIRA": {"desconto": 0.15, "minimo": 50},
        }

        if codigo in cupons_validos:
            cupom = cupons_validos[codigo]
            if valor_minimo >= cupom["minimo"]:
                return {
                    "valido": True,
                    "desconto": cupom.get("desconto", 0),
                    "frete_gratis": cupom.get("frete_gratis", False),
                }

        return {"valido": False, "desconto": 0, "frete_gratis": False}

    def categoria_permitida(categoria, idade_cliente):
        """Verifica se categoria é permitida para idade"""
        restricoes = {
            "bebidas_alcoolicas": 18,
            "cigarros": 18,
            "jogos_adultos": 18,
            "suplementos": 16,
        }

        return idade_cliente >= restricoes.get(categoria, 0)

    funcoes = {
        "calcular_frete": calcular_frete,
        "validar_cupom": validar_cupom,
        "categoria_permitida": categoria_permitida,
    }

    dados = [
        {
            "cliente": {
                "id": 1,
                "nome": "João",
                "idade": 25,
                "vip": True,
                "cep": "01234-567",
            },
            "carrinho": {
                "itens": [
                    {
                        "produto": "Notebook",
                        "preco": 2000,
                        "quantidade": 1,
                        "peso": 2.5,
                        "categoria": "eletronicos",
                    },
                    {
                        "produto": "Mouse",
                        "preco": 50,
                        "quantidade": 2,
                        "peso": 0.3,
                        "categoria": "eletronicos",
                    },
                ],
                "total": 2100,
                "peso_total": 3.1,
            },
            "cupom": "SAVE10",
            "metodo_pagamento": "cartao_credito",
        },
        {
            "cliente": {
                "id": 2,
                "nome": "Maria",
                "idade": 17,
                "vip": False,
                "cep": "20000-000",
            },
            "carrinho": {
                "itens": [
                    {
                        "produto": "Livro",
                        "preco": 30,
                        "quantidade": 3,
                        "peso": 0.5,
                        "categoria": "livros",
                    },
                    {
                        "produto": "Cerveja",
                        "preco": 15,
                        "quantidade": 6,
                        "peso": 0.6,
                        "categoria": "bebidas_alcoolicas",
                    },
                ],
                "total": 180,
                "peso_total": 5.1,
            },
            "cupom": "PRIMEIRA",
            "metodo_pagamento": "pix",
        },
        {
            "cliente": {
                "id": 3,
                "nome": "Carlos",
                "idade": 30,
                "vip": True,
                "cep": "30000-000",
            },
            "carrinho": {
                "itens": [
                    {
                        "produto": "Suplemento",
                        "preco": 100,
                        "quantidade": 2,
                        "peso": 1.0,
                        "categoria": "suplementos",
                    }
                ],
                "total": 200,
                "peso_total": 2.0,
            },
            "cupom": "FRETEGRATIS",
            "metodo_pagamento": "boleto",
        },
    ]

    regras = [
        # Regra 1: Validação de idade para produtos restritos
        {
            "!": [
                {
                    "some": [
                        {"var": "carrinho.itens"},
                        {
                            "!": [
                                {
                                    "apply": [
                                        "categoria_permitida",
                                        {"var": "categoria"},
                                        {"var": "cliente.idade"},
                                    ]
                                }
                            ]
                        },
                    ]
                }
            ]
        },
        # Regra 2: Verificação se cupom é válido (retorna boolean)
        {
            "if": [
                {"!=": [{"var": "cupom"}, ""]},
                {
                    ">": [
                        {"var": "carrinho.total"},
                        100  # Valor mínimo para cupom básico
                    ]
                },
                False
            ]
        },
        # Regra 3: Cálculo de frete
        {
            "apply": [
                "calcular_frete",
                {"var": "carrinho.peso_total"},
                {"var": "cliente.cep"},
            ]
        },
        # Regra 4: Cliente VIP tem frete grátis acima de R$ 500
        {
            "if": [
                {
                    "and": [
                        {"var": "cliente.vip"},
                        {">": [{"var": "carrinho.total"}, 500]},
                    ]
                },
                0,
                {
                    "apply": [
                        "calcular_frete",
                        {"var": "carrinho.peso_total"},
                        {"var": "cliente.cep"},
                    ]
                },
            ]
        },
        # Regra 5: Validação de método de pagamento
        {
            "or": [
                {
                    "and": [
                        {"==": [{"var": "metodo_pagamento"}, "cartao_credito"]},
                        {"<": [{"var": "carrinho.total"}, 5000]},
                    ]
                },
                {
                    "and": [
                        {"==": [{"var": "metodo_pagamento"}, "pix"]},
                        {"<": [{"var": "carrinho.total"}, 10000]},
                    ]
                },
                {"==": [{"var": "metodo_pagamento"}, "boleto"]},
            ]
        },
    ]

    return TestScenario("E-commerce", regras, dados, funcoes)


def criar_cenario_financeiro():
    """Cenário financeiro com análise de risco"""

    def calcular_score_risco(renda, idade, historico_credito, dividas):
        """Calcula score de risco para empréstimo"""
        score = 500  # Score base

        # Fator renda
        if renda > 10000:
            score += 200
        elif renda > 5000:
            score += 100
        elif renda > 2000:
            score += 50

        # Fator idade
        if 25 <= idade <= 55:
            score += 100
        elif 18 <= idade <= 24 or 56 <= idade <= 65:
            score += 50

        # Histórico de crédito
        if historico_credito == "excelente":
            score += 150
        elif historico_credito == "bom":
            score += 100
        elif historico_credito == "regular":
            score += 50

        # Dívidas
        if dividas < renda * 0.3:
            score += 100
        elif dividas < renda * 0.5:
            score += 50

        return min(score, 1000)

    def aprovar_emprestimo(score, valor_solicitado, renda_mensal):
        """Decide aprovação de empréstimo"""
        if score < 600:
            return {"aprovado": False, "motivo": "Score insuficiente"}

        if valor_solicitado > renda_mensal * 10:
            return {"aprovado": False, "motivo": "Valor muito alto para a renda"}

        if score >= 800:
            return {"aprovado": True, "taxa": 0.015, "motivo": "Cliente premium"}
        elif score >= 700:
            return {"aprovado": True, "taxa": 0.025, "motivo": "Cliente qualificado"}
        else:
            return {"aprovado": True, "taxa": 0.035, "motivo": "Cliente padrão"}

    def calcular_limite_cartao(renda, score, relacionamento_anos):
        """Calcula limite do cartão de crédito"""
        limite_base = renda * 3

        if score >= 800:
            limite_base *= 1.5
        elif score >= 700:
            limite_base *= 1.2
        elif score < 600:
            limite_base *= 0.5

        if relacionamento_anos > 5:
            limite_base *= 1.3
        elif relacionamento_anos > 2:
            limite_base *= 1.1

        return round(limite_base, 2)

    funcoes = {
        "calcular_score_risco": calcular_score_risco,
        "aprovar_emprestimo": aprovar_emprestimo,
        "calcular_limite_cartao": calcular_limite_cartao,
    }

    dados = [
        {
            "cliente": {
                "id": 1,
                "nome": "João Silva",
                "idade": 35,
                "renda_mensal": 8000,
                "historico_credito": "excelente",
                "dividas_atuais": 1500,
                "relacionamento_anos": 7,
                "conta_corrente": True,
            },
            "solicitacao": {
                "tipo": "emprestimo",
                "valor": 50000,
                "prazo_meses": 24,
                "finalidade": "reforma_casa",
            },
        },
        {
            "cliente": {
                "id": 2,
                "nome": "Maria Santos",
                "idade": 28,
                "renda_mensal": 4500,
                "historico_credito": "bom",
                "dividas_atuais": 800,
                "relacionamento_anos": 3,
                "conta_corrente": True,
            },
            "solicitacao": {
                "tipo": "cartao_credito",
                "valor": 0,
                "prazo_meses": 0,
                "finalidade": "compras",
            },
        },
        {
            "cliente": {
                "id": 3,
                "nome": "Pedro Costa",
                "idade": 22,
                "renda_mensal": 2000,
                "historico_credito": "regular",
                "dividas_atuais": 1200,
                "relacionamento_anos": 1,
                "conta_corrente": False,
            },
            "solicitacao": {
                "tipo": "emprestimo",
                "valor": 10000,
                "prazo_meses": 12,
                "finalidade": "educacao",
            },
        },
    ]

    regras = [
        # Regra 1: Cálculo de score de risco
        {
            "apply": [
                "calcular_score_risco",
                {"var": "cliente.renda_mensal"},
                {"var": "cliente.idade"},
                {"var": "cliente.historico_credito"},
                {"var": "cliente.dividas_atuais"},
            ]
        },
        # Regra 2: Verificação se empréstimo seria aprovado (boolean)
        {
            "if": [
                {"==": [{"var": "solicitacao.tipo"}, "emprestimo"]},
                {
                    ">": [
                        {
                            "apply": [
                                "calcular_score_risco",
                                {"var": "cliente.renda_mensal"},
                                {"var": "cliente.idade"},
                                {"var": "cliente.historico_credito"},
                                {"var": "cliente.dividas_atuais"},
                            ]
                        },
                        600  # Score mínimo
                    ]
                },
                False
            ]
        },
        # Regra 3: Cálculo de limite do cartão
        {
            "if": [
                {"==": [{"var": "solicitacao.tipo"}, "cartao_credito"]},
                {
                    "apply": [
                        "calcular_limite_cartao",
                        {"var": "cliente.renda_mensal"},
                        {
                            "apply": [
                                "calcular_score_risco",
                                {"var": "cliente.renda_mensal"},
                                {"var": "cliente.idade"},
                                {"var": "cliente.historico_credito"},
                                {"var": "cliente.dividas_atuais"},
                            ]
                        },
                        {"var": "cliente.relacionamento_anos"},
                    ]
                },
                0,
            ]
        },
        # Regra 4: Pré-aprovação (regra complexa)
        {
            "and": [
                {"var": "cliente.conta_corrente"},
                {">": [{"var": "cliente.renda_mensal"}, 3000]},
                {
                    "<": [
                        {"var": "cliente.dividas_atuais"},
                        {"*": [{"var": "cliente.renda_mensal"}, 0.4]},
                    ]
                },
                {
                    ">": [
                        {
                            "apply": [
                                "calcular_score_risco",
                                {"var": "cliente.renda_mensal"},
                                {"var": "cliente.idade"},
                                {"var": "cliente.historico_credito"},
                                {"var": "cliente.dividas_atuais"},
                            ]
                        },
                        650,
                    ]
                },
            ]
        },
        # Regra 5: Cliente premium
        {
            "and": [
                {">": [{"var": "cliente.renda_mensal"}, 15000]},
                {"==": [{"var": "cliente.historico_credito"}, "excelente"]},
                {">": [{"var": "cliente.relacionamento_anos"}, 5]},
            ]
        },
    ]

    return TestScenario("Financeiro", regras, dados, funcoes)


def criar_cenario_iot():
    """Cenário IoT com sensores e automação"""

    def calcular_consumo_energia(dispositivos_ativos, tempo_uso_horas):
        """Calcula consumo de energia"""
        consumo_por_dispositivo = {
            "luz_led": 0.01,
            "luz_incandescente": 0.06,
            "ar_condicionado": 2.5,
            "geladeira": 0.15,
            "tv": 0.12,
            "computador": 0.3,
        }

        total = 0
        for dispositivo in dispositivos_ativos:
            total += consumo_por_dispositivo.get(dispositivo, 0.1) * tempo_uso_horas

        return round(total, 2)

    def determinar_acao_clima(temperatura, umidade, presenca):
        """Determina ação do sistema de climatização"""
        if not presenca:
            return {"acao": "desligar", "motivo": "Sem presença"}

        if temperatura > 26 and umidade > 70:
            return {
                "acao": "ar_condicionado",
                "potencia": 80,
                "motivo": "Muito quente e úmido",
            }
        elif temperatura > 24:
            return {
                "acao": "ventilador",
                "potencia": 60,
                "motivo": "Temperatura elevada",
            }
        elif temperatura < 18:
            return {"acao": "aquecedor", "potencia": 50, "motivo": "Temperatura baixa"}
        else:
            return {"acao": "manter", "potencia": 0, "motivo": "Temperatura ideal"}

    def calcular_score_seguranca(
        sensores_porta, sensores_janela, cameras_ativas, alarme_ativo
    ):
        """Calcula score de segurança"""
        score = 0

        # Pontos por sensores
        score += len(sensores_porta) * 20
        score += len(sensores_janela) * 15
        score += len(cameras_ativas) * 25

        # Bonus por alarme ativo
        if alarme_ativo:
            score += 50

        return min(score, 100)

    funcoes = {
        "calcular_consumo_energia": calcular_consumo_energia,
        "determinar_acao_clima": determinar_acao_clima,
        "calcular_score_seguranca": calcular_score_seguranca,
    }

    dados = [
        {
            "sensores": {
                "temperatura": 25.5,
                "umidade": 65,
                "luminosidade": 300,
                "presenca": True,
                "movimento": False,
            },
            "dispositivos": {
                "luzes": ["luz_led", "luz_led", "luz_incandescente"],
                "climatizacao": ["ar_condicionado"],
                "eletronicos": ["tv", "computador"],
                "seguranca": [
                    "camera_sala",
                    "camera_entrada",
                    "sensor_porta_principal",
                ],
            },
            "configuracao": {
                "modo_economia": False,
                "temperatura_ideal": 23,
                "alarme_ativo": True,
                "horario": "18:30",
            },
        },
        {
            "sensores": {
                "temperatura": 19.2,
                "umidade": 45,
                "luminosidade": 150,
                "presenca": False,
                "movimento": True,
            },
            "dispositivos": {
                "luzes": ["luz_led"],
                "climatizacao": [],
                "eletronicos": ["geladeira"],
                "seguranca": ["sensor_porta_principal", "sensor_janela_quarto"],
            },
            "configuracao": {
                "modo_economia": True,
                "temperatura_ideal": 21,
                "alarme_ativo": False,
                "horario": "02:15",
            },
        },
        {
            "sensores": {
                "temperatura": 28.8,
                "umidade": 80,
                "luminosidade": 800,
                "presenca": True,
                "movimento": True,
            },
            "dispositivos": {
                "luzes": [],
                "climatizacao": ["ar_condicionado", "ventilador"],
                "eletronicos": ["tv", "computador", "geladeira"],
                "seguranca": [
                    "camera_sala",
                    "camera_entrada",
                    "camera_quintal",
                    "sensor_porta_principal",
                ],
            },
            "configuracao": {
                "modo_economia": False,
                "temperatura_ideal": 24,
                "alarme_ativo": True,
                "horario": "14:45",
            },
        },
    ]

    regras = [
        # Regra 1: Controle automático de climatização
        {
            "apply": [
                "determinar_acao_clima",
                {"var": "sensores.temperatura"},
                {"var": "sensores.umidade"},
                {"var": "sensores.presenca"},
            ]
        },
        # Regra 2: Desligar luzes quando não há presença
        {
            "if": [
                {"!": [{"var": "sensores.presenca"}]},
                "desligar_luzes",
                "manter_luzes",
            ]
        },
        # Regra 3: Calcular consumo de energia
        {
            "apply": [
                "calcular_consumo_energia",
                {
                    "merge": [
                        {"var": "dispositivos.luzes"},
                        {"var": "dispositivos.climatizacao"},
                        {"var": "dispositivos.eletronicos"},
                    ]
                },
                1,
            ]
        },
        # Regra 4: Score de segurança
        {
            "apply": [
                "calcular_score_seguranca",
                [{"var": "dispositivos.seguranca.0"}],
                [{"var": "dispositivos.seguranca.1"}],
                {"var": "dispositivos.seguranca"},
                {"var": "configuracao.alarme_ativo"},
            ]
        },
        # Regra 5: Modo economia automático
        {
            "or": [
                {"var": "configuracao.modo_economia"},
                {
                    "and": [
                        {"!": [{"var": "sensores.presenca"}]},
                        {"!": [{"var": "sensores.movimento"}]},
                    ]
                },
                {
                    "and": [
                        {">": [{"var": "configuracao.horario"}, "22:00"]},
                        {"<": [{"var": "configuracao.horario"}, "06:00"]},
                    ]
                },
            ]
        },
    ]

    return TestScenario("IoT", regras, dados, funcoes)


def executar_cenario(cenario: TestScenario, num_execucoes: int = 1000):
    """Executa um cenário de teste"""
    print(f"\n🎯 Executando cenário: {cenario.nome}")
    print("-" * 50)

    sucessos = 0
    erros = 0
    tempo_total = 0
    resultados_amostra = []

    for i in range(num_execucoes):
        regra = random.choice(cenario.regras)
        dados = random.choice(cenario.dados)

        try:
            inicio = time.time()
            resultado = jsonLogic(regra, dados, cenario.funcoes)
            fim = time.time()

            tempo_execucao = fim - inicio
            tempo_total += tempo_execucao
            sucessos += 1

            # Coleta amostras dos primeiros resultados
            if i < 5:
                resultados_amostra.append(
                    {
                        "execucao": i + 1,
                        "resultado": resultado,
                        "tempo_ms": tempo_execucao * 1000,
                    }
                )

        except Exception as e:
            erros += 1
            if erros <= 3:
                print(f"   ❌ Erro na execução {i+1}: {e}")

    # Mostra resultados de amostra
    print("📊 Amostra de resultados:")
    for amostra in resultados_amostra:
        print(
            f"   Execução {amostra['execucao']}: {amostra['resultado']} ({amostra['tempo_ms']:.2f}ms)"
        )

    # Estatísticas
    print("\n📈 Estatísticas:")
    print(f"   Total de execuções: {num_execucoes}")
    print(f"   Sucessos: {sucessos}")
    print(f"   Erros: {erros}")
    print(f"   Taxa de sucesso: {(sucessos/num_execucoes*100):.1f}%")
    print(f"   Tempo médio: {(tempo_total/num_execucoes)*1000:.3f}ms")
    print(f"   Throughput: {num_execucoes/tempo_total:.0f} operações/s")

    return {
        "cenario": cenario.nome,
        "execucoes": num_execucoes,
        "sucessos": sucessos,
        "erros": erros,
        "tempo_total": tempo_total,
        "taxa_sucesso": (sucessos / num_execucoes * 100),
        "tempo_medio_ms": (tempo_total / num_execucoes) * 1000,
        "throughput": num_execucoes / tempo_total,
    }


def main():
    """Executa todos os cenários de teste"""
    print("🚀 TESTE MASSIVO DE CARGA - JSON LOGIC")
    print("=" * 60)
    print("Testando diferentes cenários de negócio com payloads variados")
    print("=" * 60)

    # Cria cenários
    cenarios = [
        criar_cenario_ecommerce(),
        criar_cenario_financeiro(),
        criar_cenario_iot(),
    ]

    resultados = []

    # Executa cada cenário
    for cenario in cenarios:
        resultado = executar_cenario(cenario, 2000)
        resultados.append(resultado)

    # Resumo geral
    print("\n" + "=" * 60)
    print("📊 RESUMO GERAL DOS TESTES")
    print("=" * 60)

    total_execucoes = sum(r["execucoes"] for r in resultados)
    total_sucessos = sum(r["sucessos"] for r in resultados)
    total_erros = sum(r["erros"] for r in resultados)
    total_tempo = sum(r["tempo_total"] for r in resultados)

    print(f"🎯 Total de execuções: {total_execucoes:,}")
    print(f"✅ Total de sucessos: {total_sucessos:,}")
    print(f"❌ Total de erros: {total_erros:,}")
    print(f"📈 Taxa de sucesso geral: {(total_sucessos/total_execucoes*100):.2f}%")
    print(f"⏱️  Tempo médio geral: {(total_tempo/total_execucoes)*1000:.3f}ms")
    print(f"🚀 Throughput geral: {total_execucoes/total_tempo:.0f} operações/s")

    print("\n📋 Resultados por cenário:")
    for resultado in resultados:
        print(
            f"   {resultado['cenario']}: {resultado['taxa_sucesso']:.1f}% sucesso, {resultado['tempo_medio_ms']:.2f}ms médio"
        )

    print("\n🎉 Teste massivo concluído!")
    print(f"💪 JSON Logic demonstrou robustez em {len(cenarios)} cenários diferentes")
    print(f"🔥 Performance média: {total_execucoes/total_tempo:.0f} operações/segundo")


if __name__ == "__main__":
    main()
