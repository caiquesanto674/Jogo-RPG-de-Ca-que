# world/worldmap.py
import random
class WorldMap:
    def __init__(self, width=30, height=30):
        self.width = width
        self.height = height
        self.grid = [[random.randint(0,3) for _ in range(height)] for _ in range(width)]
    def get_modificador_movimento(self, pos, tipo_unidade):
        x,y = pos
        if not (0<=x<self.width and 0<=y<self.height): return 0.0
        terreno = self.grid[x][y]
        mods = {'Veiculo': {0:1.0,1:0.7,2:0.5,3:0.2}, 'Personagem': {0:1.0,1:0.8,2:0.6,3:0.4}}
        return mods.get(tipo_unidade, {}).get(terreno, 1.0)
    def get_terreno_nome(self, pos):
        nomes = {0:"Planície",1:"Floresta",2:"Montanha",3:"Pântano"}
        x,y = pos
        if 0<=x<self.width and 0<=y<self.height:
            return nomes[self.grid[x][y]]
        return "Fora"
