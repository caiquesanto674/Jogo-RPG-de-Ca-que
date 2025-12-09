# ai/cardinal.py
import random

class AICardinal:
    def __init__(self):
        self.nome = "CIEL ASCENDIDO"
        self.correcoes = 0
    def salvar_realidade(self, economia, player):
        if economia.reservas.get('comida',0) < 500 or economia.reservas.get('mana',0) < 300 or player.moral < 20:
            economia.reservas['comida'] = max(3000, economia.reservas.get('comida',0)+3000)
            economia.reservas['mana'] = max(1800, economia.reservas.get('mana',0)+1800)
            player.moral = 100.0
            self.correcoes += 1
            return True
        return False
