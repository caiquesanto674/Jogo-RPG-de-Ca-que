# src/events/mundo.py

import random
from src.utils.log_protocol import LogSistema

class MundoSimulado:
    def __init__(self, log: LogSistema):
        self.log = log
        self.faccoes = [f"Clã Estelar {i}" for i in range(3)]
        self.conflitos = 0

    def simular_turno(self):
        if random.random() < 0.4:
            f1, f2 = random.sample(self.faccoes, 2)
            tipo_conflito = random.choice(["território", "recursos", "ideologia"])
            self.log.registrar("MUNDO", "Simulação de Fundo", f"Novo conflito entre {f1} e {f2} por {tipo_conflito}.")
            self.conflitos += 1
