# src/systems/economia.py

import random

class EconomiaUnificada:
    def __init__(self):
        self.reservas = {
            'creditos': 50000, 'ouro': 8000, 'mana': 5000, 'comida': 10000, 'aço': 5000,
            'materia_escura_ssss': 250, 'eter_puro': 2200
        }

    def ciclo(self):
        self.reservas['creditos'] += random.randint(1000, 2500)
        self.reservas['ouro'] += random.randint(300, 600)
        self.reservas['comida'] -= random.randint(150, 400)
        self.reservas['mana'] -= random.randint(100, 250)
        if random.random() < 0.25:
            bonus_materia = random.randint(10, 25)
            self.reservas['materia_escura_ssss'] += bonus_materia
            print(f"[ECONOMIA] Matéria Escura SSSS cristalizada do vácuo (+{bonus_materia}).")

    def transferir(self, valor: int, destino: str) -> bool:
        if valor <= self.reservas['creditos']:
            self.reservas['creditos'] -= valor
            return True
        return False
