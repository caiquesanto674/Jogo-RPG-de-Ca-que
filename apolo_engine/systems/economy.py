# systems/economy.py
class Economia:
    def __init__(self):
        self.reservas = {'ouro':30000,'eter':5000,'mana':2500,'materia_escura_ssss':200}
    def ciclo_ganho(self):
        # consumo passivo
        self.reservas['mana'] -= 100
        self.reservas['eter'] += 50
