import unittest
import sys
from io import StringIO
from nexus_unificado import game_loop_principal

class TestNexusUnificadoSmoke(unittest.TestCase):
    def test_game_loop_runs_without_errors(self):
        """
        Verifica se a função principal 'game_loop_principal' pode ser
        executada sem levantar exceções. Este é um teste de fumaça
        para garantir que o jogo inicia e completa seu ciclo básico.
        """
        # Redireciona a saída padrão para suprimir o output do jogo durante o teste
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            game_loop_principal()
        except Exception as e:
            self.fail(
                f"A função 'game_loop_principal' levantou uma exceção inesperada: {e}"
            )
        finally:
            # Restaura a saída padrão
            sys.stdout = original_stdout

if __name__ == '__main__':
    unittest.main()
