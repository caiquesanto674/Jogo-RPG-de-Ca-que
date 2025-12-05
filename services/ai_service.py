from datetime import datetime


class AI_NPC:
    def __init__(self, nome='AI Suprema'):
        self.nome = nome
        self.log = []

    def registrar(self, personagem, acao):
        entrada = f"{personagem.nome} ({personagem.cargo}) fez {acao}."
        self.log.append((datetime.now(), entrada))

    def analisar(self, personagem):
        perfil = "agressivo" if personagem.xp > 150 else "neutro"
        return {"Nome": personagem.nome, "Cargo": personagem.cargo, "Perfil": perfil,
                "HP": personagem.hp, "Últimas ações": personagem.historico[-2:]}
