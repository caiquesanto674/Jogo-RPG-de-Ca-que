import random
from typing import Optional
from src.constantes import CLASSES, RACAS

# ===================== ENTIDADES BASE, MONARCA E INIMIGO =====================
class Entidade:
    def __init__(self, nome: str, hp: int, pos: tuple):
        self.nome = nome
        self.hp = hp
        self.pos = pos
        self.energia = 100
        self.estado = 'neutro'
        self.inventario = []

class Personagem(Entidade):
    def __init__(self, nome, cargo='Jogador', raca=None, classe=None, base=None, pos=(0,0)):
        super().__init__(nome, hp=120 if cargo=='OWNER' else 100, pos=pos)
        self.raca = raca or random.choice(RACAS)
        self.classe = classe or random.choice(CLASSES)
        self.cargo = cargo
        self.base = base
        self.moral = 100.0 if cargo!='OWNER' else None # Moral só no Monarca
        self.humor = "neutro"

    def agir(self, acao: str, alvo: Optional[Entidade] = None):
        if acao == 'atacar' and alvo:
            dano = random.randint(15, 30)
            alvo.hp = max(0, alvo.hp - dano)
            return f"[{self.nome}] ataca {alvo.nome} e causa {dano} de dano! HP restante: {alvo.hp}"
        return f"{self.nome} executou ação: {acao}"

class MonarcaAbsoluto(Personagem):
    """Protagonista - Monarca Caíque (OWNER), com atributos de APOLO e Agony Overflow."""
    def __init__(self, nome: str, base: 'BaseMilitar'):
        super().__init__(nome, cargo="OWNER", raca="Humano", classe="Comandante", base=base)
        self.moral = 100.0
        self.indice_dimensional = 3.0
        self.harem = {"Luna": 100, "Calia Cardinal": 100, "Maria": 95}
        self.hp = 9999

    def ativar_volicao(self):
        """Mecânica Agony Overflow: A dor me torna mais forte (Evolução Reativa)."""
        if self.moral < 20:
            self.indice_dimensional += 0.5
            self.moral = 70
            print(f"\n⚡ AGONY OVERFLOW ATIVADO! NOVO ÍNDICE DIMENSIONAL: {self.indice_dimensional:.2f}")
            return True
        return False

class Inimigo(Personagem):
    """Inimigo de alto nível com Poder Psicológico e Sobrenatural."""
    def __init__(self, nome, cargo='Geral Inimigo', raca='Demônio', nivel_ameaca=65, poder_psicologico=True, pos=(0,0)):
        super().__init__(nome, cargo, raca, classe='Mago', pos=pos)
        self.hp = 150
        self.nivel_forca = nivel_ameaca
        self.poder_psicologico = poder_psicologico

    def usar_poder(self, alvo: MonarcaAbsoluto):
        """Ataca a Moral do Monarca, mitigado pela defesa SSSS da Base."""
        if self.poder_psicologico and alvo.cargo == 'OWNER' and alvo.base:
            dano_base = self.nivel_forca * 0.75
            defesa_pct = alvo.base.defesa_psiquica
            dano_final = dano_base * (1.0 - defesa_pct)

            alvo.moral = max(0, alvo.moral - dano_final)
            alvo.humor = "dominado_psicologicamente"

            print(f"⚠️ [ATAQUE PSÍQUICO]: {self.nome} usou Manipulação Mental.")
            print(f"   Mitigação SSSS: {defesa_pct*100:.0f}% | Dano de Moral Recebido: {dano_final:.1f}")
            return 'PSICOLOGICO'
        return 'IDLE'

# ===================== AI NPC (INTELIGÊNCIA DE SUPORTE AVANÇADA) =====================
class AI_NPC_Suporte(Personagem):
    def tomar_decisao_suporte(self, monarca: MonarcaAbsoluto, inimigo: Inimigo):
        """Delibera ações baseadas no estado do Monarca (Suporte Tático Inteligente)."""

        if monarca.moral < 40 and monarca.base and monarca.base.defesa_psiquica < 0.5:
             # Prioridade 1: Ativar defesa se a moral estiver baixa e a defesa inativa
             print(f"[{self.nome} - SUPORTE TÁTICO]: Moral baixa. Iniciando ativação do Campo Psíquico SSSS.")
             monarca.base.aplicar_upgrade_psiquico()
             return 'ATIVAR_DEFESA_PSÍQUICA'

        if monarca.moral < 50 and self.classe in ('Clérigo', 'Mago'):
            # Prioridade 2: Restauração de Moral
            monarca.moral = min(100, monarca.moral + random.randint(10, 20))
            print(f"[{self.nome} - SUPORTE]: Usando Sinergia de Vontade. Moral restaurada.")
            return 'RESTAURAR_MORAL'

        if inimigo and inimigo.hp > 0:
            return self.agir('atacar', inimigo)

        return 'IDLE'
