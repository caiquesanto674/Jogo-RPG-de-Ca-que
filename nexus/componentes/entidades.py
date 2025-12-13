import logging
from typing import List

from nexus.utils.constants import confirmar


class Arma:
    """Definição de armas e seu poder de combate."""

    def __init__(self, nome: str, poder: int, tipo: str):
        self.nome, self.poder, self.tipo = nome, poder, tipo


class UnidadeCombate:
    """Unidade militar com moral e arsenal."""

    def __init__(
        self,
        nome: str,
        classe: str,
        moral: int = 80,
        armas: List[Arma] = None,
        hp: int = 100,
        atk: int = 10,
        defn: int = 5,
    ):
        self.nome, self.classe, self.moral = nome, classe, moral
        self.armas = armas if armas else []
        self.hp = hp
        self.atk = atk
        self.defn = defn
        self.level = 1
        self.exp = 0

    def poder_combate(self) -> int:
        """Calcula o poder total (ataque + armas)."""
        return self.atk + sum(a.poder for a in self.armas)

    def atacar(self, alvo: "UnidadeCombate"):
        dano = max(1, self.atk - alvo.defn)
        alvo.hp -= dano
        logging.info(f"[COMBATE] {self.nome} causou {dano} de dano em {alvo.nome}.")
        return dano

    def ganhar_exp(self, valor):
        self.exp += valor
        if self.exp >= 100 * self.level:
            self.level += 1
            self.exp = 0
            self.atk += 2
            self.hp += 10
            logging.info(f"[LEVEL UP] {self.nome} subiu para o nível {self.level}!")


class Inimigo(UnidadeCombate):
    def __init__(self, nome, level):
        super().__init__(nome, "Inimigo", hp=50 + level * 10, atk=5 + level * 2, defn=3 + level)
        self.level = level


class Guardiao:
    """Entidade semi-divina (Poderes Divinos/Sobrenaturais)."""

    def __init__(self, nome: str, poder_unico: str):
        self.nome = nome
        self.poder_unico = poder_unico
        self.atento = False

    def despertar(self):
        """Ativa o poder único do guardião."""
        if not self.atento:
            self.atento = True
            logging.info(confirmar("GUARDIAO", True))
