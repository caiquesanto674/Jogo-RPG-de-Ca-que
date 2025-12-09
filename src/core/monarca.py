# src/core/monarca.py

class MonarcaAbsoluto:
    def __init__(self, nome):
        self.nome = nome
        self.cargo = "OWNER / MONARCA"
        self.moral = 100.0
        self.indice_dimensional = 3.0
        self.harem = {"Luna": 100, "Seo-Yeon": 99, "Calia Cardinal": 100, "Maria": 95}
        self.pontos_quiz = 0
        self.patente = "Comandante"

    def promover(self):
        patentes = ["Comandante", "General", "Marechal", "Monarca Estelar"]
        idx = min(self.pontos_quiz // 2, len(patentes) - 1)
        self.patente = patentes[idx]

    def ativar_volicao(self):
        if self.moral > 20:
            self.moral -= 25
            print(f"\n>> VOLIÇÃO ABSOLUTA ATIVADA — A REALIDADE SE DOBRA À VONTADE DO MONARCA.")
            return True
        print("\n>> AGONIA PROFUNDA — A DOR ME TORNA MAIS FORTE. <<")
        self.indice_dimensional += 0.5
        self.moral = 80
        return True

    def sinergia_harem(self):
        bonus = len(self.harem) * 15
        self.moral = min(100, self.moral + bonus)
        print(f">> SINERGIA DE SUBMISSÃO: {len(self.harem)} almas servem ao Monarca. Moral restaurada (+{bonus}).")
