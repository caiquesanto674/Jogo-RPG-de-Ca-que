# APOLO ENGINE - ARQUIVO ÚNICO CONSOLIDADO
# ==========================================
# Este arquivo contém a base completa do motor APOLO + ATLAS + NEXUS
# Gerado a partir de toda a arquitetura discutida.

# ==========================
# 1. IMPORTAÇÕES BÁSICAS
# ==========================
import uuid
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

# ==========================
# 2. SISTEMA DE LOG GLOBAL
# ==========================
class ApoloLogger:
    def __init__(self):
        self.logs = []

    def registrar(self, mensagem: str, tipo: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{timestamp}] [{tipo}] {mensagem}"
        self.logs.append(log)
        print(log)

LOGGER = ApoloLogger()

# ==========================
# 3. SISTEMA DE EVENTOS
# ==========================
class Evento:
    def __init__(self, nome: str, dados: Dict[str, Any] = None):
        self.id = uuid.uuid4()
        self.nome = nome
        self.dados = dados or {}

class EventBus:
    def __init__(self):
        self.assinantes = {}

    def emitir(self, evento: Evento):
        LOGGER.registrar(f"Evento emitido: {evento.nome}")
        if evento.nome in self.assinantes:
            for callback in self.assinantes[evento.nome]:
                callback(evento)

    def ouvir(self, nome_evento: str, callback):
        if nome_evento not in self.assinantes:
            self.assinantes[nome_evento] = []
        self.assinantes[nome_evento].append(callback)

EVENTOS = EventBus()

# ==========================
# 4. SISTEMA ATLAS (MUNDO)
# ==========================
class AtlasMundo:
    def __init__(self, nome="AETHERIA"):
        self.nome = nome
        self.regioes = {}

    def criar_regiao(self, nome):
        LOGGER.registrar(f"Região criada: {nome}")
        self.regioes[nome] = {
            "npc": [],
            "objetos": [],
            "conexoes": []
        }

ATLAS = AtlasMundo()

# ==========================
# 5. NEXUS (PERSONAGENS)
# ==========================
class Personagem:
    def __init__(self, nome: str, classe: str):
        self.id = uuid.uuid4()
        self.nome = nome
        self.classe = classe
        self.hp = 100
        self.energia = 100
        LOGGER.registrar(f"Personagem criado: {nome} [{classe}]")

    def atacar(self, alvo):
        dano = random.randint(5, 25)
        alvo.hp -= dano
        LOGGER.registrar(f"{self.nome} atacou {alvo.nome} causando {dano} de dano")

# ==========================
# 6. SISTEMA DE ECONOMIA
# ==========================
class Economia:
    def __init__(self):
        self.saldo_global = 0
        self.registros = []

    def transacao(self, origem, destino, valor):
        self.saldo_global += valor
        self.registros.append((origem, destino, valor))
        LOGGER.registrar(f"Transação registrada: {origem} -> {destino} ({valor})")

ECONOMIA = Economia()

# ==========================
# 7. SISTEMA DE FÍSICA
# ==========================
class Fisica:
    def aplicar_forca(self, massa, aceleracao):
        return massa * aceleracao

FISICA = Fisica()

# ==========================
# 8. SISTEMA DE MISSÕES
# ==========================
class Missao:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
        self.progresso = 0
        LOGGER.registrar(f"Missão criada: {nome}")

    def atualizar(self, valor):
        self.progresso += valor
        LOGGER.registrar(f"Progresso da missão '{self.nome}' atualizado para {self.progresso}%")

# ==========================
# 9. MOTOR PRINCIPAL APOLO
# ==========================
class ApoloEngine:
    def __init__(self):
        LOGGER.registrar("APOLO Engine iniciado.")
        self.personagens = []
        self.missoes = []

    def registrar_personagem(self, personagem: Personagem):
        self.personagens.append(personagem)
        LOGGER.registrar(f"Personagem registrado no motor: {personagem.nome}")

    def registrar_missao(self, missao: Missao):
        self.missoes.append(missao)

    def atualizar(self):
        LOGGER.registrar("Ciclo de atualização do APOLO executado.")

# Instância global
APOLO = ApoloEngine()

# ==========================
# 10. EXEMPLO DE EXECUÇÃO

# ==========================
# 14. SISTEMA DE DIÁLOGO
# ==========================
class Dialogo:
    def __init__(self, personagem, linhas: List[str]):
        self.personagem = personagem
        self.linhas = linhas
        self.indice = 0
        LOGGER.registrar(f"Diálogo iniciado com {personagem.nome}")

    def proxima_linha(self):
        if self.indice < len(self.linhas):
            frase = self.linhas[self.indice]
            LOGGER.registrar(f"{self.personagem.nome}: {frase}")
            self.indice += 1
            return frase
        else:
            LOGGER.registrar("Diálogo encerrado.")
            return None

# 10. EXEMPLO DE EXECUÇÃO
# ==========================
if __name__ == "__main__":
    ATLAS.criar_regiao("Vale Inicial")

    p1 = Personagem("Kael", "Guerreiro")
    p2 = Personagem("Mira", "Arqueira")

    APOLO.registrar_personagem(p1)
    APOLO.registrar_personagem(p2)

    p1.atacar(p2)

    m1 = Missao("Defender o Vale", "Proteja o Vale Inicial de invasores.")
    APOLO.registrar_missao(m1)
    m1.atualizar(20)

    APOLO.atualizar()
# ==========================
# 13. SISTEMA DE IA AVANÇADA (NOVA PARTE)
# ==========================
class IAAvancada:
    def __init__(self, nivel:int = 1):
        self.nivel = nivel
        LOGGER.registrar(f"IA Avançada iniciada no nível {nivel}")

    def decidir_acao(self, personagem: Personagem, contexto: Dict[str, Any]):
        """
        Sistema simples de tomada de decisão baseado em nível.
        Nível maior = decisões mais complexas.
        """
        if self.nivel == 1:
            return "observando"
        elif self.nivel == 2:
            return "patrulhando"
        elif self.nivel == 3:
            if personagem.hp < 40:
                return "recuar"
            else:
                return "atacar"
        else:
            return "analisando"

# Instância global para uso
IA_GLOBAL = IAAvancada(3)
