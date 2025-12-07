import unittest

# Testes básicos de integridade do projeto APOLO

class TestBasicoAPOLO(unittest.TestCase):
    def test_imports(self):
        # Testa se módulos essenciais importam sem erro
        import apolo_engine
        from apolo_engine.entities.entidade import Entidade
        from apolo_engine.systems.economy import Economia
        from apolo_engine.systems.base import BaseMilitar
        from apolo_engine.ai.cardinal import AICardinal
        # Apenas assegura que as classes existem
        self.assertTrue(Entidade is not None)
        self.assertTrue(Economia is not None)
        self.assertTrue(BaseMilitar is not None)
        self.assertTrue(AICardinal is not None)

    def test_economia_inicia(self):
        from apolo_engine.systems.economy import Economia
        eco = Economia()
        self.assertTrue(isinstance(eco.reservas, dict))
        # Reserva inicial deve ter 'eter' e 'mana'
        self.assertIn('eter', eco.reservas)
        self.assertIn('mana', eco.reservas)

if __name__ == '__main__':
    unittest.main()
