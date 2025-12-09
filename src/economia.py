import random


# ===================== ECONOMIA & TECNologia (Tycoon + SSSS) =====================
class Economia:
    def __init__(self):
        self.reservas = {
            "ouro_conceitual": 30,
            "materia_escura_ssss": 200,
            "eter": 2000,
            "mana": 2500,
            "comida": 3500,
            "consciencia_remanescente": 20000,
        }

    def ciclo_ganho(self):
        """Processa consumo e ganhos passivos."""
        self.reservas["comida"] -= random.randint(120, 350)
        self.reservas["mana"] -= random.randint(50, 140)
