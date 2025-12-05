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
# O novo código será inserido ANTES da linha do placeholder.
CODIGO_PRINCIPAL: List[str] = [
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
    """Salva o log de merge no arquivo."""
    try:
        with open(LOG_MERGE_FILE, 'a', encoding='utf-8') as arquivo:
            arquivo.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensagem}\n")
    except IOError as e:
        # Se falhar, imprime no console, mas não aborta
        print(f"[ERRO DE LOG]: Falha ao salvar log de merge. {e}", file=sys.stderr)


def detectar_conflitos(novo_codigo: str) -> List[str]:
    """
    Detecta conflitos na Unificação Causal, procurando por funções e classes
    que já existem no código principal.
    """
    padrao_def = re.compile(r"^(?:class|def)\s+(\w+)")
    defs_principais = set()

    # Encontra todas as definições no Código Principal
    for linha in CODIGO_PRINCIPAL:
        match = padrao_def.search(linha)
        if match:
            defs_principais.add(match.group(1))

    # Verifica se as definições do novo código já existem
    conflitos = []
    for linha in novo_codigo.splitlines():
        match = padrao_def.search(linha)
        if match:
            nome_definicao = match.group(1)
            if nome_definicao in defs_principais:
                conflitos.append(nome_definicao)

    return conflitos

def integrar_novo_modulo(nome_modulo: str, secao_alvo: str, novo_codigo: str) -> Tuple[str, str]:
    """
    Recebe um novo bloco de código, detecta conflitos e o integra na seção correta.

    Args:
        nome_modulo: O nome da fonte do módulo (ex: 'ChatGPT/RPG multiverso').
        secao_alvo: O nome da seção de destino (deve estar em SECOES_VALIDAS).
        novo_codigo: O código do novo módulo.

    Returns:
        Uma tupla contendo (status do merge, código unificado).
    """
    global CODIGO_PRINCIPAL

    # 1. Validação da Seção
    if secao_alvo not in SECOES_VALIDAS:
        mensagem = f"[ERRO DE INTEGRAÇÃO Causal]: Seção alvo '{secao_alvo}' não é válida. O código não foi integrado."
        salvar_log_merge(mensagem)
        return mensagem, "".join(CODIGO_PRINCIPAL)

    # 2. Detecção de Conflitos
    conflitos = detectar_conflitos(novo_codigo)
    if conflitos:
        mensagem = f"[ERRO DE CONFLITO Causal]: Módulo '{nome_modulo}' falhou no merge. Conflitos detectados em: {', '.join(conflitos)}. O código não foi alterado."
        salvar_log_merge(mensagem)
        return mensagem, "".join(CODIGO_PRINCIPAL)

    # 3. Integração na Seção Correta
    placeholder = SECOES_VALIDAS[secao_alvo]
    try:
        # Encontra o índice do placeholder
        indice = CODIGO_PRINCIPAL.index(placeholder + "\n")
    except ValueError:
        mensagem = f"[ERRO DE INTEGRAÇÃO Causal]: Placeholder '{placeholder}' não encontrado no código principal."
        salvar_log_merge(mensagem)
        return mensagem, "".join(CODIGO_PRINCIPAL)

    # Prepara o bloco de código a ser inserido
    bloco_a_inserir = [f"\n# --- INTEGRADO DE: {nome_modulo} ({secao_alvo}) ---\n"]
    for linha in novo_codigo.splitlines():
        bloco_a_inserir.append(linha + "\n")

    # Insere o novo código ANTES do placeholder
    CODIGO_PRINCIPAL[indice:indice] = bloco_a_inserir

    mensagem = f"[SUCESSO DE MERGE Causal]: Módulo '{nome_modulo}' integrado com sucesso na seção '{secao_alvo}'."
    salvar_log_merge(mensagem)

    return mensagem, "".join(CODIGO_PRINCIPAL)

# ==================== DEMONSTRAÇÃO DO INTEGRATOR ====================
if __name__ == '__main__':
    # Este bloco executa uma breve demonstração de integração, mas para
    # o teste CRIS, vamos executar o 'test_integrador_cris.py'.
    print("Módulo Integrador Causal carregado. Execute 'test_integrador_cris.py' para a Verificação CRIS.")