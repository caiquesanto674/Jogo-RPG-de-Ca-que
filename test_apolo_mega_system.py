import unittest
from unittest.mock import patch
from APOLO_MEGA_SYSTEM_FINAL import *

class TestApoloMegaSystem(unittest.TestCase):

    def setUp(self):
        """Configura um ambiente de teste novo para cada teste."""
        self.engine = Engine()

    def test_inicializacao_engine(self):
        """Verifica se o motor do jogo é inicializado corretamente."""
        self.assertEqual(self.engine.turno, 0)
        self.assertIsInstance(self.engine.economia, Economia)
        self.assertIsInstance(self.engine.protagonista, MonarcaAbsoluto)
        self.assertEqual(self.engine.protagonista.nome, "CAÍQUE APOLO Ω")
        self.assertEqual(len(self.engine.inimigos), 1)

    def test_economia_ciclo_ganho(self):
        """Testa se a economia ganha recursos a cada ciclo."""
        ouro_inicial = self.engine.economia.reservas.get('ouro_conceitual', 0)
        comida_inicial = self.engine.economia.reservas.get('comida', 0)

        self.engine.economia.ciclo_ganho()

        self.assertEqual(self.engine.economia.reservas['ouro_conceitual'], ouro_inicial + 10)
        self.assertEqual(self.engine.economia.reservas['comida'], comida_inicial + 100)

    def test_ataque_psiquico_sem_defesa(self):
        """Verifica o dano de moral quando a defesa psíquica está inativa."""
        monarca = self.engine.protagonista
        inimigo = self.engine.inimigos[0]

        moral_inicial = monarca.moral
        inimigo.usar_poder(monarca)

        dano_esperado = inimigo.nivel_forca * 0.75
        self.assertAlmostEqual(monarca.moral, moral_inicial - dano_esperado)

    def test_ataque_psiquico_com_defesa(self):
        """Verifica a mitigação de dano da defesa psíquica SSSS."""
        monarca = self.engine.protagonista
        inimigo = self.engine.inimigos[0]

        # Ativa a defesa
        monarca.base.defesa_psiquica = 0.5
        moral_inicial = monarca.moral

        inimigo.usar_poder(monarca)

        dano_esperado = (inimigo.nivel_forca * 0.75) * 0.5
        self.assertAlmostEqual(monarca.moral, moral_inicial - dano_esperado)

    def test_ai_cardinal_intervencao(self):
        """Testa se a AI Cardinal intervém quando a moral está criticamente baixa."""
        monarca = self.engine.protagonista
        economia = self.engine.economia

        monarca.moral = 10  # Força a condição de intervenção

        self.engine.cardinal.salvar_realidade(monarca, economia)

        self.assertEqual(monarca.moral, 100.0)
        self.assertGreater(economia.reservas['comida'], 3500)
        self.assertEqual(self.engine.cardinal.correcoes, 1)

    def test_resolucao_conflito_ia(self):
        """Verifica se o sistema de resolução de conflitos funciona como esperado."""
        log_manager = self.engine.log_manager
        conteudo_falso = "<<<<<<< HEAD \n Código Antigo \n ======= \n Código Novo \n >>>>>>> feature"

        em_conflito, _ = ConflictResolver.simular_leitura_arquivo(conteudo_falso)
        self.assertTrue(em_conflito)

        _, decisao = ConflictResolver.resolver_conflito(conteudo_falso, "INCOMING")
        log_manager.registrar_correcao("teste.py", decisao)

        self.assertEqual(log_manager.total_correcoes_aplicadas, 1)

if __name__ == '__main__':
    unittest.main()
