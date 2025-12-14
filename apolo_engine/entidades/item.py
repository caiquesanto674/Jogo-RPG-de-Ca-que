# -*- coding: utf-8 -*-

class Item:
    """ Representa um item que pode ser armazenado no inventário. """
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo  # Ex: "arma", "pocao", "acessorio"
