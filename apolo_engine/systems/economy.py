from datetime import datetime


class Economia:
    def __init__(self, reserva=100000):
        self.reserva = reserva
        self.transacoes = []
        self.recursos_locais = {"metal": 2000, "combustivel": 1000, "plasma": 500}

    def transferir(self, valor: int, destino: str) -> bool:
        if valor <= self.reserva:
            self.reserva -= valor
            self.transacoes.append(
                {"destino": destino, "valor": valor, "timestamp": datetime.now()}
            )
            return True
        return False
