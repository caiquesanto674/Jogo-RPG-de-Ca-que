import unittest

from apolo_engine.entities.unidade import UnidadeMilitar
from apolo_engine.tecnologia import Tecnologia


class TestUnidadeMilitar(unittest.TestCase):
    def setUp(self):
        """Prepara uma tecnologia base para os testes."""
        self.tech = Tecnologia()

    def test_criacao_unidade_sucesso(self):
        """Verifica se uma unidade é criada com os atributos corretos da sua classe."""
        unidade = UnidadeMilitar(nome="Tanque-01", classe="Tanque", tech=self.tech)
        self.assertEqual(unidade.nome, "Tanque-01")
        self.assertEqual(unidade.classe, "Tanque")
        self.assertEqual(unidade.vida_maxima, 150)  # Valor de 'Defesa_Base' para Tanque
        self.assertEqual(unidade.forca_base, 20)  # Valor de 'Forca_Base' para Tanque
        self.assertEqual(unidade.mobilidade, 3)

    def test_criacao_unidade_classe_invalida(self):
        """Garante que a criação de uma unidade com uma classe desconhecida levanta um erro."""
        with self.assertRaises(ValueError):
            UnidadeMilitar(nome="Soldado Comum", classe="Guerreiro", tech=self.tech)

    def test_forca_belica_moral_afeta(self):
        """Testa se a moral da unidade afeta corretamente sua força bélica."""
        unidade = UnidadeMilitar(nome="Tanque Desmoralizado", classe="Tanque", moral=50, tech=self.tech)
        # Força Bélica = 20 * (50/100) = 10
        self.assertAlmostEqual(unidade.calcular_forca_belica(), 10.0)

    def test_forca_belica_bonus_comando(self):
        """Testa se o bônus de comando de um Comandante é aplicado corretamente."""
        comandante = UnidadeMilitar(nome="Comandante-Chefe", classe="Comandante", tech=self.tech)
        # Força Bélica = 30 * 1.0 * 1.0 * 1.0 * (1.0 + 0.25) = 37.5
        self.assertAlmostEqual(comandante.calcular_forca_belica(), 37.5)

    def test_forca_belica_bonus_posicao(self):
        """Verifica se o bônus tático de posição é aplicado corretamente."""
        unidade = UnidadeMilitar(nome="Franco-Atirador Elevado", classe="Franco-Atirador", tech=self.tech)
        # Força Bélica com bônus de posição de 20%
        # 45 * 1.0 * 1.0 * (1.0 + 0.20) * 1.0 = 54.0
        self.assertAlmostEqual(unidade.calcular_forca_belica(bonus_posicao=0.20), 54.0)

    def test_forca_belica_combinacao_bonus(self):
        """Testa uma combinação de todos os bônus na força bélica."""
        self.tech.arvore["Plasma"] = 3  # Bônus de +30%
        comandante = UnidadeMilitar(
            nome="Comandante de Elite", classe="Comandante", moral=120, tech=self.tech
        )

        # Força Base: 30
        # Moral: 1.2
        # Bônus Tech: 1.0 + 3 * 0.10 = 1.3
        # Bônus Posição: 1.0 + 0.10 = 1.1
        # Bônus Comando: 1.0 + 0.25 = 1.25
        # Força Bélica = 30 * 1.2 * 1.3 * 1.1 * 1.25 = 64.35
        forca_calculada = comandante.calcular_forca_belica(bonus_posicao=0.10)
        self.assertAlmostEqual(forca_calculada, 64.35)


if __name__ == "__main__":
    unittest.main()
