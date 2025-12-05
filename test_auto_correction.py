# test_auto_correction.py
# Testes de Unidade para o Motor de Auto-Correção

import unittest
from auto_correction_system import SystemState, AutoCorrectionEngine, FailureTracker

class TestAutoCorrectionEngine(unittest.TestCase):

    def setUp(self):
        """Configura um novo motor de IA e componentes para cada teste."""
        self.engine = AutoCorrectionEngine(initial_resources=1000)
        self.comp_ok = SystemState("Componente OK", 50.0, 80.0, 100)
        self.comp_buggy = SystemState("Componente Buggy", 60.0, 45.0, 200)
        self.comp_caro = SystemState("Componente Caro", 40.0, 30.0, 1500)

        self.engine.add_component(self.comp_ok)
        self.engine.add_component(self.comp_buggy)
        self.engine.add_component(self.comp_caro)

    def test_component_is_buggy(self):
        """Testa se a detecção de bug (abaixo do threshold) funciona."""
        self.assertFalse(self.comp_ok.is_buggy(), "Componente OK não deve ser marcado como buggy.")
        self.assertTrue(self.comp_buggy.is_buggy(), "Componente Buggy deve ser marcado como falha.")

    def test_monitor_and_diagnose(self):
        """Testa se a IA consegue rastrear falhas corretamente."""
        self.engine.monitor_and_diagnose()

        # Apenas os componentes 'buggy' e 'caro' devem estar na fila
        self.assertEqual(len(self.engine.failure_queue), 2, "A fila de falhas deve conter apenas os componentes com falha.")
        names_in_queue = {f.component_name for f in self.engine.failure_queue}
        self.assertIn("Componente Buggy", names_in_queue)
        self.assertIn("Componente Caro", names_in_queue)
        self.assertNotIn("Componente OK", names_in_queue)

    def test_successful_fix(self):
        """Testa a correção bem-sucedida e o consumo de recursos."""
        initial_resources = self.engine.resources

        # Cria um rastreador para o componente que será corrigido
        tracker = FailureTracker(self.comp_buggy)

        # Aplica a correção
        success = self.engine.apply_fix(tracker)

        self.assertTrue(success, "A correção deveria ter sido bem-sucedida.")

        # Verifica o consumo de recursos
        expected_resources = initial_resources - self.comp_buggy.fix_cost
        self.assertEqual(self.engine.resources, expected_resources, "Os recursos devem ser gastos.")

        # Verifica se o componente foi corrigido (acima do threshold)
        self.assertTrue(self.comp_buggy.current_value >= self.comp_buggy.threshold, "O valor atual deve ser restaurado após a correção.")

        self.assertEqual(self.engine.successful_fixes, 1, "Deve haver 1 correção bem-sucedida.")

    def test_failed_fix_due_to_resources(self):
        """Testa a falha na correção devido à falta de recursos."""
        initial_resources = self.engine.resources

        # Tenta corrigir o componente caro (custo 1500 > recursos 1000)
        tracker = FailureTracker(self.comp_caro)

        # Aplica a correção
        success = self.engine.apply_fix(tracker)

        self.assertFalse(success, "A correção deveria ter falhado por falta de recursos.")

        # Verifica se os recursos NÃO foram gastos
        self.assertEqual(self.engine.resources, initial_resources, "Os recursos não devem ser gastos se a correção falhar.")

        self.assertEqual(self.engine.failed_fixes, 1, "Deve haver 1 correção falha registrada.")

        # Verifica se o componente AINDA está buggy
        self.assertTrue(self.comp_caro.is_buggy(), "O componente não deve ser corrigido se o recurso faltar.")

    def test_run_full_cycle(self):
        """Testa o ciclo completo: detectar, corrigir (e falhar onde aplicável)."""
        # Comp Buggy (Custo 200) será corrigido. Comp Caro (Custo 1500) falhará.
        initial_resources = self.engine.resources # 1000

        self.engine.run_auto_correction_cycle()

        # Recursos devem ser 1000 - 200 = 800
        self.assertEqual(self.engine.resources, 800)
        self.assertEqual(self.engine.successful_fixes, 1)
        self.assertEqual(self.engine.failed_fixes, 1)

        # O componente corrigido não deve mais ser um bug
        self.assertFalse(self.comp_buggy.is_buggy())
        # O componente caro ainda deve ser um bug
        self.assertTrue(self.comp_caro.is_buggy())

# Código para executar os testes
if __name__ == '__main__':
    # Para executar, salve como 'test_auto_correction.py' e execute 'python -m unittest test_auto_correction.py'
    # Use o comando abaixo para executar dentro de um ambiente notebook/console
    print("Executando testes. Se estiver em um ambiente que suporte unittest, execute no terminal.")
    # unittest.main() # Descomente para rodar via CLI/Terminal