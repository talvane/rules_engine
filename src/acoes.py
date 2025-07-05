# file: acoes.py

def aprovar_solicitacao(dados):
    print(f"AÇÃO EXECUTADA: Solicitação {dados['id']} APROVADA.")
    dados['status_final'] = 'Aprovado'

def recusar_solicitacao(dados):
    print(f"AÇÃO EXECUTADA: Solicitação {dados['id']} RECUSADA.")
    dados['status_final'] = 'Recusado'

def enviar_para_analise_manual(dados):
    print(f"AÇÃO EXECUTADA: Solicitação {dados['id']} enviada para ANÁLISE MANUAL.")
    dados['status_final'] = 'Análise Manual'

def logar_erro_validacao(dados, erro):
    print(f"AÇÃO EXECUTADA: Erro de validação na solicitação {dados['id']}: {erro}")
    dados['status_final'] = 'Erro de Validação'
    dados['detalhe_erro'] = erro

# Mapeia os resultados das regras para as funções de ação
ACOES_DISPONIVEIS = {
    "APROVADO": aprovar_solicitacao,
    "RECUSADO": recusar_solicitacao,
    "ANALISE_MANUAL": enviar_para_analise_manual,
}