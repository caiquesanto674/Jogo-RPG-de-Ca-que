# -*- coding: utf-8 -*-

from .item import Item

class Inventario:
    """ Gerencia a coleção de itens de uma entidade. """
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item: Item):
        self.itens.append(item)
        print(f"  -> {item.nome} foi adicionado ao inventário.")

    def remover_item(self, item: Item):
        self.itens.remove(item)
