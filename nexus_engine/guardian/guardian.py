"""
Módulo Principal do Nexus Guardian.
"""

from typing import Dict

from nexus_engine.guardian.structural_analyzer import StructuralAnalyzer
from nexus_engine.guardian.semantic_analyzer import SemanticAnalyzer
from nexus_engine.guardian.auto_heal_engine import AutoHealEngine
from nexus_engine.guardian.patch_system import PatchSystem
from nexus_engine.guardian.test_executor import TestExecutor
from nexus_engine.guardian.memory_kernel import MemoryKernel

class NexusGuardian:
    """
    Sistema de análise e autocorreção unificado.
    Orquestra os vários componentes do sistema Guardian.
    """

    def __init__(self):
        self.analisador_estrutural = StructuralAnalyzer()
        self.analisador_semantico = SemanticAnalyzer()
        self.auto_heal = AutoHealEngine()
        self.patch_system = PatchSystem()
        self.testes = TestExecutor()
        self.memoria = MemoryKernel()

    def analisar_codigo(self, codigo: str, nome_arquivo: str) -> Dict:
        """
        Executa uma análise completa do código, utilizando todos os
        subsistemas do Guardian.

        Args:
            codigo (str): O código-fonte a ser analisado.
            nome_arquivo (str): O nome do arquivo associado ao código.

        Returns:
            Dict: Um relatório completo da análise.
        """
        # Etapa 1: Tentativa de autocura (opcional, pode ser ativada se necessário)
        # codigo_curado = self.auto_heal.heal_syntax(codigo)
        # codigo_curado = self.auto_heal.heal_structure(codigo_curado)
        codigo_analise = codigo # Usar o código original por padrão

        # Etapa 2: Análise Estrutural
        estrutura = self.analisador_estrutural.map_file(codigo_analise, nome_arquivo)

        # Etapa 3: Análise Semântica
        semantica = self.analisador_semantico.analyze(codigo_analise, nome_arquivo)

        # Etapa 4: Execução de Testes Básicos
        resultados_teste = self.testes.run_basic_tests(codigo_analise)

        # Etapa 5: Armazenar resultados na memória
        dados_completos = {
            "estrutura": estrutura,
            "semantica": semantica,
            "testes": resultados_teste,
            "hash": estrutura.get("hash") # Reutiliza o hash já calculado
        }
        self.memoria.store(nome_arquivo, dados_completos)

        # Etapa 6: Gerar o relatório final
        relatorio = {
            "arquivo": nome_arquivo,
            # "curado": codigo != codigo_analise, # Desativado por padrão
            "analise": dados_completos
        }

        return relatorio

    def comparar_arquivos(self, nome_arquivo1: str, nome_arquivo2: str) -> Dict:
        """
        Compara dois arquivos previamente analisados que estão na memória.
        """
        dados1 = self.memoria.retrieve(nome_arquivo1)
        dados2 = self.memoria.retrieve(nome_arquivo2)

        if not dados1 or not dados2:
            return {"erro": "Um ou ambos os arquivos não foram encontrados na memória."}

        similaridade = self.analisador_semantico.compare_similarity(nome_arquivo1, nome_arquivo2)

        hash1 = dados1.get("hash")
        hash2 = dados2.get("hash")

        return {
            "similaridade_semantica": similaridade,
            "hashes_iguais": hash1 == hash2,
            "hash_arquivo1": hash1,
            "hash_arquivo2": hash2
        }

    def gerar_patch_entre_versoes(self, codigo_original: str, codigo_modificado: str) -> Dict:
        """
        Gera um patch entre duas versões de um código.
        """
        return self.patch_system.generate_patch(codigo_original, codigo_modificado)
