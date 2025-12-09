class SistemaAliados:
    def __init__(self, economia):
        self.economia = economia
        self.aliados = 0
        self.custo_alianca = 250

    def formar_alianca(self):
        if self.economia.recursos >= self.custo_alianca:
            self.economia.recursos -= self.custo_alianca
            self.aliados += 1
            return True
        return False

    def quebrar_alianca(self):
        if self.aliados > 0:
            self.aliados -= 1
            return True
        return False
