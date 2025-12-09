# apolo_engine/entities/base_militar.py

from apolo_engine.systems.economia import SistemaEconomia


class BaseMilitar:
    """
    Representa uma Base Militar, um local estratégico, de produção e comando.
    """

    def __init__(
        self, nome: str, nivel_defesa: int, multiplicador_producao: float, economia: SistemaEconomia
    ):
        self.nome = nome
        self.nivel_defesa = nivel_defesa
        self.producao_bonus = multiplicador_producao
        self.aliados_estacionados = []
        self._economia = economia
        print(f"Base Militar '{self.nome}' estabelecida.")

    # Funções de Comportamento/Confirmação
    def _frase_confirmacao(self, acao: str):
        """Frases de confirmação de comportamento (simulando resposta militar/AI)."""
        frases = {
            "reforco": (
                f"Comando {self.nome} recebido. Solicitação de reforço enviada. "
                "Status: Prontidão Máxima."
            ),
            "producao": (
                f"Protocolos de Produção em {self.nome} iniciados. " "Coletando Minerais Raros."
            ),
            "defesa": (
                f"Alerta de Defesa Nível {self.nivel_defesa} ativado. " "Posições mantidas."
            ),
        }
        print(
            "[COMANDO]: " f"{frases.get(acao, 'Ação desconhecida. Aguardando novos parâmetros.')}"
        )

    def iniciar_producao_recursos(self):
        """Inicia a produção de recursos na base, integrando com a Economia."""
        aumento = self._economia.gerar_recursos("MineraisRaros", self.producao_bonus)
        self._frase_confirmacao("producao")
        print(f"Base {self.nome} produziu {aumento} Minerais Raros.")

    def solicitar_reforcos(self, unidade_nome: str, quantidade: int):
        """Simula o envio de uma solicitação de reforço."""
        self._frase_confirmacao("reforco")
        # Lógica para adicionar unidades (Entidades) à base (não detalhada aqui)
        pass

    def acionar_defesa(self):
        """Ativa protocolos de defesa e anuncia o status."""
        self._frase_confirmacao("defesa")
        # Lógica de combate defensivo
        pass
