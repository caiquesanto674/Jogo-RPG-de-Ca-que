# ====================== TESTE DE VERIFICAÇÃO CRIS =======================
# Teste de Confirmação, Revisão e Integridade do Sistema de Unificação Causal.
# Objetivo: Garantir que o Integrador_Modular.py obedece às regras de conflito
# e integração de seções.

import unittest
import os
from typing import List
from unittest.mock import patch, mock_open

# Importamos as funções refatoradas e as constantes do nosso módulo principal
try:
    from Integrador_Modular import (
        integrar_novo_modulo, detectar_conflitos, SECOES_VALIDAS, LOG_MERGE_FILE, CODIGO_PRINCIPAL_TEMPLATE, salvar_log_merge
    )
except ImportError:
    print("ERRO: O arquivo Integrador_Modular.py deve estar no mesmo diretório.")
    exit(1)

class TestIntegradorCausal(unittest.TestCase):
    """
    Conjunto de testes unitários para o Sistema de Unificação Causal (Nexus),
    agora testando a versão refatorada sem estado global.
    """

    def setUp(self):
        """ Prepara o ambiente para cada teste, limpando o arquivo de log. """
        if os.path.exists(LOG_MERGE_FILE):
            os.remove(LOG_MERGE_FILE)
        self.codigo_base = list(CODIGO_PRINCIPAL_TEMPLATE)
        print(f"\n[{self.id().split('.')[-1]}] -> Teste Preparado...")

    def test_a_deteccao_de_conflito_deve_falhar(self):
        """ CRIS-01: Testa se a detecção de conflitos funciona corretamente. """
        print("Executando: Testa Detecção de Conflito...")
        codigo_conflitante = "def regra_base_global(): pass"

        conflitos = detectar_conflitos(self.codigo_base, codigo_conflitante)
        self.assertIn('regra_base_global', conflitos)

        status, codigo_final = integrar_novo_modulo(
            self.codigo_base, "CRIS Teste Conflito", "TECNOLOGIA E HABILIDADES", codigo_conflitante
        )
        self.assertIn("[ERRO DE CONFLITO Causal]", status)
        self.assertEqual(self.codigo_base, codigo_final) # Garante que o código não foi modificado
        print("OK: Conflito detectado e merge bloqueado.")

    def test_b_integracao_em_secao_valida_deve_funcionar(self):
        """ CRIS-02: Testa a integração bem-sucedida em uma seção válida. """
        print("Executando: Testa Integração em Seção Válida...")
        codigo_github = "class RecursoFinanceiro: pass"

        status, codigo_final = integrar_novo_modulo(
            self.codigo_base, "GitHub Econ", "ECONOMIA E RECURSOS", codigo_github
        )

        self.assertIn("[SUCESSO DE MERGE Causal]", status)
        self.assertNotEqual(self.codigo_base, codigo_final)
        self.assertIn("class RecursoFinanceiro", "".join(codigo_final))

        print("OK: Código integrado com sucesso na seção correta.")

    def test_c_integracao_em_secao_invalida_deve_falhar(self):
        """ CRIS-03: Testa se a integração falha com uma seção alvo inválida. """
        print("Executando: Testa Seção Inválida...")
        codigo_teste = "def funcao_teste(): pass"

        status, codigo_final = integrar_novo_modulo(
            self.codigo_base, "CRIS Teste Seção Inválida", "SEÇÃO INEXISTENTE", codigo_teste
        )

        self.assertIn("[ERRO DE INTEGRAÇÃO Causal]", status)
        self.assertEqual(self.codigo_base, codigo_final)
        print("OK: Integração bloqueada devido a Seção Alvo Inválida.")

    def test_d_log_de_causalidade_deve_conter_registros(self):
        """ CRIS-04: Testa se o arquivo de log é criado e registra os eventos. """
        print("Executando: Testa Log de Causalidade...")

        codigo_sucesso = "class TesteLogSucesso: pass"
        codigo_falha = "def regra_base_global(): pass" # Conflito

        status_sucesso, _ = integrar_novo_modulo(self.codigo_base, "Log Sucesso", "TECNOLOGIA E HABILIDADES", codigo_sucesso)
        status_falha, _ = integrar_novo_modulo(self.codigo_base, "Log Falha", "TECNOLOGIA E HABILIDADES", codigo_falha)

        self.assertTrue(os.path.exists(LOG_MERGE_FILE))
        with open(LOG_MERGE_FILE, 'r', encoding='utf-8') as f:
            log_content = f.read()
        self.assertIn("Módulo 'Log Sucesso'", log_content)
        self.assertIn("Módulo 'Log Falha'", log_content)
        print("OK: Log de Causalidade criado e registrando eventos.")

    def test_e_integracao_sem_placeholder_deve_falhar(self):
        """ CRIS-05: Testa o que acontece se o placeholder da seção estiver faltando. """
        print("Executando: Testa Ausência de Placeholder...")

        # Cria uma versão do código sem o placeholder de Economia
        codigo_sem_placeholder = list(self.codigo_base)
        placeholder_economia = SECOES_VALIDAS["ECONOMIA E RECURSOS"] + "\n"
        if placeholder_economia in codigo_sem_placeholder:
            codigo_sem_placeholder.remove(placeholder_economia)

        codigo_novo = "class NovaEconomia: pass"
        status, codigo_final = integrar_novo_modulo(
            codigo_sem_placeholder, "Teste Placeholder", "ECONOMIA E RECURSOS", codigo_novo
        )

        self.assertIn("[ERRO DE INTEGRAÇÃO Causal]", status)
        self.assertIn("não encontrado no código principal", status)
        self.assertEqual(codigo_sem_placeholder, codigo_final)
        print("OK: Integração bloqueada devido à ausência do placeholder.")

    def test_f_try_with_resources_deve_ser_seguro(self):
        """ CRIS-06: Valida a robustez do 'with' statement (try-with-resources). """
        print("Executando: Testa Segurança do 'with' statement...")

        mensagem_teste = "Teste de escrita com falha."

        # Simula uma IOError durante a operação de escrita no arquivo.
        # O 'with' statement deve garantir que, mesmo com a exceção, o programa não quebre.
        with patch("builtins.open", mock_open()) as mock_file:
            mock_file.side_effect = IOError("Permissão negada")

            # Usamos 'patch' para capturar a saída do print de erro
            with patch('sys.stderr') as mock_stderr:
                salvar_log_merge(mensagem_teste)

                # Verificamos se a mensagem de erro foi impressa no sys.stderr
                captured_output = "".join(call.args[0] for call in mock_stderr.write.call_args_list)
                self.assertIn("[ERRO DE LOG]", captured_output)
                self.assertIn("Permissão negada", captured_output)

        print("OK: 'with' statement lidou com IOError de forma segura.")


if __name__ == '__main__':
    print("================================================================")
    print(" INICIANDO TESTE DE VERIFICAÇÃO CRIS PARA O NEXUS DE GRAVATAÍ ")
    print("================================================================")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    print("\n================================================================")
    print(" TESTE CRIS CONCLUÍDO. VERIFIQUE AS MENSAGENS 'OK' ACIMA. ")
    print("================================================================")
