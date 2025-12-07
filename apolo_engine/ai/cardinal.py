# ai/cardinal.py
import random

class AICardinal:
    def __init__(self):
        self.nome = "CIEL ASCENDIDO"
        self.correcoes = 0
    def salvar_realidade(self, economia, player):
        if economia.reservas.get('comida',0) < 500 or economia.reservas.get('mana',0) < 300 or player.moral < 20:
            economia.reservas['comida'] = max(3000, economia.reservas.get('comida',0)+3000)
            economia.reservas['mana'] = max(1800, economia.reservas.get('mana',0)+1800)
            player.moral = 100.0
            self.correcoes += 1
            return True
        return False

class AI_NPC_Suporte:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
    def tomar_decisao_suporte(self, monarca, inimigo):
        if monarca.moral < 40 and monarca.base and monarca.base.defesa_psiquica < 0.5:
            monarca.base.aplicar_upgrade_psiquico()
            return 'ATIVAR_DEFESA_PSÍQUICA'
        if monarca.moral < 50:
            monarca.moral = min(100, monarca.moral +  random.randint(10,20))
            return 'RESTAURAR_MORAL'
        if inimigo and inimigo.hp>0:
            return 'ATACAR_INIMIGO'
        return 'IDLE'
