import unittest
from main import MotorJogo


class TestMotorJogo(unittest.TestCase):
    def test_inicializacao_e_ciclo(self):
        """
        Testa se o MotorJogo pode ser inicializado e executar um ciclo de turno sem erros.
        """
        try:
            motor = MotorJogo()
            motor.ciclo_turno()
        except Exception as e:
            self.fail(f"A inicialização ou o ciclo do MotorJogo falhou com o erro: {e}")

if __name__ == "__main__":
    unittest.main()
