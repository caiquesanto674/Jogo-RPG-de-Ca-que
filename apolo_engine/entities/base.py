import uuid
from typing import List

from ..systems.economy import Economia
from ..systems.tecnologia import Tecnologia
from .unidade import UnidadeMilitar
from ..ai.comportamento import ComportamentoBase, EstadoIA


class BaseMilitar:
    # --- Constantes de Comportamento da IA para fácil balanceamento ---
    LIMIAR_SAUDE_DEFENSIVO = 50.0
    LIMIAR_RECURSO_METAL_EXPANSAO = 1500
    LIMIAR_RECURSO_COMBUSTIVEL_EXPANSAO = 1000
    NIVEL_BASE_PARA_PRIORIZAR_TECNOLOGIA = 3
    NIVEL_MAX_BIOTECNOLOGIA_PRIORITARIA = 5
    # ---

    def __init__(self, owner: str, local: str, economia: Economia, tecnologia: Tecnologia, nivel: int = 1):
        self.id = uuid.uuid4()
        self.owner = owner
        self.local = local
        self.nivel = nivel
        self.recursos = {"metal": 1000, "combustível": 500, "plasma": 120}
        self.economia = economia
        self.tecnologia = tecnologia
        self.unidades: List[UnidadeMilitar] = []
        self.saude_base = 100.0
        self.eficiencia_operacional = 100.0
        self.custo_subsistencia_base = {"metal": 20, "combustível": 10}
        self.comportamento = ComportamentoBase()

    def avaliar_cenario_e_decidir(self):
        """
        O cérebro da base. Avalia o estado e toma decisões estratégicas.
        """
        # --- Fase de Avaliação: Mudar de estado com base na situação ---
        if self.saude_base < self.LIMIAR_SAUDE_DEFENSIVO:
            self.comportamento.definir_estado(EstadoIA.DEFENSIVO)
        elif self.alerta_recursos_baixos() and self.comportamento.estado_atual != EstadoIA.DEFENSIVO:
            self.comportamento.definir_estado(EstadoIA.CONSERVADOR)
        elif (self.recursos["metal"] > self.LIMIAR_RECURSO_METAL_EXPANSAO and
              self.recursos["combustível"] > self.LIMIAR_RECURSO_COMBUSTIVEL_EXPANSAO):
             self.comportamento.definir_estado(EstadoIA.EXPANSIONISTA)

        # --- Fase de Ação: Executar ações com base no estado atual ---
        if self.comportamento.estado_atual == EstadoIA.EXPANSIONISTA:
            # Se a base for de nível alto, ela pode priorizar tecnologia
            if (self.nivel > self.NIVEL_BASE_PARA_PRIORIZAR_TECNOLOGIA and
                self.tecnologia.arvore.get("Biotecnologia", 1) < self.NIVEL_MAX_BIOTECNOLOGIA_PRIORITARIA):
                print(f"[IA DECISÃO] {self.local} priorizando avanço tecnológico em Biotecnologia.")
                self.tecnologia.pesquisar("Biotecnologia", self)
            else:
                print(f"[IA DECISÃO] {self.local} em modo expansionista, tentando upgrade.")
                self.expande(recurso_base="metal", valor_base=250 * self.nivel, custo_credito=500 * self.nivel)
        elif self.comportamento.estado_atual == EstadoIA.CONSERVADOR:
             print(f"[IA DECISÃO] {self.local} em modo conservador. Acumulando recursos.")
        elif self.comportamento.estado_atual == EstadoIA.DEFENSIVO:
             print(f"[IA DECISÃO] {self.local} em modo defensivo. Foco em recuperação.")

    def metabolismo_ciclo(self):
        """
        Simula o consumo de recursos para manutenção da base.
        A falha em suprir as necessidades afeta a saúde e eficiência.
        O custo é modificado pelo nível de Biotecnologia.
        """
        # A tecnologia de Biotecnologia reduz o custo de subsistência.
        nivel_biotec = self.tecnologia.arvore.get("Biotecnologia", 1)
        # Redução de 8% por nível, com um máximo de 80% de redução.
        fator_reducao = max(0.2, 1 - (nivel_biotec - 1) * 0.08)

        custo_atualizado = {
            recurso: int(custo * fator_reducao)
            for recurso, custo in self.custo_subsistencia_base.items()
        }

        consumo_total = {
            recurso: custo * self.nivel for recurso, custo in custo_atualizado.items()
        }

        recursos_suficientes = True
        for recurso, valor in consumo_total.items():
            if self.recursos.get(recurso, 0) < valor:
                recursos_suficientes = False
                break

        if recursos_suficientes:
            # LUZ: A base está saudável e bem suprida.
            for recurso, valor in consumo_total.items():
                self.recursos[recurso] -= valor
            # Recuperação gradual de saúde e eficiência se estiverem abaixo de 100
            self.saude_base = min(100.0, self.saude_base + 0.5)
            self.eficiencia_operacional = min(100.0, self.eficiencia_operacional + 0.2)
            print(f"[METABOLISMO] {self.local}: Subsistência OK. Saúde: {self.saude_base:.1f}, Eficiência: {self.eficiencia_operacional:.1f}")
        else:
            # ESCURIDÃO: A base está em crise de subsistência.
            print(f"[ALERTA] {self.local}: Falha na subsistência! Recursos insuficientes.")
            self.saude_base = max(0.0, self.saude_base - 5.0)
            self.eficiencia_operacional = max(10.0, self.eficiencia_operacional - 2.5)
            print(f"[METABOLISMO] {self.local}: Crise! Saúde: {self.saude_base:.1f}, Eficiência: {self.eficiencia_operacional:.1f}")

    def alerta_recursos_baixos(self) -> bool:
        """Verifica se os recursos estão perigosamente baixos."""
        limite_alerta = 5  # Alerta se os recursos forem < 5x o custo de um ciclo
        for recurso, custo in self.custo_subsistencia_base.items():
            if self.recursos.get(recurso, 0) < (custo * self.nivel * limite_alerta):
                print(f"[ALERTA] {self.local}: Níveis de {recurso} estão criticamente baixos!")
                return True
        return False

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
