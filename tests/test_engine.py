import unittest
from nexus.sistemas.motor import MotorNexus


class TestEngineIntegration(unittest.TestCase):
    def setUp(self):
        """Prepara uma nova instância do motor para cada teste."""
        self.engine = MotorNexus(owner="TEST_COMMANDER")

    def test_ciclos_completos_sem_erros(self):
        """
        Verifica se o método principal 'turno_completo' pode ser executado
        múltiplas vezes sem levantar exceções. Este é um teste de fumaça
        crítico para garantir a integração de todos os sistemas.
        """
        try:
            for i in range(5):
                print(f"Executando ciclo de teste {i + 1}...")
                self.engine.turno_completo()
        except Exception as e:
            self.fail(
                f"O método 'turno_completo' levantou uma exceção inesperada: {e}"
            )
