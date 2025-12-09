import unittest
import sys
import os

# Adiciona o diretório raiz ao path para permitir importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from apolo_engine.entities.entidade import MonarcaAbsoluto, Inimigo, AI_NPC_Suporte
from apolo_engine.systems.economy import Economia
from apolo_engine.systems.base import BaseMilitar
from apolo_engine.ai.cardinal import AICardinal
from apolo_engine.combat.combat import calcular_efeito_psiquico

class TestApoloEngine(unittest.TestCase):

    def setUp(self):
        self.eco = Economia()
        self.base = BaseMilitar("Test Base", None, self.eco)
        self.monarca = MonarcaAbsoluto("Test Monarca", self.base)
        self.inimigo = Inimigo("Test Inimigo")
        self.cardinal = AICardinal()

    def test_ataque_psiquico(self):
        moral_inicial = self.monarca.moral
        resultado = self.inimigo.usar_poder(self.monarca)
        dano = calcular_efeito_psiquico(resultado['valor'], self.base.defesa_psiquica)
        self.monarca.moral -= dano
        self.assertLess(self.monarca.moral, moral_inicial)

    def test_mitigacao_psiquica(self):
        self.base.defesa_psiquica = 0.5
        moral_inicial = self.monarca.moral
        resultado = self.inimigo.usar_poder(self.monarca)
        dano_final = calcular_efeito_psiquico(resultado['valor'], self.base.defesa_psiquica)
        self.monarca.moral -= dano_final
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

    def test_escudo_psionico_bloqueia_dano(self):
        self.base.tecnologia.pesquisar("Escudo Psiônico SSSS", self.base)
        self.base.ativar_escudo_psionico()

        moral_inicial = self.monarca.moral
        resultado = self.inimigo.usar_poder(self.monarca)

        # Simula a lógica do main.py
        if self.base.escudo_psionico_ativo and self.base.escudo_psionico_carga > 0:
            # Dano bloqueado
            pass
        else:
            dano = calcular_efeito_psiquico(resultado['valor'], self.base.defesa_psiquica)
            self.monarca.moral -= dano

        self.assertEqual(self.monarca.moral, moral_inicial)

    def test_escudo_psionico_sem_carga(self):
        self.base.tecnologia.pesquisar("Escudo Psiônico SSSS", self.base)
        self.base.ativar_escudo_psionico()
        self.base.escudo_psionico_carga = 0

        moral_inicial = self.monarca.moral
        resultado = self.inimigo.usar_poder(self.monarca)

        # Simula a lógica do main.py
        if self.base.escudo_psionico_ativo and self.base.escudo_psionico_carga > 0:
            # Dano bloqueado
            pass
        else:
            dano = calcular_efeito_psiquico(resultado['valor'], self.base.defesa_psiquica)
            self.monarca.moral -= dano

        self.assertLess(self.monarca.moral, moral_inicial)

if __name__ == '__main__':
    unittest.main()
