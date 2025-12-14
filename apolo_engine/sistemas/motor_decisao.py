# -*- coding: utf-8 -*-

import random

class SistemaDecisaoFonte:
    """ Centraliza todas as regras e cálculos do jogo (o 'S.D.F'). """
    def __init__(self):
        self.regras = {
            "dano_base": 10,
            "modificador_forca": 1.5,
            "cura_base_pocao": 20
        }

    def calcular_dano(self, forca):
        """ Calcula o dano de um ataque com base na força da entidade. """
        return self.regras["dano_base"] + (forca * self.regras["modificador_forca"])

    def calcular_cura(self):
        """ Calcula a quantidade de vida que uma poção restaura. """
        return self.regras["cura_base_pocao"] + random.randint(0, 10)
