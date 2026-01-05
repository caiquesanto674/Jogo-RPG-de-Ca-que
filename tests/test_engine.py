import unittest
from io import StringIO
from unittest.mock import patch
from apolo_engine.systems.motor import Engine_APOLO
from apolo_engine.systems.log import LogLevel, LogSistema


class TestEngineIntegration(unittest.TestCase):
    def setUp(self):
        """Prepara uma nova instância do motor para cada teste."""
        self.engine = Engine_APOLO(owner="TEST_COMMANDER")

    def test_ciclos_completos_sem_erros(self):
        """
        Verifica se o método principal 'turno_completo' pode ser executado
        múltiplas vezes sem levantar exceções. Este é um teste de fumaça
        crítico para garantir a integração de todos os sistemas.
        """
        try:
            for i in range(5):
                self.engine.turno_completo()
        except Exception as e:
            self.fail(
                f"O método 'turno_completo' levantou uma exceção inesperada: {e}"
            )

    def test_log_level_filter(self):
        """
        Verifica se o sistema de log filtra corretamente as mensagens
        com base no nível de log configurado.
        """
        log_sistema = LogSistema(min_level=LogLevel.INFO)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            log_sistema.registrar(
                "TEST", "DEBUG_SOURCE", "Debug message", level=LogLevel.DEBUG
            )
            self.assertEqual(fake_out.getvalue(), "")

            log_sistema.registrar(
                "TEST", "INFO_SOURCE", "Info message", level=LogLevel.INFO
            )
            self.assertIn("Info message", fake_out.getvalue())
