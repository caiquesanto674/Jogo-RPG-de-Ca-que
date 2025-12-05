# ====================== SISTEMA DE UNIFICAÇÃO CAUSAL ========================
# Função: Gerenciar a integração de módulos de código vindos de múltiplas
# plataformas (o seu "Multiverso de Gravataí") no projeto 'Jogo RPG de Caíque'.
#
# A integração é feita em SEÇÕES ESPECÍFICAS para manter a organização
# (Economia, Militar, Tecnologia, etc.), conforme o seu plano de modularização.

from typing import Dict, List, Tuple
import re
from datetime import datetime
import sys

# =========================== CONFIGURAÇÃO E LOG ============================

LOG_MERGE_FILE = "log_merge_causal.txt"

# Estrutura inicial do código principal com placeholders para organização.
CODIGO_PRINCIPAL_TEMPLATE: List[str] = [
    "# === ARQUIVO PRINCIPAL DO NEXUS (Jogo RPG de Caíque) ===\n",
    "import random\n",
    "import sys\n",
    "\n",
    "# ----------------------- SEÇÃO 1: CORE E INICIALIZAÇÃO -----------------------\n",
    "def regra_base_global():\n",
    "    return 'Volição Ativa e Kernel 2.5'\n",
    "\n",
    "# ----------------------- SEÇÃO 2: MÓDULOS DE JOGO ------------------------\n",
    "\n",
    "[# SEÇÃO PARA: ECONOMIA E RECURSOS #]\n",
    "\n",
    "[# SEÇÃO PARA: UNIDADES E COMBATE MILITAR #]\n",
    "\n",
    "[# SEÇÃO PARA: TECNOLOGIA E HABILIDADES #]\n",
    "\n",
    "# ----------------------- SEÇÃO 3: LÓGICA PRINCIPAL (LOOP) -----------------------\n",
    "def game_loop_principal():\n",
    "    print(f'Iniciando Loop: {regra_base_global()}')\n",
    "\n",
    "# === FIM DO ARQUIVO ===\n"
]

# Mapeamento para garantir que o nome da seção é válido
SECOES_VALIDAS = {
    "ECONOMIA E RECURSOS": "[# SEÇÃO PARA: ECONOMIA E RECURSOS #]",
    "UNIDADES E COMBATE MILITAR": "[# SEÇÃO PARA: UNIDADES E COMBATE MILITAR #]",
    "TECNOLOGIA E HABILIDADES": "[# SEÇÃO PARA: TECNOLOGIA E HABILIDADES #]",
}


def salvar_log_merge(mensagem: str):
    """
    Salva uma mensagem de log no arquivo de merge, com timestamp.

    Esta função utiliza o statement 'with open(...)', que é o equivalente em Python
    ao bloco 'try-with-resources' de outras linguagens. Ele garante que o arquivo
    será fechado automaticamente ao final do bloco, mesmo que ocorram erros,
    prevenindo vazamentos de recursos.

    Args:
        mensagem (str): A mensagem a ser registrada no log.
    """
    try:
        with open(LOG_MERGE_FILE, 'a', encoding='utf-8') as arquivo:
            arquivo.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}\n")
    except IOError as e:
        # Se falhar ao escrever no arquivo, imprime no console para não perder o log.
        print(f"[ERRO DE LOG]: Falha ao salvar log de merge. {e}", file=sys.stderr)


def detectar_conflitos(codigo_principal: List[str], novo_codigo: str) -> List[str]:
    """
    Analisa o código principal e um novo trecho de código para encontrar
    definições de classes ou funções com o mesmo nome.

    Args:
        codigo_principal (List[str]): O estado atual do código principal.
        novo_codigo (str): O novo trecho de código a ser verificado.

    Returns:
        List[str]: Uma lista com os nomes das classes/funções conflitantes.
    """
    padrao_def = re.compile(r"^(?:class|def)\s+(\w+)")
    defs_principais = set()

    for linha in codigo_principal:
        match = padrao_def.search(linha)
        if match:
            defs_principais.add(match.group(1))

    conflitos = []
    for linha in novo_codigo.splitlines():
        match = padrao_def.search(linha)
        if match:
            nome_definicao = match.group(1)
            if nome_definicao in defs_principais:
                conflitos.append(nome_definicao)

    return conflitos

def integrar_novo_modulo(codigo_principal: List[str], nome_modulo: str, secao_alvo: str, novo_codigo: str) -> Tuple[str, List[str]]:
    """
    Integra um novo módulo de código no código principal, após validar a seção
    e verificar a ausência de conflitos.

    Args:
        codigo_principal (List[str]): O estado atual do código principal.
        nome_modulo (str): Nome da fonte do novo módulo (para logging).
        secao_alvo (str): Nome da seção onde o código será inserido.
        novo_codigo (str): O código a ser integrado.

    Returns:
        Tuple[str, List[str]]: Uma tupla contendo uma mensagem de status e o
                               novo estado do código principal (modificado ou não).
    """
    codigo_modificado = list(codigo_principal)

    if secao_alvo not in SECOES_VALIDAS:
        mensagem = f"[ERRO DE INTEGRAÇÃO Causal]: Seção alvo '{secao_alvo}' não é válida. O código não foi integrado."
        salvar_log_merge(mensagem)
        return mensagem, codigo_modificado

    conflitos = detectar_conflitos(codigo_modificado, novo_codigo)
    if conflitos:
        mensagem = f"[ERRO DE CONFLITO Causal]: Módulo '{nome_modulo}' falhou no merge. Conflitos detectados em: {', '.join(conflitos)}. O código não foi alterado."
        salvar_log_merge(mensagem)
        return mensagem, codigo_modificado

    placeholder = SECOES_VALIDAS[secao_alvo]
    try:
        indice = codigo_modificado.index(placeholder + "\n")
    except ValueError:
        mensagem = f"[ERRO DE INTEGRAÇÃO Causal]: Placeholder '{placeholder}' não encontrado no código principal."
        salvar_log_merge(mensagem)
        return mensagem, codigo_modificado

    bloco_a_inserir = [f"\n# --- INTEGRADO DE: {nome_modulo} ({secao_alvo}) ---\n"]
    for linha in novo_codigo.splitlines():
        bloco_a_inserir.append(linha + "\n")

    codigo_modificado[indice:indice] = bloco_a_inserir

    mensagem = f"[SUCESSO DE MERGE Causal]: Módulo '{nome_modulo}' integrado com sucesso na seção '{secao_alvo}'."
    salvar_log_merge(mensagem)

    return mensagem, codigo_modificado

# ==================== DEMONSTRAÇÃO DO INTEGRATOR ====================
if __name__ == '__main__':
    print("Módulo Integrador Causal carregado. Execute 'test_integrador_cris.py' para a Verificação CRIS.")
