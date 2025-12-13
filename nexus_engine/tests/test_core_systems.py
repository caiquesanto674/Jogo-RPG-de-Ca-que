"""
Testes unitários para os sistemas centrais refatorados do Nexus Engine.
"""

import sys
import os
import unittest
from datetime import datetime

# Adiciona o diretório raiz do projeto ao sys.path para garantir que os imports funcionem
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Importa as classes refatoradas
from nexus_engine.core.logger import UniversalLog
from nexus_engine.core.time_manager import NexusTime
from nexus_engine.entities.entity import Entidade
from nexus_engine.core.engine import NexusEngine
from nexus_engine.guardian.guardian import NexusGuardian

class TestUniversalLog(unittest.TestCase):
    """Testes para o sistema de log universal"""

    def setUp(self):
        self.log = UniversalLog(max_size=10)

    def test_registrar_evento(self):
        """Testa registro de evento"""
        evento_id = self.log.registrar("teste", "info", {"mensagem": "teste"})
        self.assertIsInstance(evento_id, str)
        self.assertEqual(len(evento_id), 36)

    def test_consultar_eventos(self):
        """Testa consulta de eventos"""
        self.log.registrar("teste", "info", {"teste": 1})
        self.log.registrar("teste", "erro", {"teste": 2})

        eventos = self.log.consultar(tipo="info")
        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0]["tipo"], "info")

    def test_limite_tamanho(self):
        """Testa limite de tamanho do log"""
        for i in range(15):
            self.log.registrar("teste", "info", {"numero": i})

        self.assertLessEqual(len(self.log.eventos), 10)

class TestNexusTime(unittest.TestCase):
    """Testes para o sistema de tempo"""

    def setUp(self):
        self.tempo = NexusTime()

    def test_inicializacao(self):
        """Testa inicialização do tempo"""
        self.assertEqual(self.tempo.velocidade, 1.0)
        self.assertFalse(self.tempo.pausado)

    def test_definir_velocidade(self):
        """Testa definição de velocidade"""
        self.tempo.definir_velocidade(2.0)
        self.assertEqual(self.tempo.velocidade, 2.0)

        with self.assertRaises(ValueError):
            self.tempo.definir_velocidade(0.0)

    def test_pausar_retomar(self):
        """Testa pausa e retomada do tempo"""
        self.tempo.pausar()
        self.assertTrue(self.tempo.pausado)

        self.tempo.retomar()
        self.assertFalse(self.tempo.pausado)

class TestEntidade(unittest.TestCase):
    """Testes para entidades"""

    def setUp(self):
        self.entidade = Entidade("Teste", nivel=1)

    def test_criacao_entidade(self):
        """Testa criação de entidade"""
        self.assertEqual(self.entidade.nome, "Teste")
        self.assertEqual(self.entidade.nivel, 1)
        self.assertTrue(self.entidade.esta_viva())

    def test_receber_dano(self):
        """Testa recebimento de dano"""
        # O HP máximo é 100 + 1 * 10 = 110
        dano = self.entidade.receber_dano(50)
        self.assertEqual(dano, 50)
        self.assertEqual(self.entidade.hp, 60)

    def test_curar(self):
        """Testa cura da entidade"""
        self.entidade.receber_dano(50) # HP vai para 60
        cura = self.entidade.curar(25)
        self.assertEqual(cura, 25)
        self.assertEqual(self.entidade.hp, 85)

    def test_afeto_limites(self):
        """Testa limites de afeto"""
        self.entidade.alterar_afeto(150)
        self.assertEqual(self.entidade.afeto, 100)

        self.entidade.alterar_afeto(-250)
        self.assertEqual(self.entidade.afeto, -100)

class TestNexusEngine(unittest.TestCase):
    """Testes para o motor principal"""

    def setUp(self):
        self.engine = NexusEngine()

    def test_iniciar_engine(self):
        """Testa inicialização do motor"""
        sucesso = self.engine.iniciar()
        self.assertTrue(sucesso)
        self.assertTrue(self.engine.iniciado)

    def test_registrar_entidade(self):
        """Testa registro de entidade"""
        entidade = Entidade("Teste")
        entidade_id = self.engine.registrar_entidade(entidade)

        self.assertIn(entidade_id, self.engine.entidades)
        self.assertEqual(self.engine.entidades[entidade_id].nome, "Teste")

    def test_tick(self):
        """Testa ciclo de atualização"""
        self.engine.iniciar()
        resultado = self.engine.tick()

        self.assertIn("tempo", resultado)
        self.assertIn("eventos_processados", resultado)

class TestNexusGuardian(unittest.TestCase):
    """Testes para o sistema Guardian"""

    def setUp(self):
        self.guardian = NexusGuardian()

    def test_analisar_arquivo(self):
        """Testa análise de arquivo"""
        codigo = """
class Teste:
    def metodo(self):
        return True
"""
        relatorio = self.guardian.analisar_codigo(codigo, "teste.py")

        self.assertEqual(relatorio["arquivo"], "teste.py")
        self.assertIn("analise", relatorio)
        self.assertTrue(relatorio["analise"]["estrutura"]["valido"])

if __name__ == '__main__':
    unittest.main()
