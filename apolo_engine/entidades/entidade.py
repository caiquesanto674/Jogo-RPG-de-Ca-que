# -*- coding: utf-8 -*-

from apolo_engine.entidades.inventario import Inventario
from apolo_engine.entidades.memoria import MemoriaIA
from apolo_engine.sistemas.motor_decisao import SistemaDecisaoFonte

class Entidade:
    """ Classe base para qualquer ser vivo no jogo (jogadores, inimigos, NPCs). """
    def __init__(self, nome, forca, vida):
        self.nome = nome
        self.forca = forca
        self.vida = vida
        self.inventario = Inventario()
        self.memoria = MemoriaIA()

    def atacar(self, outra_entidade, sistema_decisao: SistemaDecisaoFonte):
        """ Realiza uma ação de ataque contra outra entidade. """
        dano = sistema_decisao.calcular_dano(self.forca)
        print(f"  -> {self.nome} ataca {outra_entidade.nome} e causa {dano} de dano!")
        outra_entidade.vida -= dano
        outra_entidade.memoria.adicionar_evento_curto_prazo(f"{self.nome} atacou")

    def usar_pocao(self, sistema_decisao: SistemaDecisaoFonte):
        """ Usa uma poção do inventário para restaurar a vida. """
        pocao = next((item for item in self.inventario.itens if item.tipo == "pocao"), None)
        if pocao:
            cura = sistema_decisao.calcular_cura()
            self.vida += cura
            self.inventario.remover_item(pocao)
            print(f"  -> {self.nome} usa {pocao.nome} e recupera {cura} de vida. Vida atual: {self.vida}")
            self.memoria.adicionar_fato_longo_prazo("sabe_usar_pocao", True)
        else:
            print(f"  -> {self.nome} não tem poções para usar!")
