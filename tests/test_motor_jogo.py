import random
import unittest
from src.motor_jogo import MotorJogo

class TestMotorJogo(unittest.TestCase):
    def test_multiagentes(self):
        engine = MotorJogo()
        for i in range(3):
            engine.ciclo_turno(random.choice(["combate","exploracao","crise"]))
        self.assertTrue(all(a.evo>=0 for a in engine.agentes))
        print("Testes básicos de multi-agente concluídos!")

if __name__ == "__main__":
    unittest.main()
