import logging
import random

from nexus.componentes.entidades import UnidadeCombate


class Missao:
    def __init__(self, nome, dificuldade):
        self.nome = nome
        self.dificuldade = dificuldade
        self.recompensa = dificuldade * 25
        self.status = "pendente"

    def executar(self, personagem: UnidadeCombate):
        chance = personagem.level * random.uniform(0.5, 1.5)
        if chance >= self.dificuldade:
            personagem.ganhar_exp(self.recompensa)
            logging.info(f"[MISSÃO] {personagem.nome} completou '{self.nome}'.")
            self.status = "concluída"
            return True
        else:
            personagem.hp -= 10
            logging.info(f"[MISSÃO] {personagem.nome} falhou em '{self.nome}'.")
            self.status = "falhou"
            return False
