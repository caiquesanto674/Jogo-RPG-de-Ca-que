# -*- coding: utf-8 -*-
# =============== ARQUIVO CONCEITO: SUPREMO_RPG_AI_X.py ===============
# Inspirado, consolidado e melhorado a partir de toda nossa conversa

import random
from datetime import datetime

# 1. --- CONFIGURAÇÃO GLOBAL, HIERARQUIA E CONTA DO OWNER ---
CLASSES   = ['Guerreiro', 'Mago', 'Comandante', 'Engenheiro', 'Assassino', 'Espadachim', 'Clérigo']
RACAS     = ['Humano', 'Elfo', 'Orc', 'Demônio', 'Androide', 'IA']
ARMAS     = ['Espada', 'Lança', 'Arco', 'Fuzil', 'Varinha', 'Canhão']
VEICULOS  = ['Cavalo', 'Dragão', 'Moto', 'Tanque', 'Mecha', 'Nave']
TECNOLOGIAS=['Campo de Força','Nanobot','Bombardeio Orbital','Teleportador','IA Defensiva']
FUNCOES_BASE = ['Forja', 'Centro Médico', 'Arsenal', 'Laboratório','Hangar']
CARGOS = [
    'OWNER', 'Administrador', 'Diretor', 'Master GM', 'Game Master', 'Moderador', 'Jogador'
]
MORAL = ['Bom', 'Neutro', 'Mau', 'Caótico', 'Ordem']

def rank_xp(xp):
    limites = [100, 500, 1000, 2500, 8000, 18000, 30000, 70000, 99999999]
    tags = ['F','E','D','C','B','A','S','SS','Lenda']
    for i,v in enumerate(limites):
        if xp < v: return tags[i]
    return tags[-1]

class ContaUsuario:
    def __init__(self, email, senha, cargo):
        self.email = email
        self.senha = senha
        self.cargo = cargo
    def autenticar(self, email, senha):
        return (self.email==email) and (self.senha==senha)
    def alterar_senha(self, senha_atual, nova_senha):
        if self.senha == senha_atual:
            self.senha = nova_senha
            print('\u001B[91mSenha trocada com sucesso!\u001B[0m')
        else:
            print('\u001B[91mFalha na troca de senha: senha atual incorreta.\u001B[0m')

OWNER = ContaUsuario("caiquesanto674@gmail.com", "edson4020SS", "OWNER")

# 2. --- FRASES DE LOG / FEEDBACK EM COR ---
def frase_confirmacao(personagem, acao, sucesso=True, cor="\u001B[92m"):
    status = "Sucesso" if sucesso else "Falha"
    return f"{cor}[{personagem.nome}-{personagem.cargo}] {acao} - {status}\u001B[0m"

# 3. --- ITENS & INVENTÁRIO ---
class Item:
    def __init__(self, nome, tipo, poder=0, efeito=None):
        self.nome = nome
        self.tipo = tipo
        self.poder = poder
        self.efeito = efeito or "Nenhum efeito"

class Inventario:
    def __init__(self):
        self.itens = []
    def adicionar(self, item):
        self.itens.append(item)
    def remover(self, nome):
        for i in self.itens:
            if i.nome == nome: self.itens.remove(i)
    def lista(self):
        return [(i.nome, i.tipo, i.poder) for i in self.itens]

# 4. --- OBJETOS DO JOGO ---
class Personagem:
    def __init__(self, nome, cargo="Jogador", classe=None, raca=None):
        self.nome = nome
        self.cargo = cargo
        self.raca = raca or random.choice(RACAS)
        self.classe = classe or random.choice(CLASSES)
        self.hp = 120 if cargo=="OWNER" else 100
        self.mana = 90 if cargo=="OWNER" else 50
        self.xp = 0
        self.nivel = 1
        self.rank = 'F'
        self.ouro = random.randint(200,800)
        self.arma = random.choice(ARMAS)
        self.veiculo = random.choice(VEICULOS)
        self.status_moral = random.choice(MORAL)
        self.vivo = True
        self.historico = []
        self.inventario = Inventario()
    def agir(self, acao, alvo=None):
        if not self.vivo:
            return frase_confirmacao(self, "Ação negada (morto)", False, "\u001B[91m")
        if acao == "atacar" and alvo:
            dano = random.randint(15,40)
            gasto = random.randint(10, 20)
            self.mana = max(0, self.mana-gasto)
            alvo.hp = max(0, alvo.hp-dano)
            self.xp += 35
            msg = f"{self.nome} atacou {alvo.nome} tirou {dano} HP."
            if alvo.hp==0: alvo.vivo=False; msg+=" Inimigo derrotado!"
            self.historico.append(msg)
            return frase_confirmacao(self, msg, True)
        elif acao == "cura":
            self.hp = min(self.hp+30, 120)
            self.mana = max(0, self.mana-20)
            msg = f"{self.nome} se curou 30 HP."
            self.historico.append(msg)
            return frase_confirmacao(self, msg)
        elif acao == "explorar":
            ganho = random.randint(10,80)
            self.ouro += ganho
            self.xp += 25
            msg = f"{self.nome} explorou, ganho {ganho} ouro."
            self.historico.append(msg)
            return frase_confirmacao(self, msg)
        elif acao == "adquirir_item":
            novo_item = Item("Poção de Cura", "Poção", 30, "Cura 30HP")
            self.inventario.adicionar(novo_item)
            msg = f"{self.nome} adquiriu uma {novo_item.nome}."
            self.historico.append(msg)
            return frase_confirmacao(self, msg, True)
        return frase_confirmacao(self, "comando desconhecido", False, "\u001B[91m")
    def subir_nivel(self):
        if self.xp >= 400*self.nivel:
            self.nivel += 1
            self.hp = 120 + 10*self.nivel
            self.rank = rank_xp(self.xp)
            self.historico.append(f"Subiu para nível {self.nivel}")
            return frase_confirmacao(self, "subiu de nível!")
        return frase_confirmacao(self, "XP insuficiente - não subiu", False, "\u001B[91m")
    def ficha(self):
        return {
            "Nome": self.nome,"Cargo": self.cargo,"Raça": self.raca,"Classe": self.classe,
            "HP": self.hp,"Mana": self.mana,"XP": self.xp,"Ouro": self.ouro,
            "Rank": self.rank, "Nível": self.nivel, "Status": "Vivo" if self.vivo else "Morto",
            "Inventário": self.inventario.lista(),
            "Histórico Resumido": self.historico[-3:]
        }

# 5. --- BASE MILITAR, ECO, TECNOLOGIA, ANÁLISE ===
class BaseMilitar:
    def __init__(self, nome, comandante):
        self.nome = nome
        self.comandante = comandante
        self.funcs = random.sample(FUNCOES_BASE, 3)
        self.tecnologias = random.sample(TECNOLOGIAS, 2)
        self.armas = random.sample(ARMAS, 2)
        self.veiculos = random.sample(VEICULOS, 1)
        self.recursos = {"Ouro": random.randint(1200, 4000), "Éter": random.randint(20, 80)}
        self.moral = random.choice(MORAL)
    def status(self):
        return {
            "Base": self.nome, "Comandante": self.comandante.nome, "Funções": self.funcs,
            "Tecnologias": self.tecnologias, "Armas": self.armas, "Veículos": self.veiculos,
            "Recursos": self.recursos, "Moral": self.moral
        }

class Economia:
    def __init__(self):
        self.mercado = {"Ouro": 4000, "Éter": 120, "Cristal": 30}
        self.flutuacao = 1.0
    def transacao(self, recurso, qtd, player):
        preco = int(self.mercado.get(recurso,1)*self.flutuacao/15)
        total = preco * max(1, qtd)
        player.ouro -= total
        self.mercado[recurso] -= qtd
        txt = f"{player.nome} comprou {qtd} {recurso} por {total} ouro."
        player.historico.append(f"COMÉRCIO: {txt}")
        return txt

class Tecnologia:
    def __init__(self):
        self.nivel = 1
        self.inovacoes = []
    def pesquisar(self, tech):
        self.nivel += 1
        self.inovacoes.append(tech)
        return f"Nova tecnologia desbloqueada: {tech} (Nível {self.nivel})!"

# 6. --- AI ANALYTICS & NPC ---
class AI_NPC:
    def __init__(self, nome='AI Suprema'):
        self.nome = nome
        self.log = []
    def registrar(self, personagem, acao):
        entrada = f"{personagem.nome} ({personagem.cargo}) fez {acao}."
        self.log.append((datetime.now(), entrada))
        return f"LOG: {entrada}"
    def analisar(self, personagem):
        perfil = "agressivo" if personagem.xp > 150 else "neutro"
        return {"Nome": personagem.nome,"Cargo": personagem.cargo,"Perfil":perfil,
                "HP": personagem.hp, "Últimas ações": personagem.historico[-2:]}

# 7. --- TESTES, EXEMPLO DE USO, OWNER, ETC ---
if __name__ == "__main__":
    # Dono cria, loga, e tem poderes supremos
    print("==== SUPREMO RPG AI (DEMO) ====")
    owner = Personagem("Caíque", cargo="OWNER")
    ai = AI_NPC()
    eco = Economia()
    tec = Tecnologia()
    base = BaseMilitar("Bastião da Verdade", owner)
    npc = Personagem("Maria", cargo="Game Master", classe="Mago", raca="Elfo")
    vilao = Personagem("Ezren", classe="Assassino")

    print("--- OWNER/ADMIN ---")
    print(owner.ficha())
    print(ai.analisar(owner))
    print(owner.agir("explorar"))
    print(owner.agir("atacar", vilao))
    print(owner.agir("adquirir_item"))
    print(eco.transacao("Éter", 2, owner))
    print(tec.pesquisar("IA Defensiva Quântica"))
    print(base.status())
    print(ai.registrar(owner,"alterou a cosmologia do mundo!"))
    print(owner.subir_nivel())
    print("--- NPC TESTE ---")
    print(npc.ficha())
    print(npc.agir("cura"))
    print("--- VILÃO ---")
    print(vilao.ficha())
    print("--- LOG ANALYTICS ---")
    for t, log in ai.log[-3:]:
        print(f"[{t.strftime('%H:%M')}] {log}")

# RESUMO:
# Este arquivo centraliza todos os poderes, funções, hierarquia, conta OWNER, feedback, combate, economia, teste e análise AI do RPG. Pode ser expandido para interface visual, menus, multiplayer e eventos avançados. Você é identificado e tratado como Fundador/Dono/OWNER, com permissão total, logs especiais e comandos exclusivos.
