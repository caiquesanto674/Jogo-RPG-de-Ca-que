# -*- coding: utf-8 -*-
"""
Este módulo implementa um sistema de RPG de texto simples com combate por turnos,
gerenciamento de inventário, e diferentes tipos de inteligência artificial para
controlar os inimigos.
"""

import random
import datetime

# ==============================================================================
# 1. MÓDULOS PRINCIPAIS DO JOGO
# ==============================================================================

class SistemaDecisaoFonte:
    """
    Centraliza todas as regras e cálculos do jogo (o 'S.D.F').
    Esta classe atua como a 'fonte da verdade' para mecânicas como dano e cura,
    garantindo que as regras sejam consistentes em todo o jogo.
    """
    def __init__(self):
        """Inicializa o sistema com as regras de jogo padrão."""
        self.regras = {
            "dano_base": 10,
            "modificador_forca": 1.5,
            "cura_base_pocao": 20
        }

    def calcular_dano(self, forca):
        """
        Calcula o dano de um ataque com base na força da entidade.

        Args:
            forca (int): O valor de força da entidade que está atacando.

        Returns:
            float: O dano total calculado.
        """
        return self.regras["dano_base"] + (forca * self.regras["modificador_forca"])

    def calcular_cura(self):
        """
        Calcula a quantidade de vida que uma poção restaura.
        A cura inclui um pequeno fator aleatório para adicionar variabilidade.

        Returns:
            int: A quantidade total de vida restaurada.
        """
        return self.regras["cura_base_pocao"] + random.randint(0, 10)

class Item:
    """
    Representa um item que pode ser armazenado no inventário.

    Attributes:
        nome (str): O nome do item.
        tipo (str): A categoria do item (ex: "arma", "pocao", "acessorio").
    """
    def __init__(self, nome, tipo):
        """
        Inicializa um novo item.

        Args:
            nome (str): O nome do item.
            tipo (str): O tipo do item.
        """
        self.nome = nome
        self.tipo = tipo

class Inventario:
    """
    Gerencia a coleção de itens de uma entidade.
    Permite adicionar e remover itens do inventário.
    """
    def __init__(self):
        """Inicializa um inventário vazio."""
        self.itens = []

    def adicionar_item(self, item):
        """
        Adiciona um item ao inventário.

        Args:
            item (Item): O objeto Item a ser adicionado.
        """
        self.itens.append(item)
        print(f"  -> {item.nome} foi adicionado ao inventário.")

    def remover_item(self, item):
        """
        Remove um item do inventário.

        Args:
            item (Item): O objeto Item a ser removido.
        """
        self.itens.remove(item)

class MemoriaIA:
    """
    Armazena as experiências de uma entidade para tomada de decisão.
    A memória é dividida em curto prazo (eventos do turno) e longo prazo (fatos aprendidos).
    """
    def __init__(self):
        """Inicializa as memórias de curto e longo prazo."""
        self.memoria_curto_prazo = []
        self.memoria_longo_prazo = {}

    def adicionar_evento_curto_prazo(self, evento):
        """
        Adiciona um evento à memória de curto prazo.

        Args:
            evento (str): A descrição do evento.
        """
        self.memoria_curto_prazo.append(evento)

    def adicionar_fato_longo_prazo(self, chave, valor):
        """
        Adiciona um fato aprendido à memória de longo prazo.

        Args:
            chave (str): A chave que identifica o fato.
            valor (any): O valor do fato.
        """
        self.memoria_longo_prazo[chave] = valor
        print(f"  -> [Memória de Longo Prazo] Fato aprendido: {chave} = {valor}")

    def limpar_memoria_curto_prazo(self):
        """Limpa todos os eventos da memória de curto prazo."""
        self.memoria_curto_prazo = []

class Entidade:
    """
    Classe base para qualquer ser vivo no jogo (jogadores, inimigos, NPCs).

    Attributes:
        nome (str): O nome da entidade.
        forca (int): O atributo de força, usado para calcular dano.
        vida (int): Os pontos de vida atuais da entidade.
        inventario (Inventario): O inventário da entidade.
        memoria (MemoriaIA): A memória da entidade.
    """
    def __init__(self, nome, forca, vida):
        """
        Inicializa uma nova entidade.

        Args:
            nome (str): O nome da entidade.
            forca (int): O valor de força inicial.
            vida (int): O valor de vida inicial.
        """
        self.nome = nome
        self.forca = forca
        self.vida = vida
        self.inventario = Inventario()
        self.memoria = MemoriaIA()

    def atacar(self, outra_entidade, sistema_decisao):
        """
        Realiza uma ação de ataque contra outra entidade.

        Args:
            outra_entidade (Entidade): A entidade alvo do ataque.
            sistema_decisao (SistemaDecisaoFonte): O sistema de regras do jogo.
        """
        dano = sistema_decisao.calcular_dano(self.forca)
        print(f"  -> {self.nome} ataca {outra_entidade.nome} e causa {dano} de dano!")
        outra_entidade.vida -= dano
        outra_entidade.memoria.adicionar_evento_curto_prazo(f"{self.nome} atacou")

    def usar_pocao(self, sistema_decisao):
        """
        Usa uma poção do inventário para restaurar a vida.
        Procura por um item do tipo "pocao", o utiliza e o remove do inventário.

        Args:
            sistema_decisao (SistemaDecisaoFonte): O sistema de regras do jogo.
        """
        pocao_para_usar = None
        for item in self.inventario.itens:
            if item.tipo == "pocao":
                pocao_para_usar = item
                break

        if pocao_para_usar:
            cura = sistema_decisao.calcular_cura()
            self.vida += cura
            self.inventario.remover_item(pocao_para_usar)
            print(f"  -> {self.nome} usa {pocao_para_usar.nome} e recupera {cura} de vida. Vida atual: {self.vida}")
            self.memoria.adicionar_fato_longo_prazo("sabe_usar_pocao", True)
        else:
            print(f"  -> {self.nome} não tem poções para usar!")

class Personagem(Entidade):
    """Representa o jogador controlado por um humano."""
    def __init__(self, nome, forca, vida):
        super().__init__(nome, forca, vida)

class Inimigo(Entidade):
    """
    Representa um adversário controlado pela IA.

    Attributes:
        assistente_ia: A instância de IA que controla as ações do inimigo.
    """
    def __init__(self, nome, forca, vida, assistente_ia=None):
        super().__init__(nome, forca, vida)
        self.assistente_ia = assistente_ia

class Mundo:
    """
    Contém e gerencia todas as entidades e o ambiente do jogo.

    Attributes:
        entidades (list): A lista de entidades presentes no mundo.
        servico_gps (ServicoGPS): Um simulador de serviço de GPS.
        servico_tempo (ServicoDeTempo): Um simulador de serviço de tempo.
    """
    def __init__(self, servico_gps, servico_tempo):
        """
        Inicializa o mundo do jogo.

        Args:
            servico_gps: A instância do serviço de GPS.
            servico_tempo: A instância do serviço de tempo.
        """
        self.entidades = []
        self.servico_gps = servico_gps
        self.servico_tempo = servico_tempo

    def adicionar_entidade(self, entidade):
        """
        Adiciona uma entidade ao mundo.

        Args:
            entidade (Entidade): A entidade a ser adicionada.
        """
        self.entidades.append(entidade)

# ==============================================================================
# 2. MÓDULOS DE INTELIGÊNCIA ARTIFICIAL
# ==============================================================================

class AssistenteSupervisionado:
    """
    IA para tarefas com respostas previsíveis (ex: diálogos).
    Funciona com base em um conjunto de regras predefinidas.
    """
    def gerar_dialogo(self, situacao):
        """
        Gera uma linha de diálogo com base na situação atual.

        Args:
            situacao (str): O contexto para o diálogo (ex: "inicio_combate").

        Returns:
            str: A linha de diálogo gerada.
        """
        if situacao == "inicio_combate":
            return "Prepare-se para a batalha!"
        elif situacao == "fim_combate":
            return "Você venceu... desta vez."
        return "..."

class AssistenteReforco:
    """
    IA para tomada de decisão estratégica (ex: combate).
    Usa a memória e o estado do jogo para escolher a melhor ação.
    """
    def tomar_decisao_combate(self, inimigo, jogador):
        """
        Analisa o estado do combate e decide a próxima ação do inimigo.

        Args:
            inimigo (Inimigo): A instância do inimigo que está decidindo.
            jogador (Personagem): A instância do jogador.

        Returns:
            str: A ação a ser executada ("atacar" ou "usar pocao").
        """
        print(f"  -> [IA de Reforço] Analisando a situação...")
        if jogador.memoria.memoria_longo_prazo.get("sabe_usar_pocao"):
            print("  -> [IA de Reforço] O jogador pode se curar. É melhor manter a pressão com ataques.")
            return "atacar"
        if inimigo.vida < 30 and any(item.tipo == "pocao" for item in inimigo.inventario.itens):
            print("  -> [IA de Reforço] Vida baixa! É mais seguro usar uma poção.")
            return "usar pocao"
        return "atacar"

class AssistenteAutoSupervisionado:
    """
    IA para geração de conteúdo novo e criativo (ex: itens).
    Simula a capacidade de criar novos elementos para o jogo.
    """
    def __init__(self):
        """Inicializa a IA com um banco de dados de itens conhecidos."""
        self.banco_itens = [
            {"nome": "Espada Mágica", "tipo": "arma"},
            {"nome": "Elixir Revigorante", "tipo": "pocao"},
        ]

    def gerar_item_aleatorio(self):
        """
        Gera um novo item aleatório a partir do banco de itens.

        Returns:
            Item: Um novo objeto Item.
        """
        item_escolhido = random.choice(self.banco_itens)
        print(f"  -> [IA Auto-Supervisionada] Gerou um novo item: {item_escolhido['nome']}")
        return Item(item_escolhido['nome'], item_escolhido['tipo'])

# ==============================================================================
# 3. MÓDULOS DE SIMULAÇÃO E DIAGNÓSTICO
# ==============================================================================

class SistemaDeDiagnostico:
    """Ferramentas para monitorar a saúde do jogo e simular falhas."""
    def verificar_integridade(self, mundo):
        """
        Verifica a integridade das entidades no mundo.

        Args:
            mundo (Mundo): O mundo do jogo a ser verificado.
        """
        print("\n[Diagnóstico] Verificando integridade do sistema...")
        for entidade in mundo.entidades:
            if entidade.vida <= 0:
                print(f"[Diagnóstico] Alerta: Entidade '{entidade.nome}' com vida inválida.")

class ServicoGPS:
    """Simula um serviço de GPS para fornecer dados de localização."""
    def obter_localizacao(self):
        """
        Retorna uma coordenada de GPS fixa.

        Returns:
            tuple: Uma tupla com latitude e longitude.
        """
        return (-23.5505, -46.6333)

class ServicoDeTempo:
    """Simula um serviço de tempo para fornecer a data e hora atuais."""
    def obter_hora_atual(self):
        """
        Retorna a data e hora atuais.

        Returns:
            datetime: O objeto datetime atual.
        """
        return datetime.datetime.now()

# ==============================================================================
# 4. FUNÇÃO PRINCIPAL E LOOP DE JOGO
# ==============================================================================

def main():
    """
    Ponto de entrada principal do programa.
    Inicializa o jogo, gerencia o loop de combate e finaliza a execução.
    """
    # --- Inicialização ---
    print("--- INICIALIZANDO O SISTEMA DE RPG ---")
    sdf = SistemaDecisaoFonte()
    servico_gps = ServicoGPS()
    servico_tempo = ServicoDeTempo()
    mundo = Mundo(servico_gps=servico_gps, servico_tempo=servico_tempo)

    # Inicializa as IAs
    ia_supervisionada = AssistenteSupervisionado()
    ia_reforco = AssistenteReforco()
    ia_autossupervisionada = AssistenteAutoSupervisionado()

    # Cria as entidades do jogo
    jogador = Personagem("Herói", 10, 100)
    monstro = Inimigo("Ogro", 5, 80, assistente_ia=ia_reforco)
    mundo.adicionar_entidade(jogador)
    mundo.adicionar_entidade(monstro)

    # Adiciona itens iniciais aos inventários
    jogador.inventario.adicionar_item(ia_autossupervisionada.gerar_item_aleatorio())
    monstro.inventario.adicionar_item(Item("Poção de Cura Simples", "pocao"))

    # --- Início do Combate ---
    print("\n--- COMBATE INICIADO ---")
    print(f"{monstro.nome}: '{ia_supervisionada.gerar_dialogo('inicio_combate')}'\n")

    # Loop principal do combate
    while jogador.vida > 0 and monstro.vida > 0:
        # --- Turno do Jogador ---
        print(f"--- Turno do Jogador (Vida: {jogador.vida}) ---")
        monstro.memoria.limpar_memoria_curto_prazo()

        # Obtém a ação do jogador
        acao = input("O que você faz? (atacar / usar pocao): ").lower()
        if acao == "atacar":
            jogador.atacar(monstro, sdf)
        elif acao == "usar pocao":
            jogador.usar_pocao(sdf)
        else:
            print("Ação inválida!")
            continue

        if monstro.vida <= 0:
            break

        # --- Turno do Inimigo ---
        print(f"\n--- Turno do Inimigo (Vida: {monstro.vida}) ---")
        acao_ia = monstro.assistente_ia.tomar_decisao_combate(monstro, jogador)

        # Executa a ação da IA
        if acao_ia == "atacar":
            monstro.atacar(jogador, sdf)
        elif acao_ia == "usar pocao":
            monstro.usar_pocao(sdf)

        print("-" * 20)

    # --- Fim do Combate ---
    print("\n--- COMBATE FINALIZADO ---")
    if jogador.vida > 0:
        print(f"O {jogador.nome} foi vitorioso!")
        print(f"{monstro.nome}: '{ia_supervisionada.gerar_dialogo('fim_combate')}'")
    else:
        print(f"O {monstro.nome} foi vitorioso!")

if __name__ == "__main__":
    main()
