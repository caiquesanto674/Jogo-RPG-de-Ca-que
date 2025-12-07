# -*- coding: utf-8 -*-
"""
Este módulo contém os testes automatizados para o `rpg_game.py`.
Os testes cobrem as principais funcionalidades do jogo, como combate,
gerenciamento de inventário e lógica da IA.
"""

import unittest
from unittest.mock import MagicMock
from rpg_game import (
    SistemaDecisaoFonte,
    Item,
    Inventario,
    Entidade,
    Personagem,
    Inimigo,
    AssistenteReforco,
)

class TestSistemaDecisaoFonte(unittest.TestCase):
    """Testes para a classe SistemaDecisaoFonte."""

    def setUp(self):
        """Configura um S.D.F. para ser usado em todos os testes."""
        self.sdf = SistemaDecisaoFonte()

    def test_calcular_dano(self):
        """Verifica se o cálculo de dano está correto."""
        forca = 10
        dano_esperado = 10 + (10 * 1.5)  # dano_base + (forca * modificador_forca)
        self.assertEqual(self.sdf.calcular_dano(forca), dano_esperado)

    def test_calcular_cura(self):
        """Verifica se o cálculo de cura está dentro da faixa esperada."""
        cura_minima = 20  # cura_base_pocao
        cura_maxima = 30  # cura_base_pocao + 10
        cura_calculada = self.sdf.calcular_cura()
        self.assertTrue(cura_minima <= cura_calculada <= cura_maxima)

class TestInventario(unittest.TestCase):
    """Testes para a classe Inventario."""

    def setUp(self):
        """Configura um inventário e um item para os testes."""
        self.inventario = Inventario()
        self.item = Item("Poção", "pocao")

    def test_adicionar_item(self):
        """Verifica se um item é adicionado corretamente ao inventário."""
        self.inventario.adicionar_item(self.item)
        self.assertIn(self.item, self.inventario.itens)

    def test_remover_item(self):
        """Verifica se um item é removido corretamente do inventário."""
        self.inventario.adicionar_item(self.item)
        self.inventario.remover_item(self.item)
        self.assertNotIn(self.item, self.inventario.itens)

class TestEntidade(unittest.TestCase):
    """Testes para a classe Entidade."""

    def setUp(self):
        """Configura entidades e um S.D.F. para os testes."""
        self.sdf = SistemaDecisaoFonte()
        self.jogador = Personagem("Herói", 10, 100)
        self.inimigo = Inimigo("Ogro", 5, 80)

    def test_atacar(self):
        """Verifica se o ataque reduz a vida do alvo corretamente."""
        vida_inicial = self.inimigo.vida
        dano_esperado = self.sdf.calcular_dano(self.jogador.forca)

        self.jogador.atacar(self.inimigo, self.sdf)

        self.assertEqual(self.inimigo.vida, vida_inicial - dano_esperado)
        self.assertIn("Herói atacou", self.inimigo.memoria.memoria_curto_prazo)

    def test_usar_pocao_com_sucesso(self):
        """Verifica se usar uma poção aumenta a vida e remove o item."""
        pocao = Item("Poção de Cura", "pocao")
        self.jogador.inventario.adicionar_item(pocao)
        self.jogador.vida = 50

        self.jogador.usar_pocao(self.sdf)

        self.assertGreater(self.jogador.vida, 50)
        self.assertNotIn(pocao, self.jogador.inventario.itens)
        self.assertTrue(self.jogador.memoria.memoria_longo_prazo.get("sabe_usar_pocao"))

    def test_usar_pocao_sem_pocao(self):
        """Verifica o comportamento ao tentar usar uma poção sem tê-la."""
        vida_inicial = self.jogador.vida
        self.jogador.usar_pocao(self.sdf)
        self.assertEqual(self.jogador.vida, vida_inicial)

class TestAssistenteReforco(unittest.TestCase):
    """Testes para a IA de Reforço."""

    def setUp(self):
        """Configura as entidades e a IA para os testes."""
        self.ia = AssistenteReforco()
        self.jogador = Personagem("Herói", 10, 100)
        self.inimigo = Inimigo("Ogro", 5, 80)

    def test_decisao_atacar_quando_vida_alta(self):
        """Verifica se a IA decide atacar quando a vida do inimigo está alta."""
        decisao = self.ia.tomar_decisao_combate(self.inimigo, self.jogador)
        self.assertEqual(decisao, "atacar")

    def test_decisao_usar_pocao_quando_vida_baixa(self):
        """Verifica se a IA decide usar poção com vida baixa e com poção no inventário."""
        self.inimigo.vida = 20
        self.inimigo.inventario.adicionar_item(Item("Poção", "pocao"))
        decisao = self.ia.tomar_decisao_combate(self.inimigo, self.jogador)
        self.assertEqual(decisao, "usar pocao")

    def test_decisao_atacar_com_vida_baixa_mas_sem_pocao(self):
        """Verifica se a IA ataca com vida baixa se não tiver poção."""
        self.inimigo.vida = 20
        decisao = self.ia.tomar_decisao_combate(self.inimigo, self.jogador)
        self.assertEqual(decisao, "atacar")

    def test_decisao_prioriza_ataque_se_jogador_pode_curar(self):
        """Verifica se a IA foca no ataque se o jogador já demonstrou saber se curar."""
        self.jogador.memoria.adicionar_fato_longo_prazo("sabe_usar_pocao", True)
        self.inimigo.vida = 20
        self.inimigo.inventario.adicionar_item(Item("Poção", "pocao"))

        decisao = self.ia.tomar_decisao_combate(self.inimigo, self.jogador)
        self.assertEqual(decisao, "atacar")

if __name__ == '__main__':
    unittest.main()
