import unittest
from engine.motor import Engine

class TestEngine(unittest.TestCase):

    def setUp(self):
        self.engine = Engine()

    def test_inicializacao(self):
        self.assertEqual(self.engine.turno, 0)
        self.assertIsNotNone(self.engine.protagonista)
        self.assertEqual(self.engine.protagonista.nome, "CAÍQUE APOLO Ω")

    def test_ciclo(self):
        self.engine.ciclo()
        self.assertEqual(self.engine.turno, 1)

    def test_ataque_psiquico(self):
        monarca = self.engine.protagonista
        inimigo = self.engine.inimigos[0]
        moral_inicial = monarca.moral
        inimigo.usar_poder(monarca)
        self.assertLess(monarca.moral, moral_inicial)

    def test_ai_cardinal(self):
        monarca = self.engine.protagonista
        monarca.moral = 10
        self.engine.cardinal.salvar_realidade(monarca, self.engine.economia)
        self.assertEqual(monarca.moral, 100)

if __name__ == '__main__':
    unittest.main()
