import random
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from src.base_militar import BaseMilitar


class Tecnologia:
    def __init__(self):
        self.nivel = 1
        self.arvore = []

    def pesquisar(self, nome: str, custo: Dict[str, int], base_militar: "BaseMilitar"):
        """Pesquisa tecnologia, desbloqueando upgrades bélicos/psíquicos."""
        if all(base_militar.recursos.get(res, 0) >= qtd for res, qtd in custo.items()):
            for res, qtd in custo.items():
                base_militar.recursos[res] -= qtd
            self.nivel += 1
            self.arvore.append(nome)
            print(f"🔬 Tec. pesquisada: {nome} | Nível {self.nivel}")
            return True
        return False


# ===================== ENTIDADES (RPG) =====================
class Entidade:
    def __init__(self, nome: str, hp: int, pos: tuple):
        self.nome = nome
        self.hp = hp
        self.pos = pos
        self.inventario = []


class Personagem(Entidade):
    def __init__(self, nome, cargo="Jogador", raca="Humano", classe="Guerreiro", base=None):
        super().__init__(nome, hp=100, pos=(0, 0))
        self.cargo = cargo
        self.moral = 100.0 if cargo != "OWNER" else None
        self.humor = "neutro"
        self.base = base

    def agir(self, acao: str, alvo: Optional[Entidade] = None):
        """Executa ações básicas de combate ou interação."""
        if acao == "atacar" and alvo:
            dano = random.randint(15, 30)
            alvo.hp = max(0, alvo.hp - dano)
            return f"[{self.nome}] ataca {alvo.nome} e causa {dano} de dano!"
        return f"{self.nome} executou ação: {acao}"


class MonarcaAbsoluto(Personagem):
    """Protagonista - Monarca Caíque (OWNER), com Poder Psicológico e Hierarquia."""

    def __init__(self, nome: str, base: "BaseMilitar"):
        super().__init__(nome, cargo="OWNER", base=base)
        self.moral = 100.0
        self.indice_dimensional = 3.0
        self.hp = 9999
        self.ativacao_overflow = False

    def ativar_volicao(self):
        """Mecânica Agony Overflow: Evolução Reativa por dano psicológico."""
        if self.moral < 20 and not self.ativacao_overflow:
            self.indice_dimensional += 0.5
            self.moral = 70
            self.ativacao_overflow = True
            print(
                (
                    "\n⚡ AGONY OVERFLOW ATIVADO! NOVO ÍNDICE DIMENSIONAL: "
                    f"{self.indice_dimensional:.2f}"
                )
            )
            return True
        return False


class Inimigo(Personagem):
    """Inimigo de alto nível com Poder Psicológico."""

    def __init__(self, nome, nivel_ameaca=90, poder_psicologico=True, pos=(10, 10)):
        super().__init__(nome, cargo="Geral Inimigo", raca="Demônio", classe="Mago")
        self.hp = 150
        self.nivel_forca = nivel_ameaca
        self.poder_psicologico = poder_psicologico
        self.pos = pos

    def usar_poder(self, alvo: MonarcaAbsoluto):
        """Ataca a Moral do Monarca, mitigado pela defesa SSSS da Base."""
        if self.poder_psicologico and alvo.base:
            dano_base = self.nivel_forca * 0.75
            defesa_pct = alvo.base.defesa_psiquica
            dano_final = dano_base * (1.0 - defesa_pct)

            alvo.moral = max(0, alvo.moral - dano_final)
            alvo.humor = "dominado_psicologicamente"

            print(
                (
                    f"⚠️ [ATAQUE PSÍQUICO]: {self.nome} usou Manipulação Mental. "
                    f"Moral Monarca: {alvo.moral:.1f}"
                )
            )
            return "PSICOLOGICO"
        return "IDLE"
