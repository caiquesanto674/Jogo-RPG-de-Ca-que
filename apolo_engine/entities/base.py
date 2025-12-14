import uuid
from typing import List
from enum import Enum, auto

# AGENT-DEFINED: Added Tecnologia import for subsistence calculation
from ..systems.tecnologia import Tecnologia
from ..systems.economy import Economia
from .unidade import UnidadeMilitar

# AGENT-DEFINED: Added EstadoIA enum for the base's AI state machine
class EstadoIA(Enum):
    """Define os estados comportamentais da IA da base."""
    CONSERVADOR = auto()
    EXPANSIONISTA = auto()
    DEFENSIVO = auto()

class BaseMilitar:
    def __init__(self, owner: str, local: str, economia: Economia, tecnologia: Tecnologia, nivel: int = 1):
        self.id = uuid.uuid4()
        self.owner = owner
        self.local = local
        self.nivel = nivel
        self.recursos = {"metal": 1000, "combustível": 500, "plasma": 120}
        self.economia = economia
        # AGENT-DEFINED: Added tecnologia reference for dynamic subsistence cost
        self.tecnologia = tecnologia
        self.unidades: List[UnidadeMilitar] = []

        # AGENT-DEFINED: Added new attributes for subsistence and AI
        self.saude_base = 100
        self.eficiencia_operacional = 1.0  # 100%
        # AGENT-DEFINED: Dynamic subsistence cost based on base level
        self.custo_subsistencia = {"metal": 50 * nivel, "combustível": 25 * nivel}
        self.estado_ia = EstadoIA.CONSERVADOR

    def expande(self, recurso_base: str, valor_base: int, custo_credito: int) -> bool:
        if (
            self.recursos.get(recurso_base, 0) >= valor_base
            and self.economia.reserva >= custo_credito
        ):
            self.recursos[recurso_base] -= valor_base
            self.economia.transferir(custo_credito, f"Expansão {self.local}")
            self.nivel += 1
            print(f"[BASE] Upgrade: {self.local} -> Nível {self.nivel}")
            return True
        print("[FALHA] Recursos ou Créditos insuficientes.")
        return False

    # AGENT-DEFINED: New method for subsistence
    def metabolismo_ciclo(self):
        """
        Simula o consumo de recursos para manutenção da base.
        Falhas na subsistência afetam a saúde e eficiência.
        """
        # AGENT-DEFINED: Technology reduces subsistence cost
        modificador_tec = 1.0 - (0.05 * self.tecnologia.arvore.get("IA", 0))
        custo_real = {k: int(v * modificador_tec) for k, v in self.custo_subsistencia.items()}

        recursos_suficientes = True
        for recurso, valor in custo_real.items():
            if self.recursos.get(recurso, 0) < valor:
                recursos_suficientes = False
                break

        if recursos_suficientes:
            for recurso, valor in custo_real.items():
                self.recursos[recurso] -= valor
            self.saude_base = min(100, self.saude_base + 5)
            self.eficiencia_operacional = min(1.0, self.eficiencia_operacional + 0.05)
            print(f"[{self.local}] Subsistência OK. Saúde: {self.saude_base}, Eficiência: {self.eficiencia_operacional:.2f}")
        else:
            self.saude_base = max(0, self.saude_base - 10)
            self.eficiencia_operacional = max(0.1, self.eficiencia_operacional - 0.1)
            print(f"[ALERTA] Falha na subsistência em {self.local}! Saúde: {self.saude_base}, Eficiência: {self.eficiencia_operacional:.2f}")

    # AGENT-DEFINED: New method for AI decision making
    def avaliar_cenario_e_decidir(self):
        """
        A IA da base toma decisões com base em seu estado interno.
        """
        if self.saude_base < 50 or self.eficiencia_operacional < 0.5:
            self.estado_ia = EstadoIA.DEFENSIVO
            print(f"[{self.local}] IA -> Estado DEFENSIVO: Foco em reparos e sobrevivência.")
        elif self.recursos['metal'] > 1500 and self.recursos['combustível'] > 1000:
            self.estado_ia = EstadoIA.EXPANSIONISTA
            print(f"[{self.local}] IA -> Estado EXPANSIONISTA: Pronta para expandir.")
            # AGENT-DEFINED: AI automatically attempts to expand
            self.expande("metal", 500, 5000)
        else:
            self.estado_ia = EstadoIA.CONSERVADOR
            print(f"[{self.local}] IA -> Estado CONSERVADOR: Acumulando recursos.")
