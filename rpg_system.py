# -*- coding: utf-8 -*-

import random
import datetime

# ==============================================================================
# 1. MÓDULOS PRINCIPAIS DO JOGO
# ==============================================================================

class SistemaDecisaoFonte:
    """ Centraliza todas as regras e cálculos do jogo (o 'S.D.F'). """
    def __init__(self):
        self.regras = {
            "dano_base": 10,
            "modificador_forca": 1.5,
            "cura_base_pocao": 20
        }

    def calcular_dano(self, forca):
        """ Calcula o dano de um ataque com base na força da entidade. """
        return self.regras["dano_base"] + (forca * self.regras["modificador_forca"])

    def calcular_cura(self):
        """ Calcula a quantidade de vida que uma poção restaura. """
        return self.regras["cura_base_pocao"] + random.randint(0, 10)

class Item:
    """ Representa um item que pode ser armazenado no inventário. """
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo  # Ex: "arma", "pocao", "acessorio"

class Inventario:
    """ Gerencia a coleção de itens de uma entidade. """
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)
        print(f"  -> {item.nome} foi adicionado ao inventário.")

    def remover_item(self, item):
        self.itens.remove(item)

class MemoriaIA:
    """ Armazena as experiências de uma entidade para tomada de decisão. """
    def __init__(self):
        self.memoria_curto_prazo = []  # Eventos do turno atual
        self.memoria_longo_prazo = {}   # Fatos aprendidos que persistem

    def adicionar_evento_curto_prazo(self, evento):
        self.memoria_curto_prazo.append(evento)

    def adicionar_fato_longo_prazo(self, chave, valor):
        self.memoria_longo_prazo[chave] = valor
        print(f"  -> [Memória de Longo Prazo] Fato aprendido: {chave} = {valor}")

    def limpar_memoria_curto_prazo(self):
        self.memoria_curto_prazo = []

class Entidade:
    """ Classe base para qualquer ser vivo no jogo (jogadores, inimigos, NPCs). """
    def __init__(self, nome, forca, vida):
        self.nome = nome
        self.forca = forca
        self.vida = vida
        self.inventario = Inventario()
        self.memoria = MemoriaIA()

    def atacar(self, outra_entidade, sistema_decisao):
        """ Realiza uma ação de ataque contra outra entidade. """
        dano = sistema_decisao.calcular_dano(self.forca)
        print(f"  -> {self.nome} ataca {outra_entidade.nome} e causa {dano} de dano!")
        outra_entidade.vida -= dano
        outra_entidade.memoria.adicionar_evento_curto_prazo(f"{self.nome} atacou")

    def usar_pocao(self, sistema_decisao):
        """ Usa uma poção do inventário para restaurar a vida. """
        pocao = next((item for item in self.inventario.itens if item.tipo == "pocao"), None)
        if pocao:
            cura = sistema_decisao.calcular_cura()
            self.vida += cura
            self.inventario.remover_item(pocao)
            print(f"  -> {self.nome} usa {pocao.nome} e recupera {cura} de vida. Vida atual: {self.vida}")
            self.memoria.adicionar_fato_longo_prazo("sabe_usar_pocao", True)
        else:
            print(f"  -> {self.nome} não tem poções para usar!")

class Personagem(Entidade):
    """ Representa o jogador controlado por um humano. """
    def __init__(self, nome, forca, vida):
        super().__init__(nome, forca, vida)

class Inimigo(Entidade):
    """ Representa um adversário controlado pela IA. """
    def __init__(self, nome, forca, vida, assistente_ia=None):
        super().__init__(nome, forca, vida)
        self.assistente_ia = assistente_ia

class Mundo:
    """ Contém e gerencia todas as entidades e o ambiente do jogo. """
    def __init__(self, servico_gps, servico_tempo):
        self.entidades = []
        self.servico_gps = servico_gps
        self.servico_tempo = servico_tempo

    def adicionar_entidade(self, entidade):
        self.entidades.append(entidade)

# ==============================================================================
# 2. MÓDULOS DE INTELIGÊNCIA ARTIFICIAL
# ==============================================================================

class AssistenteSupervisionado:
    """ IA para tarefas com respostas previsíveis (ex: diálogos). """
    def gerar_dialogo(self, situacao):
        if situacao == "inicio_combate":
            return "Prepare-se para a batalha!"
        elif situacao == "fim_combate":
            return "Você venceu... desta vez."
        return "..."

class AssistenteReforco:
    """ IA para tomada de decisão estratégica (ex: combate). """
    def tomar_decisao_combate(self, inimigo, jogador):
        print(f"  -> [IA de Reforço] Analisando a situação...")
        if jogador.memoria.memoria_longo_prazo.get("sabe_usar_pocao"):
            print("  -> [IA de Reforço] O jogador pode se curar. É melhor manter a pressão com ataques.")
            return "atacar"
        if inimigo.vida < 30 and any(item.tipo == "pocao" for item in inimigo.inventario.itens):
            print("  -> [IA de Reforço] Vida baixa! É mais seguro usar uma poção.")
            return "usar pocao"
        return "atacar"

class AssistenteAutoSupervisionado:
    """ IA para geração de conteúdo novo e criativo (ex: itens). """
    def __init__(self):
        self.banco_itens = [
            {"nome": "Espada Mágica", "tipo": "arma"},
            {"nome": "Elixir Revigorante", "tipo": "pocao"},
        ]
    def gerar_item_aleatorio(self):
        item_escolhido = random.choice(self.banco_itens)
        print(f"  -> [IA Auto-Supervisionada] Gerou um novo item: {item_escolhido['nome']}")
        return Item(item_escolhido['nome'], item_escolhido['tipo'])

# ==============================================================================
# 3. MÓDULOS DE SIMULAÇÃO E DIAGNÓSTICO
# ==============================================================================

class SistemaDeDiagnostico:
    """ Ferramentas para monitorar a saúde do jogo e simular falhas. """
    def verificar_integridade(self, mundo):
        print("\n[Diagnóstico] Verificando integridade do sistema...")
        for entidade in mundo.entidades:
            if entidade.vida <= 0:
                print(f"[Diagnóstico] Alerta: Entidade '{entidade.nome}' com vida inválida.")

class ServicoGPS:
    """ Simula um serviço de GPS. """
    def obter_localizacao(self):
        return (-23.5505, -46.6333)

class ServicoDeTempo:
    """ Simula um serviço de tempo. """
    def obter_hora_atual(self):
        return datetime.datetime.now()

# ==============================================================================
# 4. FUNÇÃO PRINCIPAL E LOOP DE JOGO
# ==============================================================================

def main():
    """ Ponto de entrada principal do programa. """
    # --- Inicialização ---
    print("--- INICIALIZANDO O SISTEMA DE RPG ---")
    sdf = SistemaDecisaoFonte()
    servico_gps = ServicoGPS()
    servico_tempo = ServicoDeTempo()
    mundo = Mundo(servico_gps=servico_gps, servico_tempo=servico_tempo)

    ia_supervisionada = AssistenteSupervisionado()
    ia_reforco = AssistenteReforco()
    ia_autossupervisionada = AssistenteAutoSupervisionado()

    jogador = Personagem("Herói", 10, 100)
    monstro = Inimigo("Ogro", 5, 80, assistente_ia=ia_reforco)
    mundo.adicionar_entidade(jogador)
    mundo.adicionar_entidade(monstro)

    jogador.inventario.adicionar_item(ia_autossupervisionada.gerar_item_aleatorio())
    monstro.inventario.adicionar_item(Item("Poção de Cura Simples", "pocao"))

    # --- Início do Combate ---
    print("\n--- COMBATE INICIADO ---")
    print(f"{monstro.nome}: '{ia_supervisionada.gerar_dialogo('inicio_combate')}'\n")

    while jogador.vida > 0 and monstro.vida > 0:
        # --- Turno do Jogador ---
        print(f"--- Turno do Jogador (Vida: {jogador.vida}) ---")
        monstro.memoria.limpar_memoria_curto_prazo()
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
