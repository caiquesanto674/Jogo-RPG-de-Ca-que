import unittest
from apolo_engine.systems.economy import Economia
from apolo_engine.systems.tecnologia import Tecnologia
from apolo_engine.entities.unidade import UnidadeMilitar

class TestApoloEngineRobustez(unittest.TestCase):
    """
    Testes de robustez para o Apolo Engine, focados em cenários de
    sucesso ("luz") e falha ("escuridão").
    """
    def setUp(self):
        """Configura um ambiente limpo para cada teste."""
        self.economia = Economia(reserva=1000)
        self.tech = Tecnologia()
        # Reseta a árvore de tecnologia para um estado conhecido
        self.tech.arvore = {"IA": 1, "Plasma": 1, "Fusao": 0}

    # --- Cenários de "Escuridão" (Falha Esperada) ---

    def test_transferencia_sem_fundos_falha_graciosamente(self):
        """Verifica se uma transferência maior que a reserva falha sem quebrar o sistema."""
        saldo_inicial = self.economia.reserva
        resultado = self.economia.transferir(saldo_inicial + 500, "Custo Fantasma")
        self.assertFalse(resultado, "A transferência deveria falhar, mas retornou True.")
        self.assertEqual(self.economia.reserva, saldo_inicial, "A reserva foi modificada indevidamente após a falha.")

    def test_pesquisar_tecnologia_inexistente_nao_cria_lixo(self):
        """Garante que pesquisar uma tecnologia inválida não a adiciona à árvore."""
        tecnologia_fantasma = "Psionica Avançada"
        self.tech.pesquisar(tecnologia_fantasma)
        self.assertNotIn(tecnologia_fantasma, self.tech.arvore, "A tecnologia fantasma foi adicionada à árvore indevidamente.")

    def test_criar_unidade_com_classe_invalida_levanta_erro(self):
        """Verifica se a criação de uma unidade com uma classe desconhecida levanta um ValueError."""
        with self.assertRaises(ValueError, msg="A criação de unidade com classe inválida não levantou ValueError."):
            UnidadeMilitar(nome="Cavaleiro", classe="ClasseInexistente", tech=self.tech)

    # --- Cenários de "Luz" (Sucesso Esperado) ---

    def test_calculo_forca_belica_com_bonus_tecnologia(self):
        """Valida se o bônus de tecnologia 'Plasma' é aplicado corretamente a um Tanque."""
        unidade = UnidadeMilitar(nome="Destruidor", classe="Tanque", tech=self.tech, moral=100)

        # Força Bélica com Plasma Nível 1 (Forca_Base = 20)
        forca_inicial = unidade.calcular_forca_belica()
        self.assertAlmostEqual(forca_inicial, 20.0, msg="A Força Bélica inicial do Tanque está incorreta.")

        # Pesquisa Plasma para Nível 2 e recalcula
        self.tech.pesquisar("Plasma")
        forca_com_bonus = unidade.calcular_forca_belica()

        # Bônus esperado: Forca_Base * (1 + Nivel_Plasma * 0.15) = 20 * (1 + 2 * 0.15) = 26
        self.assertAlmostEqual(forca_com_bonus, 26.0, msg="O bônus de tecnologia Plasma não foi aplicado corretamente.")

    def test_transferencia_com_fundos_funciona_corretamente(self):
        """Verifica se uma transferência válida debita o valor correto da reserva."""
        saldo_inicial = self.economia.reserva
        valor_transferencia = 300
        resultado = self.economia.transferir(valor_transferencia, "Compra de Suprimentos")

        self.assertTrue(resultado, "A transferência válida falhou inesperadamente.")
        self.assertEqual(self.economia.reserva, saldo_inicial - valor_transferencia, "O saldo da reserva não foi debitado corretamente.")

if __name__ == "__main__":
    unittest.main()
