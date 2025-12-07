import random

from nexus_utils.helpers import rank_xp, frase_confirmacao
from nexus_core.config import RACAS, CLASSES, ARMAS, VEICULOS, FUNCOES_BASE, TECNOLOGIAS


class Personagem:
    def __init__(self, nome, cargo="Jogador", classe=None, raca=None):
        self.nome = nome
        self.cargo = cargo
        self.raca = raca or random.choice(RACAS)
        self.classe = classe or random.choice(CLASSES)
        self.hp = 120 if cargo == "OWNER" else 100
        self.mana = 90 if cargo == "OWNER" else 50
        self.xp = 0
        self.nivel = 1
        self.rank = 'F'
        self.ouro = random.randint(200, 800)
        self.arma = random.choice(ARMAS)
        self.veiculo = random.choice(VEICULOS)
        self.fichas = []
        self.status_moral = random.choice(['Bom', 'Neutro', 'Mau'])
        self.vivo = True
        self.historico = []

    def agir(self, acao, alvo=None):
        if not self.vivo:
            return frase_confirmacao(self, "Ação negada (morto)", False, "\u001B[91m")
        if acao == "atacar" and alvo:
            dano = random.randint(15, 40)
            gasto = random.randint(10, 20)
            self.mana = max(0, self.mana - gasto)
            alvo.hp = max(0, alvo.hp - dano)
            self.xp += 35
            msg = f"{self.nome} atacou {alvo.nome} tirou {dano} HP."
            if alvo.hp == 0:
                alvo.vivo = False
                msg += " Inimigo derrotado!"
            self.historico.append(msg)
            return frase_confirmacao(self, msg, True)
        elif acao == "cura":
            self.hp = min(self.hp + 30, 120)
            self.mana = max(0, self.mana - 20)
            msg = f"{self.nome} se curou 30 HP."
            self.historico.append(msg)
            return frase_confirmacao(self, msg)
        elif acao == "explorar":
            ganho = random.randint(10, 80)
            self.ouro += ganho
            self.xp += 25
            msg = f"{self.nome} explorou, ganho {ganho} ouro."
            self.historico.append(msg)
            return frase_confirmacao(self, msg)
        return frase_confirmacao(self, "comando desconhecido", False, "\u001B[91m")

    def subir_nivel(self):
        if self.xp >= 400 * self.nivel:
            self.nivel += 1
            self.hp = 120 + 10 * self.nivel
            self.rank = rank_xp(self.xp)
            self.historico.append(f"Subiu para nível {self.nivel}")
            return frase_confirmacao(self, "subiu de nível!")
        return frase_confirmacao(self, "XP insuficiente - não subiu", False, "\u001B[91m")

    def ficha(self):
        return {
            "Nome": self.nome, "Cargo": self.cargo, "Raça": self.raca, "Classe": self.classe,
            "HP": self.hp, "Mana": self.mana, "XP": self.xp, "Ouro": self.ouro,
            "Rank": self.rank, "Nível": self.nivel, "Status": "Vivo" if self.vivo else "Morto",
            "Histórico Resumido": self.historico[-3:]
        }


class BaseMilitar:
    def __init__(self, nome, comandante):
        self.nome = nome
        self.comandante = comandante
        self.funcs = random.sample(FUNCOES_BASE, 3)
        self.tecnologias = random.sample(TECNOLOGIAS, 2)
        self.armas = random.sample(ARMAS, 2)
        self.veiculos = random.sample(VEICULOS, 1)
        self.recursos = {"Ouro": random.randint(1200, 4000), "Éter": random.randint(20, 80)}
        self.moral = random.choice(['Bom', 'Neutro', 'Mau'])

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
        preco = int(self.mercado.get(recurso, 1) * self.flutuacao / 15)
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
