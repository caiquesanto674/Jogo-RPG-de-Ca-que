# integrador_jules.py
# Sistema de Integração Assistida para o Monarca Caíque
# Desenvolvido por Jules, sua IA assistente.

import ast
import logging
from datetime import datetime

# Configuração do logger para feedback claro
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# --- Funções de Análise com AST ---

def analisar_codigo(codigo_fonte: str) -> dict:
    """Analisa o código-fonte e retorna um dicionário com os nomes de classes e funções."""
    try:
        arvore = ast.parse(codigo_fonte)
        elementos = {"classes": set(), "funcoes": set()}
        # Itera apenas sobre os nós de nível superior do corpo da árvore
        for no in arvore.body:
            if isinstance(no, ast.ClassDef):
                elementos["classes"].add(no.name)
            elif isinstance(no, ast.FunctionDef):
                elementos["funcoes"].add(no.name)
        return elementos
    except SyntaxError as e:
        logging.error(f"Erro de sintaxe no código-fonte: {e}")
        return None

def detectar_conflitos(elementos_base: dict, elementos_novo: dict) -> list:
    """Detecta e retorna uma lista de nomes conflitantes."""
    conflitos = []

    classes_conflitantes = elementos_base["classes"].intersection(elementos_novo["classes"])
    if classes_conflitantes:
        for nome in classes_conflitantes:
            conflitos.append(f"Classe '{nome}'")

    funcoes_conflitantes = elementos_base["funcoes"].intersection(elementos_novo["funcoes"])
    if funcoes_conflitantes:
        for nome in funcoes_conflitantes:
            conflitos.append(f"Função '{nome}'")

    return conflitos

# --- Função Principal de Integração ---

def integrar_novo_modulo(arquivo_base: str, arquivo_novo: str, arquivo_saida: str):
    """
    Tenta integrar um novo módulo ao arquivo base de forma segura.
    Se houver conflitos, a operação é abortada.
    """
    logging.info(f"Iniciando a integração de '{arquivo_novo}' em '{arquivo_base}'.")

    try:
        with open(arquivo_base, 'r', encoding='utf-8') as f:
            codigo_base = f.read()

        with open(arquivo_novo, 'r', encoding='utf-8') as f:
            codigo_novo = f.read()
    except FileNotFoundError as e:
        logging.error(f"Erro: Arquivo não encontrado - {e.filename}")
        return

    elementos_base = analisar_codigo(codigo_base)
    elementos_novo = analisar_codigo(codigo_novo)

    if not elementos_base or not elementos_novo:
        logging.error("Análise de código falhou. Integração abortada.")
        return

    conflitos = detectar_conflitos(elementos_base, elementos_novo)

    if conflitos:
        logging.error("A integração foi abortada devido aos seguintes conflitos:")
        for conflito in conflitos:
            logging.warning(f"  - Conflito detectado: {conflito} já existe no arquivo principal.")
        logging.info("Por favor, renomeie os elementos no novo módulo e tente novamente.")
    else:
        logging.info("Nenhum conflito detectado. Prosseguindo com a fusão.")

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cabecalho_integracao = f"""
# =======================================================
# MÓDULO INTEGRADO AUTOMATICAMENTE POR JULES
# Data: {timestamp}
# Origem: {arquivo_novo}
# =======================================================
"""

        codigo_final = codigo_base + "\n" + cabecalho_integracao + codigo_novo

        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(codigo_final)

        logging.info(f"Sucesso! O código foi integrado e salvo em '{arquivo_saida}'.")
        logging.info("É recomendado revisar o arquivo final.")

if __name__ == '__main__':
    logging.info("Sistema de Integração Jules - Pronto para uso.")
    # Exemplo de como usar (atualmente comentado para evitar execução acidental)
    # arquivo_principal = 'jogo_unificado_final.py'
    # novo_modulo = 'exemplo_novo_modulo.py' # Substitua pelo nome do seu arquivo
    # arquivo_final = 'jogo_unificado_final.py' # Pode ser o mesmo para sobrescrever ou um novo

    # integrar_novo_modulo(arquivo_principal, novo_modulo, arquivo_final)
