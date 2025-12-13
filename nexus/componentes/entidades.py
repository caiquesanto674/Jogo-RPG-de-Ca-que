# nexus/componentes/entidades.py
import logging
from typing import List

# Importando a função de confirmação de um futuro módulo de utilitários
from ..utils.helpers import confirmar


from typing import Optional, Tuple

from ..sistemas.tecnologia import Tecnologia
from .classes_unidades import CLASSES_APOLO


class UnidadeCombate:
    """Unidade militar com moral e arsenal."""

    def __init__(
        self,
        nome: str,
        classe: str,
        moral: int = 100,
        tech: Tecnologia = None,
        posicao: Optional[Tuple[int, int]] = None,
        poder_psicologico: Optional[str] = None,
        aliados_proximos: int = 0,
        level: int = 1,
        exp: int = 0,
    ):
        # 1. Carrega o perfil da classe do dicionário
        perfil = CLASSES_APOLO.get(classe)
        if not perfil:
            raise ValueError(f"Classe '{classe}' desconhecida.")

        self.nome = nome
        self.classe = classe
        self.moral = moral
        self.tech = tech or Tecnologia()
        self.posicao = posicao
        self.poder_psicologico = poder_psicologico
        self.aliados_proximos = aliados_proximos
        self.level = level
        self.exp = exp

        # 2. Atributos Táticos (Herdados da Classe)
        self.hp_max = perfil["Defesa_Base"]
        self.hp = self.hp_max
        self.forca_base = perfil["Forca_Base"]
        self.mobilidade = perfil["Mobilidade"]
        self.habilidade_especial = perfil["Habilidade_Especial"]

        # 3. Bônus Específicos da Classe
        self.alcance_bonus = perfil.get("Bonus_Alcance", 0)
        self.bonus_comando = perfil.get("Bonus_Comando", 0)

    def calcular_forca_belica(self, bonus_posicao: float = 0.0) -> float:
        """
        Calcula a Força Bélica final, integrando todos os sistemas:
        Classe, Moral, Tecnologia, Posição Tática e Bônus Psicológicos.
        """
        # Bônus de Tecnologia
        bonus_tech = 1.0
        # Simples, pois a tecnologia em nexus_unificado é apenas um nível
        if self.tech and self.tech.nivel > 1:
            bonus_tech += self.tech.nivel * 0.05

        # Bônus Psicológico e de Aliança
        bonus_psico = (
            self.aliados_proximos if self.poder_psicologico == "Comando" else 0
        ) * 0.25
        bonus_alianca = self.aliados_proximos * 5

        # Bônus Tático de Posição (do futuro GridCombat)
        bonus_tatico = 1.0 + bonus_posicao

        # Fórmula final consolidada
        forca_com_moral = self.forca_base * (self.moral / 100.0)
        forca_final = (
            forca_com_moral * bonus_tech * bonus_tatico
            + bonus_psico
            + bonus_alianca
        )
        return forca_final

    def atacar(self, alvo: "UnidadeCombate"):
        dano = max(1, int(self.calcular_forca_belica() - alvo.calcular_forca_belica() * 0.2))
        alvo.hp -= dano
        logging.info(f"[COMBATE] {self.nome} causou {dano} de dano em {alvo.nome}.")
        return dano

    def ganhar_exp(self, valor):
        self.exp += valor
        if self.exp >= 100 * self.level:
            self.level += 1
            self.exp = 0
            self.atk += 2
            self.hp += 10
            logging.info(f"[LEVEL UP] {self.nome} subiu para o nível {self.level}!")


class Inimigo(UnidadeCombate):
    def __init__(self, nome, level):
        super().__init__(nome, "Inimigo", level=level)
        # Ajusta a força base e o HP com base no nível
        self.forca_base += level * 2
        self.hp_max += level * 10
        self.hp = self.hp_max


class Guardiao:
    """Entidade semi-divina (Poderes Divinos/Sobrenaturais)."""

    def __init__(self, nome: str, poder_unico: str):
        self.nome = nome
        self.poder_unico = poder_unico
        self.atento = False

    def despertar(self):
        """Ativa o poder único do guardião."""
        if not self.atento:
            self.atento = True
            logging.info(confirmar("GUARDIAO", True))


class EnergiaBase:
    def __init__(self, energia_total=1000):
        self.energia_total = energia_total
        self.energia_atual = energia_total

    def consumir(self, valor):
        if valor <= self.energia_atual:
            self.energia_atual -= valor
            return True
        return False

    def recarregar(self, valor):
        self.energia_atual = min(self.energia_total, self.energia_atual + valor)


class BaseMilitar:
    """Base de Operações, Defesa e Recrutamento."""

    def __init__(self, nome: str):
        self.nome = nome
        self.nivel = 1
        self.recursos = {"aço": 1000, "mana": 300, "populacao": 200}
        self.defesa = 120
        self.unidades: List[UnidadeCombate] = []
        self.guardioes: List[Guardiao] = []
        self.energia = EnergiaBase(2000)
        self.suprimentos = 500

    def adicionar_guardiao(self, guardiao: Guardiao):
        self.guardioes.append(guardiao)

    def consumir_suprimentos(self, valor):
        if valor <= self.suprimentos:
            self.suprimentos -= valor
            return True
        return False


class MembroFamilia:
    """Sistema de Saga e Herança, gestão de herdeiros (Vida Escolar/Drama/Romance)."""

    def __init__(self, nome: str, talento: str):
        self.nome, self.talento = nome, talento
        self.herdeiros: List[MembroFamilia] = []

    def nova_geracao(self, herdeiro: "MembroFamilia"):
        self.herdeiros.append(herdeiro)
