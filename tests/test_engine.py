import unittest
import sys
import os

# Adiciona o diretório raiz ao path para permitir importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apolo_engine.entities.entidade import MonarcaAbsoluto, Inimigo
from apolo_engine.systems.economy import Economia
from apolo_engine.systems.base import BaseMilitar
from apolo_engine.ai.cardinal import AICardinal

class TestApoloEngine(unittest.TestCase):

    def setUp(self):
        self.eco = Economia()
        self.base = BaseMilitar("Test Base", None, self.eco)
        self.monarca = MonarcaAbsoluto("Test Monarca", self.base)
        self.inimigo = Inimigo("Test Inimigo")
        self.cardinal = AICardinal()

    def test_ataque_psiquico(self):
        moral_inicial = self.monarca.moral
        self.inimigo.usar_poder(self.monarca)
        self.assertLess(self.monarca.moral, moral_inicial)

    def test_mitigacao_psiquica(self):
        self.base.defesa_psiquica = 0.5
        moral_inicial = self.monarca.moral
        resultado = self.inimigo.usar_poder(self.monarca)
        dano_esperado = self.inimigo.nivel_forca * 0.75 * (1.0 - self.base.defesa_psiquica)
        self.assertAlmostEqual(self.monarca.moral, moral_inicial - dano_esperado, places=1)

    def test_agony_overflow(self):
        self.monarca.moral = 10
        ativado = self.monarca.ativar_volicao()
        self.assertTrue(ativado)
        self.assertEqual(self.monarca.moral, 70)

    def test_ai_cardinal_salvamento(self):
        self.monarca.moral = 10
        salvou = self.cardinal.salvar_realidade(self.eco, self.monarca)
        self.assertTrue(salvou)
        self.assertEqual(self.monarca.moral, 100)

if __name__ == '__main__':
    unittest.main()
