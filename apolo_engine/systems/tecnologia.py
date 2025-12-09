# apolo_engine/systems/tecnologia.py


class ArvoreTecnologia:
    """Gerencia a árvore de pesquisa, projetos ativos e bônus tecnológicos."""

    def __init__(self):
        self.pesquisas_desbloqueadas = {"ArmamentoNivel1": True}
        self.pesquisas_ativas = {}
        print("Árvore de Tecnologia Iniciada.")

    def iniciar_projeto(self, nome_projeto: str, custo_recursos: dict, tempo_base: int) -> bool:
        """Inicia um projeto de pesquisa se os recursos estiverem disponíveis."""
        # Lógica para verificar recursos (interagindo com SistemaEconomia)
        # ...
        if nome_projeto not in self.pesquisas_ativas:
            self.pesquisas_ativas[nome_projeto] = {"tempo_restante": tempo_base}
            return True
        return False

    def aplicar_bonus_tecnologico(self, entidade: object, projeto: str):
        """
        Aplica os bônus permanentes da tecnologia pesquisada a uma entidade
        (ex: aumento de dano em 10%).
        """
        if projeto in self.pesquisas_desbloqueadas:
            # ... aplica modificadores ...
            pass
