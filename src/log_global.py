from datetime import datetime

class LogGlobal:
    def __init__(self): self.registros = []
    def registrar(self, evento, args): self.registros.append((datetime.now(), evento, args))
