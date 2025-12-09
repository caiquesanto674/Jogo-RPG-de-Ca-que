import random
from typing import TYPE_CHECKING

from src.classes import Personagem

if TYPE_CHECKING:
    from src.classes import Inimigo, MonarcaAbsoluto
    from src.economia import Economia


# ===================== AI CARDINAL — CIEL ASCENDIDO (Deus Ex Machina) =====================
class AICardinal:
    def __init__(self):
        self.nome = "CIEL ASCENDIDO"
        self.correcoes = 0

    def salvar_realidade(self, protagonista: "MonarcaAbsoluto", economia: "Economia"):
        """Monitora e intervém para evitar o colapso de recursos e moral."""
        if (
            economia.reservas.get("comida", 0) < 500
            or economia.reservas.get("mana", 0) < 300
            or protagonista.moral < 20
        ):
            print("\nAI CARDINAL: REALIDADE EM COLAPSO. INTERVENÇÃO DIVINA EXECUTADA.")
            economia.reservas["comida"] = max(3000, economia.reservas.get("comida", 0) + 5000)
            protagonista.moral = 100.0
            self.correcoes += 1


# ===================== AI NPC (INTELIGÊNCIA DE SUPORTE) =====================
class AI_NPC_Suporte(Personagem):
    def tomar_decisao_suporte(self, monarca: "MonarcaAbsoluto", inimigo: "Inimigo"):
        """Delibera ações de suporte tático (Ex: Calia Cardinal)."""

        if monarca.moral < 40 and monarca.base and monarca.base.defesa_psiquica < 0.5:
            # Prioridade: Ativar defesa psíquica para mitigar ataque inimigo
            monarca.base.aplicar_upgrade_psiquico()
            return "ATIVAR_DEFESA_PSÍQUICA"

        if monarca.moral < 50:
            # Restauração de Moral
            monarca.moral = min(100, monarca.moral + random.randint(10, 20))
            return "RESTAURAR_MORAL"

        if inimigo and inimigo.hp > 0:
            return self.agir("atacar", inimigo)

        return "IDLE"
