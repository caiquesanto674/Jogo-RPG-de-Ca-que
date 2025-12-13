# -*- coding: utf-8 -*-

import random

# Importações necessárias
from motor_apolo.entidades.entidade import Entidade
from motor_apolo.sistemas.inventario import Item

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
    def tomar_decisao_combate(self, inimigo: Entidade, jogador: Entidade):
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
