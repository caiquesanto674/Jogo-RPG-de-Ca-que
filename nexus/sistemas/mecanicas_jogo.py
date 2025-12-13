# nexus/sistemas/mecanicas_jogo.py
import logging
import random

# Importando a função de confirmação de um futuro módulo de utilitários
from ..utils.helpers import confirmar
from ..componentes.entidades import UnidadeCombate


class Economia:
    """Gerencia reservas, produção e inflação dinâmica do jogo (Mecânica Tycoon)."""

    def __init__(self):
        self.reservas = {
            "ouro": 5000,
            "aço": 3000,
            "mana": 800,
            "comida": 1500,
            "energia": 900,
        }
        self.producao_base = 2000
        self.inflacao = 1.0  # Base 1.0

    def operar(self):
        """Calcula produção e atualiza inflação."""
        producao_ajustada = int(
            self.producao_base * (2.0 - self.inflacao)
        )  # Penaliza com inflação alta
        if producao_ajustada < 0:
            producao_ajustada = 100

        for rec in self.reservas:
            self.reservas[rec] += int(producao_ajustada // len(self.reservas))

        # Inflação dinâmica: Varia 0.99 a 1.02 por turno
        self.inflacao *= 0.99 + random.random() * 0.03
        logging.info(f"[ECONOMIA] Reservas atualizadas. Inflação: {self.inflacao:.2f}")


class Ambiente:
    """Simula o ambiente do mapa, ciclo dia/noite e recursos locais."""

    def __init__(self, nome: str, tipo: str, ciclo: str = "dia"):
        self.nome, self.tipo, self.ciclo = nome, tipo, ciclo
        self.recursos = {"agua": 1000, "mana": 350, "sombra": 0, "lux": 120}

    def atualizar(self):
        """Alterna ciclo e ajusta recursos (ex: mana, lux, sombra)."""
        self.ciclo = "noite" if self.ciclo == "dia" else "dia"
        if self.ciclo == "noite":
            self.recursos["lux"] = max(0, self.recursos["lux"] - 90)
            self.recursos["sombra"] += 5
        else:
            self.recursos["lux"] += 90
            self.recursos["sombra"] = max(0, self.recursos["sombra"] - 2)


class Missao:
    def __init__(self, nome, dificuldade):
        self.nome = nome
        self.dificuldade = dificuldade
        self.recompensa = dificuldade * 25
        self.status = "pendente"

    def executar(self, personagem: UnidadeCombate):
        # Correção: A chance de sucesso agora é baseada na Força Bélica
        forca_personagem = personagem.calcular_forca_belica()
        chance = forca_personagem * random.uniform(0.8, 1.2)

        # A dificuldade agora é um multiplicador da força (ex: 10 * 8 = 80 de força necessária)
        if chance >= self.dificuldade * 8:
            personagem.ganhar_exp(self.recompensa)
            logging.info(f"[MISSÃO] {personagem.nome} completou '{self.nome}'.")
            self.status = "concluída"
            return True
        else:
            personagem.hp -= 10
            logging.info(f"[MISSÃO] {personagem.nome} falhou em '{self.nome}'.")
            self.status = "falhou"
            return False
