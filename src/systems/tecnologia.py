# src/systems/tecnologia.py

from typing import Dict, List

class Tecnologia:
    def __init__(self):
        self.arvore: Dict[str, int] = {'IA': 1, 'Fusão': 0, 'Plasma': 1, 'Biotecnologia': 0}
        self.descobertas: List[str] = []

    def pesquisar(self, ramo: str):
        if ramo in self.arvore:
            self.arvore[ramo] += 1
            self.descobertas.append(ramo)
            print(f"[TECNOLOGIA] Ramo '{ramo}' evoluído para nível {self.arvore[ramo]}.")
