import random
import unittest

from apolo_engine.motor_jogo import MotorJogo
from apolo_engine.entities.unidade import UnidadeMilitar
from apolo_engine.systems.tecnologia import Tecnologia

class TestMotorJogo(unittest.TestCase):
    def setUp(self):
        """Prepara um novo motor de jogo para cada teste, garantindo isolamento."""
        self.engine = MotorJogo()
        self.tech = Tecnologia()

    def test_ciclo_turno_executa_sem_erros(self):
        """Verifica se um ciclo de turno completo é executado sem levantar exceções."""
        try:
            self.engine.ciclo_turno()
        except Exception as e:
            self.fail(f"O método ciclo_turno() levantou uma exceção inesperada: {e}")

    def test_economia_producao_apos_turno(self):
        """Garante que os recursos (exceto ouro) aumentam após o ciclo econômico."""
        recursos_antes = self.engine.economia.recursos.copy()
        self.engine.ciclo_turno()
        recursos_depois = self.engine.economia.recursos

        self.assertEqual(recursos_antes["ouro"], recursos_depois["ouro"])

        for recurso in ["aço", "mana", "comida", "energia"]:
            self.assertGreater(
                recursos_depois[recurso],
                recursos_antes[recurso],
                f"O recurso '{recurso}' não aumentou após um turno.",
            )

    def test_adicionar_unidade_a_base(self):
        """Testa a adição de uma nova UnidadeMilitar à base."""
        contagem_unidades_antes = len(self.engine.base.unidades)
        nova_unidade = UnidadeMilitar(nome="Franco-Atirador-01", classe="Franco-Atirador", tech=self.tech)
        self.engine.base.adicionar_unidade(nova_unidade)
        contagem_unidades_depois = len(self.engine.base.unidades)
        self.assertEqual(contagem_unidades_depois, contagem_unidades_antes + 1)
        self.assertIn(nova_unidade, self.engine.base.unidades)

    def test_forca_belica_unidade_sem_bonus(self):
        """Verifica se a força bélica de uma unidade é calculada corretamente sem bônus."""
        # Garantimos que não há bônus de tecnologia para este teste
        self.tech.arvore["Plasma"] = 0

        unidade_tanque = UnidadeMilitar(nome="Tanque Padrão", classe="Tanque", tech=self.tech)

        # Força Bélica = Forca_Base * (Moral/100) * (Bônus Tech) * (Bônus Posição) * (Bônus Comando)
        # 20 * (100/100) * (1.0 + 0 * 0.10) * 1.0 * 1.0 = 20
        poder_esperado = 20.0
        self.assertAlmostEqual(unidade_tanque.calcular_forca_belica(), poder_esperado)

    def test_forca_belica_unidade_com_tecnologia(self):
        """Verifica se o bônus de tecnologia é aplicado corretamente na força bélica."""
        self.tech.arvore['Plasma'] = 2  # Nível 2 de Plasma = +20% de bônus (0.10 por nível)
        unidade_tanque = UnidadeMilitar(nome="Tanque de Plasma", classe="Tanque", tech=self.tech)

        # Força Bélica = 20 * (100/100) * (1.0 + 2 * 0.10) * 1.0 * 1.0 = 24.0
        poder_esperado = 24.0
        self.assertAlmostEqual(unidade_tanque.calcular_forca_belica(), poder_esperado)

    def test_multiagentes_ai_evoluem(self):
        """Testa se os agentes de IA rodam seus ciclos sem erro."""
        estados_iniciais = [a.evo for a in self.engine.agentes]
        for _ in range(3):
            self.engine.ciclo_turno(random.choice(["combate", "exploracao", "crise"]))

        self.assertEqual(len(self.engine.agentes), len(estados_iniciais))


if __name__ == "__main__":
    unittest.main()
