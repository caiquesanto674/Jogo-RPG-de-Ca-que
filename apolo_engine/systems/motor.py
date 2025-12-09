# apolo_engine/systems/motor.py

from apolo_engine.ai.npc import AI_NPC
from apolo_engine.entities.base_militar import BaseMilitar
from apolo_engine.systems.economia import SistemaEconomia
from apolo_engine.systems.tecnologia import ArvoreTecnologia


class MotorApolo:
    """
    O motor principal do jogo, responsável por orquestrar todos os sistemas.
    """

    def __init__(self):
        print("Iniciando Motor Apolo...")
        self.economia = SistemaEconomia()
        self.tecnologia = ArvoreTecnologia()
        self.base_principal = BaseMilitar(
            nome="Arcanum Prime",
            nivel_defesa=10,
            multiplicador_producao=1.5,
            economia=self.economia,
        )
        self.npc_guardiao = AI_NPC(nome="NexusGuard", arvore_tecnologia=self.tecnologia)
        self.turno = 0
        print("Motor Apolo iniciado com sucesso.")

    def executar_turno(self):
        """Executa um único turno do jogo."""
        self.turno += 1
        print(f"\\n--- TURNO {self.turno} ---")

        # Lógica do turno
        self.base_principal.iniciar_producao_recursos()
        acao_npc = self.npc_guardiao.decidir_acao_combate(alvo={})  # Alvo mockado

        print(f"Ação do {self.npc_guardiao.nome}: {acao_npc}")
        print(f"Recursos Atuais: {self.economia.recursos}")


def iniciar_jogo():
    """Função principal para inicializar e rodar o jogo."""
    motor = MotorApolo()

    # Loop de jogo simples para demonstração
    for _ in range(3):
        motor.executar_turno()
