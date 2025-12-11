# -*- coding: utf-8 -*-
"""
ARQUIVO DE CONCEITO UNIFICADO DO JOGO
Este arquivo consolida os conceitos avançados de Economia, Tecnologia,
Base Militar e Sistemas de Comportamento, inspirados em múltiplas
iterações e discussões sobre o design do jogo.

Serve como um guia conceitual e protótipo para a implementação
modular no 'apolo_engine'.
"""

import random
from datetime import datetime

# =============================================================================
# ANÁLISE DE RISCOS E PROBLEMAS POTENCIAIS (PRE-MORTEM)
# =============================================================================
# 1. Complexidade de Balanceamento: A interação entre uma economia dinâmica
#    (com inflação), uma árvore tecnológica com buffs e unidades militares
#    customizáveis pode se tornar extremamente difícil de balancear.
#    -> SOLUÇÃO PROPOSTA: Isolar cada sistema para testes unitários e
#       desenvolver ferramentas de simulação para observar o equilíbrio em
#       milhares de turnos.
#
# 2. Escalabilidade da IA: A IA de comportamento precisa tomar decisões
#    considerando um número crescente de variáveis (economia, tecnologia,
#    força do jogador). Uma IA baseada em regras simples pode se tornar
#    previsível e ineficaz.
#    -> SOLUÇÃO PROPOSTA: Implementar um sistema de IA "modular", onde
#       diferentes "personalidades" (ex: Agressiva, Defensiva, Expansionista)
#       possam ser atribuídas aos NPCs, cada uma com sua própria lógica de
#       decisão e pesos.
#
# 3. Gerenciamento de Estado: Com tantos sistemas interdependentes, rastrear
#    o estado do jogo (state management) pode se tornar um desafio, levando a
#    bugs e inconsistências.
#    -> SOLUÇÃO PROPOSTA: Adotar um padrão de design claro, como o padrão
#       "Observer" ou um "Event Bus", para que os sistemas se comuniquem de
#       forma desacoplada, reagindo a eventos (ex: 'TECNOLOGIA_PESQUISADA')
#       em vez de modificar o estado um do outro diretamente.
# =============================================================================


# =============================================================================
# SEÇÃO 1: SISTEMAS DE COMPORTAMENTO E CONFIRMAÇÃO
# =============================================================================

# Dicionário centralizado de códigos de confirmação para feedback ao jogador
CODIGOS_CONFIRMACAO = {
    "BASE_UPGRADE_SUCESSO": "Base aprimorada com sucesso! Novas capacidades online.",
    "ECONOMIA_PRODUCAO_ALTA": "Produção em alta! As reservas estão florescendo.",
    "TECNOLOGIA_DESCOBERTA": "Avanço científico alcançado! O futuro é agora.",
    "UNIDADE_CRIADA": "Nova unidade pronta para o combate.",
    "OPERACAO_FALHA": "A operação falhou. Reavaliar estratégia é necessário."
}

# Dicionário de frases de comportamento para a IA, adicionando personalidade
FRASES_COMPORTAMENTO_IA = {
    "AGRESSIVO": {
        "declarar_guerra": "A fraqueza deles é um insulto. Preparem-se para a aniquilação!",
        "vitoria": "A vitória era inevitável. Eles nunca tiveram chance."
    },
    "DEFENSIVO": {
        "sob_ataque": "Nossas defesas estão sendo testadas. Repelir a ameaça a todo custo!",
        "vitoria": "A tempestade passou. Nossa resiliência prevaleceu."
    },
    "CALCULISTA": {
        "analise": "Analisando variáveis... A probabilidade de sucesso é de {chance}%.",
        "recuo": "Recuo estratégico. Viver para lutar outro dia é a jogada lógica."
    }
}

def obter_confirmacao(codigo: str) -> str:
    """Retorna uma frase de confirmação do dicionário central."""
    return CODIGOS_CONFIRMACAO.get(codigo, "Ação processada.")

def obter_frase_ia(personalidade: str, acao: str, **kwargs) -> str:
    """Retorna uma frase de comportamento da IA, com formatação opcional."""
    frase = FRASES_COMPORTAMENTO_IA.get(personalidade, {}).get(acao, "...")
    return frase.format(**kwargs)


# =============================================================================
# SEÇÃO 2: SISTEMA DE ECONOMIA AVANÇADA
# =============================================================================

class Economia:
    """
    Gerencia a economia do império, com recursos, produção, e um sistema
    de inflação dinâmico que afeta a eficiência da produção.
    """
    def __init__(self, owner: str):
        self.owner = owner
        self.recursos = {'creditos': 10000, 'metais': 5000, 'energia': 2000}
        self.producao_base_por_turno = {'creditos': 1000, 'metais': 500, 'energia': 300}
        self.inflacao = 1.0  # Fator inicial (1.0 = sem inflação)
        self.historico_transacoes = []

    def processar_turno(self):
        """
        Processa um turno econômico: calcula produção ajustada pela inflação,
        atualiza recursos e ajusta a inflação.
        """
        # A inflação alta penaliza a produção
        fator_producao = max(0.1, 2.0 - self.inflacao)

        for recurso, valor_base in self.producao_base_por_turno.items():
            ganho = int(valor_base * fator_producao)
            self.recursos[recurso] += ganho

        # A inflação flutua com base em um fator aleatório (simulando volatilidade)
        self.inflacao *= random.uniform(0.98, 1.03)
        self.historico_transacoes.append(
            f"Turno {datetime.now().second}: Produção realizada com inflação de {self.inflacao:.2f}"
        )
        print(obter_confirmacao("ECONOMIA_PRODUCAO_ALTA"))

    def gastar_recursos(self, custos: dict) -> bool:
        """Tenta gastar recursos. Retorna True se bem-sucedido, False caso contrário."""
        for recurso, custo in custos.items():
            if self.recursos.get(recurso, 0) < custo:
                print(f"Falha na transação: {recurso} insuficiente.")
                return False

        for recurso, custo in custos.items():
            self.recursos[recurso] -= custo

        self.historico_transacoes.append(f"Gasto: {custos}")
        return True

    def status_report(self):
        print("\n--- RELATÓRIO ECONÔMICO ---")
        print(f"  Proprietário: {self.owner}")
        print(f"  Inflação Atual: {self.inflacao:.2f}")
        print("  Recursos:")
        for recurso, valor in self.recursos.items():
            print(f"    - {recurso.capitalize()}: {valor}")
        print("--------------------------")


# =============================================================================
# SEÇÃO 3: SISTEMA DE TECNOLOGIA E BUFFS
# =============================================================================

class Tecnologia:
    """
    Gerencia a árvore tecnológica, pesquisas e os buffs globais
    que são aplicados a outras partes do jogo (unidades, economia, etc.).
    """
    def __init__(self):
        self.nivel_tecnologico = 1
        self.arvore_tecnologica = {
            "IA Defensiva": {"custo": 100, "desbloqueado": False, "buff": "defesa_base +10%"},
            "Propulsores de Plasma": {"custo": 200, "desbloqueado": False, "buff": "velocidade_unidade +1"},
            "Economia Quântica": {"custo": 300, "desbloqueado": False, "buff": "producao_creditos +15%"}
        }
        self.pontos_pesquisa = 0
        self.buffs_ativos = []

    def adicionar_pontos_pesquisa(self, pontos: int):
        self.pontos_pesquisa += pontos

    def pesquisar(self, nome_tecnologia: str) -> bool:
        """Tenta pesquisar uma tecnologia da árvore."""
        tech = self.arvore_tecnologica.get(nome_tecnologia)
        if not tech or tech["desbloqueado"]:
            return False

        if self.pontos_pesquisa >= tech["custo"]:
            self.pontos_pesquisa -= tech["custo"]
            tech["desbloqueado"] = True
            self.nivel_tecnologico += 1
            self.buffs_ativos.append(tech["buff"])
            print(obter_confirmacao("TECNOLOGIA_DESCOBERTA"))
            print(f"  -> Efeito: {tech['buff']}")
            return True
        return False

    def status_report(self):
        print("\n--- RELATÓRIO DE TECNOLOGIA ---")
        print(f"  Nível Tecnológico: {self.nivel_tecnologico}")
        print(f"  Pontos de Pesquisa: {self.pontos_pesquisa}")
        print("  Buffs Ativos:")
        for buff in self.buffs_ativos:
            print(f"    - {buff}")
        print("-----------------------------")


# =============================================================================
# SEÇÃO 4: CONCEITO DE BASE MILITAR
# =============================================================================

class BaseMilitar:
    """
    Representa a base de operações central do jogador. Gerencia defesas,
    construção de unidades e pode ser aprimorada.
    """
    def __init__(self, nome: str, comandante: str, economia: Economia):
        self.nome = nome
        self.comandante = comandante
        self.economia_link = economia  # Link direto para o sistema econômico
        self.nivel = 1
        self.defesa = 100
        self.unidades = []
        self.fila_construcao = []
        self.catalogo_unidades = {
            "Soldado": {"custo": {"metais": 50, "creditos": 100}, "tempo": 1},
            "Tanque": {"custo": {"metais": 200, "creditos": 300}, "tempo": 2}
        }

    def aprimorar_base(self):
        """Aprimora a base, gastando recursos para aumentar seu nível e defesas."""
        custo_upgrade = {"metais": 500 * self.nivel, "creditos": 1000 * self.nivel}
        if self.economia_link.gastar_recursos(custo_upgrade):
            self.nivel += 1
            self.defesa += 50
            print(obter_confirmacao("BASE_UPGRADE_SUCESSO"))
        else:
            print(obter_confirmacao("OPERACAO_FALHA"))

    def construir_unidade(self, nome_unidade: str):
        """Adiciona uma unidade à fila de construção se houver recursos."""
        unidade_blueprint = self.catalogo_unidades.get(nome_unidade)
        if not unidade_blueprint:
            return

        if self.economia_link.gastar_recursos(unidade_blueprint["custo"]):
            self.fila_construcao.append(nome_unidade)
            print(f"'{nome_unidade}' adicionado à fila de construção.")
        else:
            print(obter_confirmacao("OPERACAO_FALHA"))

    def processar_fila(self):
        """Processa a fila de construção e cria unidades."""
        if self.fila_construcao:
            unidade_construida = self.fila_construcao.pop(0)
            self.unidades.append(unidade_construida)
            print(obter_confirmacao("UNIDADE_CRIADA"))
            print(f"  -> Unidade pronta: {unidade_construida}")

    def status_report(self):
        print("\n--- RELATÓRIO DA BASE MILITAR ---")
        print(f"  Base: {self.nome} (Nível {self.nivel})")
        print(f"  Comandante: {self.comandante}")
        print(f"  Defesa: {self.defesa}")
        print(f"  Unidades Ativas: {len(self.unidades)}")
        print(f"  Fila de Construção: {len(self.fila_construcao)}")
        print("--------------------------------")


# =============================================================================
# SEÇÃO 5: DEMONSTRAÇÃO E SIMULAÇÃO
# =============================================================================

def simular_jogo():
    """
    Função principal que demonstra a interação entre os sistemas.
    """
    print("🚀 INICIANDO SIMULAÇÃO DE CONCEITOS AVANÇADOS 🚀")

    # 1. Inicialização dos Sistemas
    economia_jogador = Economia(owner="Comandante Supremo")
    tecnologia_jogador = Tecnologia()
    base_jogador = BaseMilitar(
        nome="Fortaleza Alpha",
        comandante="Comandante Supremo",
        economia=economia_jogador
    )
    ia_inimiga_personalidade = "AGRESSIVO"

    # 2. Simulação de alguns turnos
    for turno in range(1, 4):
        print(f"\n" + "="*50)
        print(f"========= TURNO {turno} =========")
        print("="*50)

        # Fase de Gestão do Jogador
        economia_jogador.processar_turno()
        tecnologia_jogador.adicionar_pontos_pesquisa(120)
        base_jogador.processar_fila()

        # Ações do Jogador (Exemplos)
        if turno == 1:
            base_jogador.construir_unidade("Soldado")
            tecnologia_jogador.pesquisar("IA Defensiva")
        if turno == 2:
            base_jogador.aprimorar_base()
            base_jogador.construir_unidade("Tanque")

        # Fase da IA (simulada com frases)
        print("\n--- Ações da IA Inimiga ---")
        if turno == 3:
            print(obter_frase_ia(ia_inimiga_personalidade, "declarar_guerra"))

        # Relatórios de final de turno
        economia_jogador.status_report()
        tecnologia_jogador.status_report()
        base_jogador.status_report()

    print("\n" + "="*50)
    print("✅ SIMULAÇÃO CONCLUÍDA ✅")


if __name__ == "__main__":
    simular_jogo()
