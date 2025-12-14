# -*- coding: utf-8 -*-

from apolo_engine.entidades.entidade import Entidade

class Personagem(Entidade):
    """ Representa o jogador controlado por um humano. """
    def __init__(self, nome, forca, vida):
        super().__init__(nome, forca, vida)

class Inimigo(Entidade):
    """ Representa um adversário controlado pela IA. """
    def __init__(self, nome, forca, vida, assistente_ia=None):
        super().__init__(nome, forca, vida)
        self.assistente_ia = assistente_ia
