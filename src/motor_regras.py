from src.lib.json_logic import jsonLogic
from src.regras import REGRAS_VALIDACAO, REGRA_PROCESSAMENTO
from src.acoes import ACOES_DISPONIVEIS, logar_erro_validacao


class MotorDeRegrasCustom:
    def __init__(self):
        print("Motor de Regras Customizado inicializado.")

    def _validar_dados(self, dados):
        """Executa as regras de validação."""
        print("\n--- FASE DE VALIDAÇÃO ---")
        for regra in REGRAS_VALIDACAO:
            resultado = jsonLogic(regra, dados)
            if resultado is not None:
                # Se qualquer regra de validação retornar um erro, paramos.
                print(f"Falha na validação: {resultado}")
                return resultado
        print("Validação concluída com sucesso.")
        return None

    def _processar_regras(self, dados):
        """Executa a regra principal de processamento."""
        print("\n--- FASE DE PROCESSAMENTO ---")
        decisao = jsonLogic(REGRA_PROCESSAMENTO, dados)
        print(f"Resultado da avaliação da regra: '{decisao}'")
        return decisao

    def _executar_acao(self, decisao, dados):
        """Chama a ação Python correspondente à decisão."""
        print("\n--- FASE DE AÇÃO ---")
        # Procura a ação correspondente no dicionário
        acao = ACOES_DISPONIVEIS.get(decisao)
        if callable(acao):
            acao(dados)
        else:
            print(f"Nenhuma ação definida para a decisão '{decisao}'.")

    def executar(self, dados_solicitacao):
        """Orquestra todo o processo de decisão."""
        print(
            f"\n>>>> INICIANDO EXECUÇÃO PARA SOLICITAÇÃO ID: {dados_solicitacao['id']} <<<<"
        )

        # 1. Avaliar (Validação)
        erro_validacao = self._validar_dados(dados_solicitacao)

        # 2. Decidir / Agir (sobre a validação)
        if erro_validacao:
            logar_erro_validacao(dados_solicitacao, erro_validacao)
            print("Execução interrompida devido a erro de validação.")
            return dados_solicitacao

        # 1. Avaliar (Processamento)
        decisao_final = self._processar_regras(dados_solicitacao)

        # 3. Agir (sobre o processamento)
        self._executar_acao(decisao_final, dados_solicitacao)

        print(
            f"\n>>>> EXECUÇÃO CONCLUÍDA PARA SOLICITAÇÃO ID: {dados_solicitacao['id']} <<<<"
        )
        return dados_solicitacao
