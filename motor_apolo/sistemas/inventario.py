# -*- coding: utf-8 -*-

class Item:
    """ Representa um item que pode ser armazenado no inventário. """
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo  # Ex: "arma", "pocao", "acessorio"

class Inventario:
    """ Gerencia a coleção de itens de uma entidade. """
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item: Item):
        self.itens.append(item)
        print(f"  -> {item.nome} foi adicionado ao inventário.")

    def remover_item(self, item: Item):
        self.itens.remove(item)
