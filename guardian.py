# guardian.py
# Sistema Guardião para a Arquitetura Modular do Monarca Caíque

import os
import json
import ast
import logging
from typing import Dict, List, Set

logging.basicConfig(level=logging.INFO, format='[GUARDIAN] [%(levelname)s] %(message)s')

class Guardian:
    def __init__(self, config_path: str = 'guardian_config.json'):
        """Inicializa o Guardião com a configuração da arquitetura."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            logging.info(f"Sistema Guardião ativado para o projeto '{self.config['project_name']}'.")
        except FileNotFoundError:
            logging.error(f"Arquivo de configuração '{config_path}' não encontrado. O Guardião não pode operar.")
            self.config = None
        except json.JSONDecodeError:
            logging.error(f"Erro ao decodificar o arquivo de configuração '{config_path}'.")
            self.config = None

    def _get_existing_files(self) -> Dict[str, str]:
        """Mapeia todos os arquivos .py existentes na arquitetura definida."""
        if not self.config: return {}

        source_root = self.config['architecture']['source_root']
        existing_files = {}
        for root, _, files in os.walk(source_root):
            for file in files:
                if file.endswith('.py'):
                    # Chave: nome do arquivo (sem .py), Valor: caminho completo
                    existing_files[file[:-3]] = os.path.join(root, file)
        return existing_files

    def _analyze_new_module(self, module_path: str) -> Dict[str, Set[str]]:
        """Analisa um novo módulo e extrai os nomes de suas classes e funções globais."""
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                code = f.read()
            tree = ast.parse(code)
            elements = {'classes': set(), 'functions': set()}
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    elements['classes'].add(node.name)
                elif isinstance(node, ast.FunctionDef):
                    elements['functions'].add(node.name)
            return elements
        except Exception as e:
            logging.error(f"Falha ao analisar o módulo '{module_path}': {e}")
            return {'classes': set(), 'functions': set()}

    def check_new_module(self, new_module_path: str):
        """Verifica um novo módulo contra a arquitetura e o código existentes."""
        if not self.config:
            logging.warning("Guardião desativado devido à falta de configuração.")
            return

        logging.info(f"Analisando novo módulo: '{new_module_path}'...")

        # 1. Verificar conflito de nome de arquivo
        existing_files = self._get_existing_files()
        new_module_name = os.path.basename(new_module_path)[:-3]
        if new_module_name in existing_files:
            logging.error(f"CONFLITO DE ARQUIVO: Um arquivo chamado '{new_module_name}.py' já existe em '{existing_files[new_module_name]}'.")
            logging.warning("Por favor, renomeie seu arquivo antes de tentar a integração.")
            return

        # 2. Analisar conteúdo e sugerir pasta
        new_elements = self._analyze_new_module(new_module_path)
        if not new_elements['classes']:
            logging.warning("O novo módulo não contém classes globais. Nenhuma sugestão de pasta automática.")
            return

        # 3. Sugerir a pasta com base na classe principal
        main_class = next(iter(new_elements['classes'])) # Pega a primeira classe encontrada
        suggestion = "N/A"

        if main_class in self.config['keywords_mapping']:
            target_folder_key = self.config['keywords_mapping'][main_class]
            target_path = self.config['architecture'][target_folder_key]
            suggestion = target_path
            logging.info(f"SUGESTÃO: Com base na classe '{main_class}', este módulo parece pertencer a '{target_path}'.")
        else:
            logging.warning(f"A classe principal '{main_class}' não está no mapa de palavras-chave. Nenhuma sugestão de pasta automática.")

        logging.info("Análise do Guardião concluída.")

if __name__ == '__main__':
    guardian = Guardian()
    if guardian.config:
        # Exemplo de como o Guardião será usado (requer a criação de um módulo de teste)
        # Para usar, descomente a linha abaixo e substitua pelo caminho do seu novo arquivo.
        # guardian.check_new_module('caminho/para/seu_novo_modulo.py')
        logging.info("Guardião pronto para verificar a arquitetura.")
