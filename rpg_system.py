# -*- coding: utf-8 -*-

import random

class SistemaDecisaoFonte:
    def __init__(self):
        self.regras = {
            "dano_base": 10,
            "modificador_forca": 1.5,
            "cura_base_pocao": 20
        }

    def calcular_dano(self, forca):
        return self.regras["dano_base"] + (forca * self.regras["modificador_forca"])

    def calcular_cura(self):
        return self.regras["cura_base_pocao"] + random.randint(0, 10)

class Item:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo # ex: "arma", "pocao"

class Inventario:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)
        print(f"{item.nome} foi adicionado ao inventário.")

    def remover_item(self, item):
        self.itens.remove(item)

class Entidade:
    def __init__(self, nome, forca, vida):
        self.nome = nome
        self.forca = forca
        self.vida = vida
        self.inventario = Inventario()

    def atacar(self, outra_entidade, sistema_decisao):
        dano = sistema_decisao.calcular_dano(self.forca)
        print(f"{self.nome} ataca {outra_entidade.nome} e causa {dano} de dano!")
        outra_entidade.vida -= dano

    def usar_pocao(self, sistema_decisao):
        pocao = next((item for item in self.inventario.itens if item.tipo == "pocao"), None)
        if pocao:
            cura = sistema_decisao.calcular_cura()
            self.vida += cura
            self.inventario.remover_item(pocao)
            print(f"{self.nome} usa {pocao.nome} e recupera {cura} de vida. Vida atual: {self.vida}")
        else:
            print(f"{self.nome} não tem poções para usar!")


class Personagem(Entidade):
    def __init__(self, nome, forca, vida):
        super().__init__(nome, forca, vida)

class Inimigo(Entidade):
    def __init__(self, nome, forca, vida, assistente_ia=None):
        super().__init__(nome, forca, vida)
        self.assistente_ia = assistente_ia

class Mundo:
    def __init__(self):
        self.entidades = []

    def adicionar_entidade(self, entidade):
        self.entidades.append(entidade)

# --- Assistentes de I.A. (Versão Inicial) ---

class AssistenteSupervisionado:
    def gerar_dialogo(self, situacao):
        if situacao == "inicio_combate":
            return "Prepare-se para lutar!"
        elif situacao == "fim_combate":
            return "Você me derrotou... por enquanto."
        return "..."

class AssistenteReforco:
    def tomar_decisao_combate(self, inimigo, jogador):
        # Lógica simples: se a vida estiver baixa e tiver uma poção, cure-se. Senão, ataque.
        if inimigo.vida < 30 and any(item.tipo == "pocao" for item in inimigo.inventario.itens):
            return "usar pocao"
        else:
            return "atacar"

class AssistenteAutoSupervisionado:
    def __init__(self):
        self.banco_itens = [
            {"nome": "Espada Mágica", "tipo": "arma"},
            {"nome": "Elixir Revigorante", "tipo": "pocao"},
            {"nome": "Amuleto de Proteção", "tipo": "acessorio"},
            {"nome": "Adaga Afiada", "tipo": "arma"},
            {"nome": "Poção de Cura Maior", "tipo": "pocao"}
        ]

    def gerar_item_aleatorio(self):
        item_escolhido = random.choice(self.banco_itens)
        nome = item_escolhido["nome"]
        tipo = item_escolhido["tipo"]
        print(f"[IA Auto-Supervisionada] Gerou um novo item: {nome} ({tipo})")
        return Item(nome, tipo)


def main():
    # Inicialização do mundo e dos sistemas
    mundo = Mundo()
    sdf = SistemaDecisaoFonte()

    # Inicialização dos assistentes de IA
    ia_supervisionada = AssistenteSupervisionado()
    ia_reforco = AssistenteReforco()
    ia_autossupervisionada = AssistenteAutoSupervisionado()

    # Criação dos personagens
    jogador = Personagem("Herói", 10, 100)
    monstro = Inimigo("Ogro", 5, 80, assistente_ia=ia_reforco)

    mundo.adicionar_entidade(jogador)
    mundo.adicionar_entidade(monstro)

    # IA gera um item para o jogador
    item_inicial = ia_autossupervisionada.gerar_item_aleatorio()
    jogador.inventario.adicionar_item(item_inicial)
    monstro.inventario.adicionar_item(Item("Poção de Cura Simples", "pocao"))


    # Loop de combate
    print(f"{monstro.nome}: '{ia_supervisionada.gerar_dialogo('inicio_combate')}'")
    while jogador.vida > 0 and monstro.vida > 0:
        # Turno do Jogador
        acao_jogador = input("O que você faz? (atacar/usar pocao): ").lower()
        if acao_jogador == "atacar":
            jogador.atacar(monstro, sdf)
        elif acao_jogador == "usar pocao":
            jogador.usar_pocao(sdf)
        else:
            print("Ação inválida!")
            continue

        if monstro.vida <= 0:
            print(f"{monstro.nome}: '{ia_supervisionada.gerar_dialogo('fim_combate')}'")
            print(f"{monstro.nome} foi derrotado!")
            break

        # Turno do Inimigo (controlado pela IA)
        print("\n--- Turno do Inimigo ---")
        acao_inimigo = monstro.assistente_ia.tomar_decisao_combate(monstro, jogador)
        if acao_inimigo == "atacar":
            monstro.atacar(jogador, sdf)
        elif acao_inimigo == "usar pocao":
            monstro.usar_pocao(sdf)

        if jogador.vida <= 0:
            print(f"{jogador.nome} foi derrotado!")
            break

        print(f"\nVida do {jogador.nome}: {jogador.vida}")
        print(f"Vida do {monstro.nome}: {monstro.vida}\n")


if __name__ == "__main__":
    main()
