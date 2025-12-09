# src/systems/unidades.py

from typing import List
from src.systems.tecnologia import Tecnologia

class Arma:
    def __init__(self, nome: str, poder: int, tipo: str):
        self.nome, self.poder, self.tipo = nome, poder, tipo

class UnidadeMilitar:
    def __init__(self, nome: str, classe: str, forca: int, armas: List[Arma] = None, tech: 'Tecnologia' = None, poder_psicologico: str = None, aliados_proximos: int = 0):
        self.nome, self.classe, self.forca = nome, classe, forca
        self.armas = armas if armas else []
        self.tech = tech
        self.poder_psicologico = poder_psicologico
        self.aliados_proximos = aliados_proximos
        self.moral = 100

    def poder_combate(self) -> float:
        bonus_tech = 1.0
        if self.tech:
            if self.classe in ['tanque', 'mecha', 'drone'] and self.tech.arvore.get('Plasma', 0) > 1:
                bonus_tech += self.tech.arvore['Plasma'] * 0.15
            if self.tech.arvore.get('IA', 0) > 1:
                bonus_tech += self.tech.arvore['IA'] * 0.1
        bonus_psico = (self.aliados_proximos if self.poder_psicologico == 'Comando' else 0) * 0.25
        bonus_alianca = self.aliados_proximos * 5
        return self.forca * bonus_tech * (self.moral / 100) + bonus_psico + bonus_alianca
