import random


# ===================== WORLD MAP (Construção de Mundo Tático) =====================
class WorldMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # 0=Planície(rápido), 1=Floresta(lento, cobertura)
        # 2=Montanha(lento, alto alcance), 3=Pântano(muito lento)
        self.grid = [[random.randint(0, 3) for _ in range(height)] for _ in range(width)]

    def get_modificador_movimento(self, pos: tuple, tipo_unidade: str) -> float:
        """Calcula o modificador de velocidade baseado no terreno e no tipo de unidade."""
        x, y = pos
        if not (0 <= x < self.width and 0 <= y < self.height):
            return 0.0

        terreno = self.grid[x][y]
        modificadores = {
            "Veiculo": {0: 1.0, 1: 0.7, 2: 0.5, 3: 0.2},
            "Personagem": {0: 1.0, 1: 0.8, 2: 0.6, 3: 0.4},
        }
        return modificadores.get(tipo_unidade, {}).get(terreno, 1.0)

    def get_terreno_nome(self, pos: tuple) -> str:
        nomes = {0: "Planície", 1: "Floresta", 2: "Montanha", 3: "Pântano"}
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return nomes.get(self.grid[x][y], "Desconhecido")
        return "Fora do Mapa"
