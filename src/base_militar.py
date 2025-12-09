import math
import random
from typing import TYPE_CHECKING, Dict, List, Optional

from src.classes import Entidade, Tecnologia
from src.economia import Economia

if TYPE_CHECKING:
    from src.classes import MonarcaAbsoluto
    from src.universo import WorldMap


# ===================== VEÍCulo DE COMBATE (Força Bélica e Mecha) =====================
class VeiculoDeCombate(Entidade):
    def __init__(
        self, nome: str, tipo_arma: str, base: "BaseMilitar", pos: tuple, alcance_max: int = 5
    ):
        super().__init__(nome, hp=500, pos=pos)
        self.tipo_arma = tipo_arma
        self.base_logistica = base
        self.municao = 10
        self.moral_tripulacao = 80
        self.alcance_max = alcance_max
        self.tipo_unidade = "Veiculo"

    def mover(self, dx: int, dy: int, world_map: "WorldMap"):
        """Movimento afetado pelo WorldMap e terreno."""
        nx, ny = self.pos[0] + dx, self.pos[1] + dy
        modificador = world_map.get_modificador_movimento(self.pos, self.tipo_unidade)

        if modificador >= 0.5:
            self.pos = (nx, ny)
            return (
                f"[{self.nome}]: Moveu para ({nx},{ny}) em "
                f"{world_map.get_terreno_nome(self.pos)}. Mod: {modificador:.1f}x"
            )
        return (
            f"[{self.nome}]: Bloqueado! Terreno "
            f"{world_map.get_terreno_nome(self.pos)} muito difícil."
        )

    def atirar(self, alvo: Entidade, world_map: "WorldMap"):
        """Ataque afetado por alcance e logística."""
        distancia = math.sqrt((self.pos[0] - alvo.pos[0]) ** 2 + (self.pos[1] - alvo.pos[1]) ** 2)

        if self.municao > 0 and distancia <= self.alcance_max:
            self.municao -= 1
            self.base_logistica.recursos["Munição"] = max(
                0, self.base_logistica.recursos.get("Munição", 0) - 1
            )

            dano_arma = random.randint(50, 80)
            alvo.hp = max(0, alvo.hp - dano_arma)

            return (
                f"💣 [{self.nome}]: Fogo! Dano {dano_arma} em {alvo.nome} "
                f"(Dist: {distancia:.1f}). HP Inimigo: {alvo.hp}"
            )

        if distancia > self.alcance_max:
            return f"[{self.nome}]: FALHA TÁTICA. " f"Alvo fora do alcance ({distancia:.1f})."
        return f"[{self.nome}]: FALHA LOGÍSTICA. Sem munição."


# ===================== BASE MILITAR (HUB & ESTRUTURAS) =====================
class ComponenteBase:
    def __init__(
        self, nome: str, consumo_mana: int, producao_recurso: Optional[Dict[str, int]] = None
    ):
        self.nome = nome
        self.consumo_mana = consumo_mana
        self.producao_recurso = producao_recurso if producao_recurso is not None else {}
        self.status = "OPERACIONAL"


class BaseMilitar:
    def __init__(self, nome, owner: "MonarcaAbsoluto", economia: Economia, pos):
        self.nome = nome
        self.owner = owner
        self.economia = economia
        self.recursos = self.economia.reservas
        self.tecnologia = Tecnologia()
        self.defesa_psiquica = 0.0  # Mitigação SSSS (0.0 a 0.5)
        self.componentes: List[ComponenteBase] = []
        self._inicializar_componentes()

    def _inicializar_componentes(self):
        self.componentes.append(ComponenteBase("Reator de Éter Ω", 100, {"eter": 500, "mana": 150}))
        self.componentes.append(
            ComponenteBase("Laboratório SSSS", 200, {"materia_escura_ssss": 50})
        )
        self.recursos["Munição"] = 50  # Adiciona Logística

    def ciclo_base(self):
        """Processa consumo e produção de recursos (Tycoon)."""
        consumo_total_mana = sum(
            c.consumo_mana for c in self.componentes if c.status == "OPERACIONAL"
        )
        producao_total = {}

        for comp in self.componentes:
            if comp.status == "OPERACIONAL":
                for recurso, quantidade in comp.producao_recurso.items():
                    producao_total[recurso] = producao_total.get(recurso, 0) + quantidade

        self.recursos["mana"] = self.recursos.get("mana", 0) - consumo_total_mana
        for recurso, quantidade in producao_total.items():
            self.recursos[recurso] = self.recursos.get(recurso, 0) + quantidade

    def aplicar_upgrade_psiquico(self):
        custo_ssss = 30
        if (
            "Campo Psíquico SSSS" in self.tecnologia.arvore
            and self.recursos.get("materia_escura_ssss", 0) >= custo_ssss
        ):
            self.recursos["materia_escura_ssss"] -= custo_ssss
            self.defesa_psiquica = 0.50
            print(
                "🛡️ [UPGRADE ATIVO]: Campo de Estabilidade Psíquica SSSS ativado! (50% de mitigação)"
            )
            return True
        return False
