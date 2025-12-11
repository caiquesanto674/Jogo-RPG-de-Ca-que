import random, uuid, math, hashlib, time
from datetime import datetime
from typing import Dict, List, Optional

# ===================== SISTEMAS DE DOMÍNIO E CLASSES =====================

class BaseMilitar:
    def __init__(self, owner, local, economia, nivel=1):
        self.id = uuid.uuid4()
        self.owner = owner
        self.local = local
        self.nivel = nivel
        # Recursos específicos da Base (usados para expansão e manutenção)
        self.recursos = {'metal': 1000, 'combustível': 500, 'plasma': 120}
        self.economia = economia # Referência ao sistema econômico central
        self.unidades: List[Unidade] = []

    def expande(self, recurso_base, valor_base, custo_credito):
        """Expande a base, usando recursos locais E Créditos centrais (Economia)."""
        if self.recursos.get(recurso_base, 0) >= valor_base and self.economia.reserva >= custo_credito:
            self.recursos[recurso_base] -= valor_base
            self.economia.transferir(custo_credito, f"Expansão {self.local}")
            self.nivel += 1
            print(f"[BASE] Upgrade bem-sucedido: {self.local} -> Nível {self.nivel}")
            return True
        else:
            print("[FALHA] Recursos ou Créditos insuficientes para expansão.")
            return False

class Unidade:
    def __init__(self, nome, tipo, forca_base, moral, tech: 'Tecnologia'):
        self.nome = nome
        self.tipo = tipo
        self.forca_base = forca_base
        self.moral = moral
        self.tech = tech # Referência ao sistema de tecnologia
        self.armas = []

    def calcular_forca_belica(self):
        """Calcula o poder da unidade com bônus tecnológico (Nível de Força Detalhado)."""
        bonus_tech = 1.0

        # Bônus por tecnologia (Exemplo: Plasma aumenta a Força de certos tipos)
        if self.tipo in ['tanque', 'drone'] and self.tech.arvore.get('Plasma', 0) > 1:
            bonus_tech += self.tech.arvore['Plasma'] * 0.15 # Aumento de 15% por nível de Plasma

        if self.tech.arvore.get('IA', 0) > 1:
            bonus_tech += self.tech.arvore['IA'] * 0.1 # Bônus de 10% de eficiência por IA

        forca_belica_total = self.forca_base * bonus_tech * (self.moral / 100)
        return forca_belica_total

    def receber_ordem(self, ordem, contexto):
        print(f"{self.nome} ({self.tipo}) executa: {ordem} | FB: {self.calcular_forca_belica():.2f}")

class Economia:
    def __init__(self, reserva=50000):
        self.reserva = reserva
        self.transacoes = []

    def transferir(self, valor, destino):
        if valor <= self.reserva:
            self.reserva -= valor
            self.transacoes.append({'destino': destino, 'valor': valor, 'momento': datetime.now().isoformat()})
            return True
        else:
            print('[ECONOMIA] Saldo insuficiente. Transação negada.')
            return False

class Tecnologia:
    def __init__(self):
        self.arvore: Dict[str, int] = {'IA': 1, 'Fusão': 0, 'Plasma': 1, 'Biotecnologia': 0}
        self.pesquisa = []

    def evoluir(self, ramo):
        if ramo in self.arvore:
            self.arvore[ramo] += 1
            print(f"[TECH] Tecnologia '{ramo}' evoluída para nível {self.arvore[ramo]}.")

class AI_NPC:
    def __init__(self, nome, personalidade, nivel, tech_base: Tecnologia):
        self.nome = nome
        self.personalidade = personalidade
        self.nivel = nivel
        self.tech_base = tech_base
        self.registro_acoes = []

    def decisao(self, forca_do_jogador):
        """Decisão da IA adaptativa baseada na Força Bélica (FB) do jogador."""

        # Fator de Comportamento (Refletindo a hierarquia de poder)
        if forca_do_jogador > 150 * self.nivel:
            acao = 'negociar' if self.personalidade == 'analítico' else 'defender'
        elif forca_do_jogador > 100 * self.nivel:
            acao = 'explorar'
        else:
            acao = 'atacar'

        self.registro_acoes.append((datetime.now().isoformat(), forca_do_jogador, acao))
        return acao

    def frase_comportamental(self, acao):
        frases = {
            'atacar': f"ALERTA! Iniciando ataque total com bônus de Plasma N{self.tech_base.arvore['Plasma']}.",
            'defender': "Reforçar posição e aguardar suporte Psiônico.",
            'negociar': "Solicitando trégua. Nível de Força Inimiga superior. Propondo acordo econômico.",
            'explorar': "Mapeando o território em busca de Minérios Raros."
        }
        return frases.get(acao, "Aguardando ordem superior.")

# ===================== LOGS E PROTOCOLOS DE SISTEMAS =====================

class LogSistema:
    def __init__(self):
        self.registros = []
    def registrar(self, tipo, origem, conteudo):
        entrada = {'momento': datetime.now().isoformat(), 'tipo': tipo, 'origem': origem, 'conteudo': conteudo}
        self.registros.append(entrada)
        print(f"[{tipo}] {origem}: {conteudo}")

class ProtocoloConfirmacao:
    @staticmethod
    def gerar(acao, agente, nivel):
        """Gera um código de confirmação SHA256 para rastrear ações (Segurança de Sistemas)."""
        s = f"{acao}|{agente}|{nivel}|{datetime.now().isoformat()}"
        return hashlib.sha256(s.encode()).hexdigest()

# ===================== MOTOR APOLO (ENGINE UNIFICADO) =====================

class Engine_APOLO:
    def __init__(self, owner):
        self.owner = owner
        self.economia = Economia()
        self.tech = Tecnologia()
        self.base = BaseMilitar(owner, 'Alpha Nexus', self.economia)
        self.log = LogSistema()
        self.npc = AI_NPC("LEGEON", "analítico", 3, self.tech)

        # Unidades do jogador (agora dependem da Tech)
        self.unidade_principal = Unidade("Protagonista Omega", "tanque", 100, 100, self.tech)
        self.base.unidades.append(self.unidade_principal)

    def turno(self):

        # 1. CÁLCULO INICIAL (Poder/Hierarquia)
        fb_jogador = self.unidade_principal.calcular_forca_belica()
        self.unidade_principal.receber_ordem("Manter Posição", "Status")

        # 2. DECISÃO DA IA (Comportamento Adaptativo)
        acao_npc = self.npc.decisao(fb_jogador)
        resposta_npc = self.npc.frase_comportamental(acao_npc)
        self.log.registrar("INFO", self.npc.nome, resposta_npc)

        # 3. AÇÕES (Economia, Militar, Tecnologia)
        if acao_npc == 'atacar':
            # Se atacado, o jogador deve expandir defensivamente (custo econômico/militar)
            self.base.expande('metal', 50, 5000)
            self.log.registrar("EVENTO", "BaseMilitar", "Expansão forçada (Defesa acionada).")
            self.unidade_principal.moral = max(50, self.unidade_principal.moral - 10) # Dano na moral

        elif acao_npc == 'explorar':
            # Se a IA explora, o jogador deve evoluir a tecnologia para neutralizar a vantagem
            self.tech.evoluir('IA')
            self.economia.transferir(1500, 'Pesquisa IA')
            self.log.registrar("EVENTO", "Economia", "Gastos em P&D para neutralizar exploração.")

        # 4. PROTOCOLO DE CONFIRMAÇÃO (Segurança/Sistemas)
        codigo_conf = ProtocoloConfirmacao.gerar(acao_npc, self.npc.nome, self.npc.nivel)
        self.log.registrar("PROTOCOLO", "Confirmação SHA-256", f"Código: {codigo_conf[:12]}...")

    def diagnostico(self):
        """Diagnóstico do estado do jogo (Nível de Força, Economia, Tecnologia)."""
        print("\n[[DIAGNÓSTICO FINAL DO SISTEMA CARDINALIS]]")
        print(f"**Nível de Força Protagonista:** {self.unidade_principal.calcular_forca_belica():.2f}")
        print(f"**Reserva Econômica:** Créditos {self.economia.reserva}")
        print(f"**Nível Plasma/IA:** {self.tech.arvore['Plasma']}/{self.tech.arvore['IA']}")
        print(f"**Base Nível:** {self.base.nivel}")

# ================== EXECUÇÃO SIMULADA =====================
if __name__ == "__main__":
    motor = Engine_APOLO('OWNER')

    # Preparação: Evoluir tecnologia para dar bônus na Força Bélica
    motor.tech.evoluir('Plasma') # Nível 2
    motor.tech.evoluir('Plasma') # Nível 3
    motor.tech.evoluir('IA')     # Nível 2
    motor.tech.evoluir('IA')     # Nível 3

    for i in range(3):
        print(f"\n{'='*20} TURNO {i+1} {'='*20}")
        motor.turno()
        time.sleep(0.5)

    print("\n== FIM DA SIMULAÇÃO (MOTOR APOLO) ==")
    motor.diagnostico()