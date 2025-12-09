# src/systems/ai_npc.py

from src.systems.tecnologia import Tecnologia
from src.utils.log_protocol import LogSistema

class AI_NPC:
    def __init__(self, nome: str, personalidade: str, nivel: int, tech_base: Tecnologia):
        self.nome = nome
        self.personalidade = personalidade
        self.nivel = nivel
        self.tech_base = tech_base
        self.evo = 0

    def agir(self, forca_jogador: float, log: LogSistema):
        acao = self._decisao(forca_jogador)
        frase = self._frase_comportamental(acao, forca_jogador)
        log.registrar("IA_NPC", self.nome, frase)

        recompensa = 15 if "atacar" in acao else -5
        self._reforco(recompensa)
        return acao

    def _decisao(self, forca_do_jogador: float) -> str:
        if forca_do_jogador > 150 * self.nivel:
            return 'negociar' if self.personalidade == 'analítico' else 'defender'
        elif forca_do_jogador > 100 * self.nivel:
            return 'explorar'
        else:
            return 'atacar'

    def _frase_comportamental(self, acao: str, forca_jogador: float) -> str:
        if forca_jogador > 200:
            return f"[REATIVO] Nossa força não se compara. Protocolo de rendição."
        if forca_jogador > 100:
            return f"[ADAPTATIVO] Força notável. Reavaliando tática para aliança."
        else:
            return f"[AGRESSIVO] Eles são fracos! Ataque total!"

    def _reforco(self, recompensa: int):
        self.evo += recompensa
