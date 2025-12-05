# ====================== TESTE DE VERIFICAÇÃO CRIS =======================
# Teste de Confirmação, Revisão e Integridade do Sistema de Unificação Causal.
# Objetivo: Garantir que o Integrador_Modular.py obedece às regras de conflito
# e integração de seções.

import unittest
import os
import shutil
from datetime import datetime
from typing import List

# Importamos diretamente as funções do nosso módulo principal
# Usamos try/except para lidar com o caso onde o arquivo pode não ter rodado a demonstração
try:
    from Integrador_Modular import (
        CODIGO_PRINCIPAL, integrar_novo_modulo, detectar_conflitos, SECOES_VALIDAS, LOG_MERGE_FILE
    )
except ImportError:
    print("ERRO: O arquivo Integrador_Modular.py deve estar no mesmo diretório.")
    exit(1)

# Salvamos uma cópia do estado inicial para resetar entre os testes
CODIGO_INICIAL_STATE: List[str] = list(CODIGO_PRINCIPAL)

class TestIntegradorCausal(unittest.TestCase):
    """
    Conjunto de testes unitários para o Sistema de Unificação Causal (Nexus).
    """

    def setUp(self):
        """
        Prepara o ambiente para cada teste:
        1. Reseta o código principal para o estado inicial.
        2. Limpa o arquivo de log para garantir logs específicos para o teste.
        """
        # 1. Reseta o estado do código principal para o estado inicial
        CODIGO_PRINCIPAL.clear()
        CODIGO_PRINCIPAL.extend(CODIGO_INICIAL_STATE)

        # 2. Limpa o log (se existir)
        if os.path.exists(LOG_MERGE_FILE):
            os.remove(LOG_MERGE_FILE)

        print(f"\n[{self.id().split('.')[-1]}] -> Teste Preparado...")


    def test_a_deteccao_de_conflito_deve_falhar(self):
        """
        CRIS-01: Testa se a regra de Domínio de Causalidade (Não-Conflito) é obedecida.
        Tenta adicionar uma função que já existe ('regra_base_global').
        """
        print("Executando: Testa Detecção de Conflito...")

        codigo_conflitante = """
def regra_base_global(): # Duplicado!
    return 'Volição Falha'

class ClasseNova:
    pass
"""
        # A detecção DEVE encontrar o conflito
        conflitos = detectar_conflitos(codigo_conflitante)
        self.assertIn('regra_base_global', conflitos)
        self.assertEqual(len(conflitos), 1)

        # A integração DEVE retornar uma mensagem de erro
        status, _ = integrar_novo_modulo(
            nome_modulo="CRIS Teste Conflito",
            secao_alvo="TECNOLOGIA E HABILIDADES",
            novo_codigo=codigo_conflitante
        )
        self.assertIn("[ERRO DE CONFLITO Causal]", status)
        self.assertNotIn("ClasseNova", "".join(CODIGO_PRINCIPAL))
        print("OK: Conflito detectado e merge bloqueado.")


    def test_b_integracao_em_secao_valida_deve_funcionar(self):
        """
        CRIS-02: Testa se a integração em uma seção válida ocorre no local correto.
        Simula o código de 'Recurso' vindo do GitHub.
        """
        print("Executando: Testa Integração em Seção Válida...")

        codigo_github = """
class RecursoFinanceiro:
    def __init__(self, valor):
        self.valor = valor

def processar_transacao():
    return True
"""
        # A integração DEVE ser bem-sucedida
        nome_modulo = "GitHub Volição - src/game/economia.py"
        secao_alvo = "ECONOMIA E RECURSOS"
        status, codigo_final = integrar_novo_modulo(
            nome_modulo=nome_modulo,
            secao_alvo=secao_alvo,
            novo_codigo=codigo_github
        )

        self.assertIn("[SUCESSO DE MERGE Causal]", status)
        self.assertIn("class RecursoFinanceiro", codigo_final)

        # Confirma se o código foi inserido na posição correta (antes do placeholder)
        placeholder = CODIGO_PRINCIPAL.index(SECOES_VALIDAS[secao_alvo] + "\n")

        # A linha anterior deve ser a última linha do código inserido
        self.assertIn("def processar_transacao():", CODIGO_PRINCIPAL[placeholder - 2])
        print("OK: Código de Economia integrado com sucesso na seção correta.")


    def test_c_integracao_em_secao_invalida_deve_falhar(self):
        """
        CRIS-03: Testa se a integração falha ao tentar usar uma seção inexistente.
        """
        print("Executando: Testa Seção Inválida...")

        codigo_teste = "def funcao_teste(): return 1"
        secao_invalida = "SEÇÃO INEXISTENTE"

        status, _ = integrar_novo_modulo(
            nome_modulo="CRIS Teste Seção Inválida",
            secao_alvo=secao_invalida,
            novo_codigo=codigo_teste
        )

        self.assertIn("[ERRO DE INTEGRAÇÃO Causal]", status)
        self.assertIn("não é válida", status)
        print("OK: Integração bloqueada devido a Seção Alvo Inválida.")


    def test_d_log_de_causalidade_deve_conter_registros(self):
        """
        CRIS-04: Testa se o log de eventos foi atualizado com as tentativas de merge.
        """
        print("Executando: Testa Log de Causalidade...")

        # Força um sucesso e uma falha para garantir que ambos são logados
        codigo_sucesso = "class TesteLogSucesso:\n    pass"
        codigo_falha = "def regra_base_global():\n    pass" # Conflito

        integrar_novo_modulo("Log Sucesso", "TECNOLOGIA E HABILIDADES", codigo_sucesso)
        integrar_novo_modulo("Log Falha", "TECNOLOGIA E HABILIDADES", codigo_falha)

        self.assertTrue(os.path.exists(LOG_MERGE_FILE))

        with open(LOG_MERGE_FILE, 'r', encoding='utf-8') as f:
            log_content = f.read()

        self.assertIn("[SUCESSO DE MERGE Causal]: Módulo 'Log Sucesso'", log_content)
        self.assertIn("[ERRO DE CONFLITO Causal]: Módulo 'Log Falha'", log_content)
        print("OK: Log de Causalidade (log_merge_causal.txt) criado e registrado eventos.")


if __name__ == '__main__':
    print("================================================================")
    print(" INICIANDO TESTE DE VERIFICAÇÃO CRIS PARA O NEXUS DE GRAVATAÍ ")
    print("================================================================")
    # Rodamos o módulo de teste
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    print("\n================================================================")
    print(" TESTE CRIS CONCLUÍDO. VERIFIQUE AS MENSAGENS 'OK' ACIMA. ")
    print("================================================================")