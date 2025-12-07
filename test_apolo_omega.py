# test_apolo_omega.py
# Suíte de Testes para o APOLO_DOMÍNIO_TOTAL_OMEGA_V2.0

import unittest
from unittest.mock import patch

# Importa as classes do módulo principal do jogo
from apolo_dominio_total_omega_v2 import (
    Engine,
    AICardinal,
    MonarcaAbsoluto,
    Inimigo,
    BaseMilitar,
    Economia
)

class TestMecanicasOmega(unittest.TestCase):
    """
    Testa as mecânicas de jogo mais críticas da Versão Ômega para garantir
    a estabilidade e a corretude da simulação.
    """

    def setUp(self):
        """Prepara um ambiente de jogo limpo para cada teste."""
        self.jogo = Engine()

    def test_intervencao_da_ia_cardinal(self):
        """
        Garante que a IA Cardinal (CIEL ASCENDIDO) intervém corretamente para
        'salvar a realidade' quando a moral do Monarca está criticamente baixa.
        """
        print("\n[TESTE] Verificando Intervenção da IA Cardinal...")

        # Força a moral do Monarca para um valor crítico
        self.jogo.protagonista.moral = 10

        # Guarda os valores antes da intervenção
        correcoes_antes = self.jogo.cardinal.correcoes

        # Roda o método que deveria acionar a IA Cardinal
        self.jogo.cardinal.salvar_realidade(self.jogo.protagonista, self.jogo.economia)

        # Verifica se a intervenção ocorreu
        self.assertEqual(self.jogo.cardinal.correcoes, correcoes_antes + 1, "A IA Cardinal deveria ter registrado uma correção.")
        self.assertEqual(self.jogo.protagonista.moral, 100.0, "A moral do Monarca deveria ter sido restaurada para 100.")
        print("OK: IA Cardinal interveio e restaurou a moral com sucesso.")

    def test_combate_psicologico_com_mitigacao_ssss(self):
        """
        Verifica se a Defesa Psíquica SSSS da base mitiga corretamente o dano
        de moral infligido pelo poder psicológico de um inimigo.
        """
        print("\n[TESTE] Verificando Mitigação de Dano Psicológico SSSS...")

        # Ativa a defesa psíquica manualmente para o teste
        self.jogo.base.defesa_psiquica = 0.50  # 50% de mitigação

        moral_inicial = self.jogo.protagonista.moral
        inimigo = self.jogo.inimigos[0]

        # O inimigo usa seu poder
        inimigo.usar_poder(self.jogo.protagonista)

        moral_final = self.jogo.protagonista.moral
        dano_sofrido = moral_inicial - moral_final

        # Cálculo esperado: dano_base (90 * 0.75 = 67.5) * mitigação (1.0 - 0.5) = 33.75
        dano_esperado = (inimigo.nivel_forca * 0.75) * (1.0 - self.jogo.base.defesa_psiquica)

        self.assertAlmostEqual(dano_sofrido, dano_esperado, places=1, msg="O dano de moral mitigado não corresponde ao esperado.")
        print(f"OK: Dano Psicológico mitigado corretamente. Dano recebido: {dano_sofrido:.1f} (Esperado: ~{dano_esperado:.1f})")

    def test_mecanica_agony_overflow(self):
        """
        Assegura que a mecânica 'Agony Overflow' é ativada quando a moral do
        Monarca está abaixo de 20, aumentando seu Índice Dimensional.
        """
        print("\n[TESTE] Verificando Mecânica 'Agony Overflow'...")

        # Força a moral para um valor que ative a mecânica
        self.jogo.protagonista.moral = 15

        indice_antes = self.jogo.protagonista.indice_dimensional

        # Roda o método que ativa a volição
        ativado = self.jogo.protagonista.ativar_volicao()

        self.assertTrue(ativado, "Agony Overflow deveria ter sido ativado.")
        self.assertEqual(self.jogo.protagonista.indice_dimensional, indice_antes + 0.5, "O Índice Dimensional deveria ter aumentado em 0.5.")
        self.assertEqual(self.jogo.protagonista.moral, 70, "A moral deveria ser restaurada para 70 após o overflow.")
        print("OK: 'Agony Overflow' ativado com sucesso, poder aumentado.")

    def test_nao_ativacao_de_agony_overflow_com_moral_alta(self):
        """
        Verifica que 'Agony Overflow' NÃO é ativado se a moral do Monarca
        estiver acima do limite crítico.
        """
        print("\n[TESTE] Verificando que 'Agony Overflow' não ativa com moral alta...")

        self.jogo.protagonista.moral = 50 # Moral segura
        indice_antes = self.jogo.protagonista.indice_dimensional

        ativado = self.jogo.protagonista.ativar_volicao()

        self.assertFalse(ativado, "Agony Overflow não deveria ter sido ativado.")
        self.assertEqual(self.jogo.protagonista.indice_dimensional, indice_antes, "O Índice Dimensional não deveria ter mudado.")
        print("OK: 'Agony Overflow' corretamente não ativado com moral segura.")

if __name__ == '__main__':
    print("="*70)
    print("  INICIANDO SUÍTE DE TESTES PARA AS MECÂNICAS ÔMEGA DO MONARCA  ")
    print("="*70)
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    print("\n" + "="*70)
    print("                  TESTES DA VERSÃO ÔMEGA CONCLUÍDOS                 ")
    print("="*70)
