from typing import List

from ..entities.unidade import UnidadeMilitar
from ..entities.base import BaseMilitar
from ..systems.economy import Economia
from ..systems.tecnologia import Tecnologia
from ..ai.npc import AI_NPC
from ..systems.log import LogSistema, ProtocoloConfirmacao, LogLevel


class Engine_APOLO:
    def __init__(self, owner: str):
        self.owner = owner
        self.log = LogSistema(nivel_minimo=LogLevel.INFO)
        self.economia = Economia(reserva=100000)
        self.tech = Tecnologia()
        self.base_principal = BaseMilitar(owner, "Alpha Nexus", self.economia)
        self.npc_adversario = AI_NPC("LEGEON", "analítico", 3, self.tech)

        # Unidades com poderes psicológicos e aliados
        self.unidades = [
            UnidadeMilitar(
                "Protagonista Omega",
                "Tanque",
                100,
                self.tech,
                poder_psicologico="Comando",
                aliados_proximos=3,
            ),
            UnidadeMilitar(
                "Escudeiro Psi",
                "Suporte_Psi",
                95,
                self.tech,
                poder_psicologico="Aura",
                aliados_proximos=2,
            ),
        ]
        self.base_principal.unidades = self.unidades

    def turno_completo(self):
        """Executa um turno completo com TODOS os sistemas."""
        # 1. CÁLCULO DE PODER HIERÁRQUICO
        forca_total = sum(u.calcular_forca_belica() for u in self.unidades)
        self.log.registrar("PODER", "HIERARQUIA", f"FB Total: {forca_total:.2f}", nivel=LogLevel.INFO)

        # 2. DECISÃO IA ADAPTATIVA
        acao_npc = self.npc_adversario.decisao(forca_total)
        frase_npc = self.npc_adversario.frase_comportamental(acao_npc, forca_total)
        self.log.registrar("IA", self.npc_adversario.nome, frase_npc, nivel=LogLevel.INFO)

        # 3. RESPOSTAS ESTRATÉGICAS
        self.executar_resposta_estrategica(acao_npc)

        # 4. PROTOCOLO DE SEGURANÇA (Nível DEBUG para não vazar info sensível)
        codigo_sha = ProtocoloConfirmacao.gerar(
            acao_npc, self.npc_adversario.nome, self.npc_adversario.nivel
        )
        self.log.registrar("PROTOCOLO", "SHA-256", f"Código: {codigo_sha}", nivel=LogLevel.DEBUG)

    def executar_resposta_estrategica(self, acao_npc: str):
        """Executa ações baseadas na decisão da IA adversária."""
        if acao_npc == "atacar":
            self.base_principal.expande("metal", 75, 7500)
            for unidade in self.unidades:
                unidade.moral = max(60, unidade.moral - 8)
        elif acao_npc == "explorar":
            self.tech.pesquisar("IA")
            self.economia.transferir(2500, "Pesquisa Anti-Exploração")
        elif acao_npc == "negociar":
            self.economia.reserva += 5000  # Ganho diplomático

    def diagnostico_completo(self):
        """Relatório final detalhado de TODO o sistema."""
        print("\n" + "=" * 60)
        print(" 📊 DIAGNÓSTICO COMPLETO DO IMPÉRIO CARDINALIS 📊")
        print("=" * 60)

        # Dados a serem exibidos
        economia_val = f"R$ {self.economia.reserva:,.0f}"
        tech_val = f"Plasma Nv.{self.tech.arvore['Plasma']} | IA Nv.{self.tech.arvore['IA']}"
        base_val = f"Nível {self.base_principal.nivel}"
        forca_val = f"{sum(u.calcular_forca_belica() for u in self.unidades):.2f}"
        npc_val = (
            self.npc_adversario.registro_acoes[-1][1].upper()
            if self.npc_adversario.registro_acoes
            else "INATIVO"
        )

        # Impressão formatada
        print(f" 💰 Economia...........: {economia_val}")
        print(f" ⚙️  Tecnologia.........: {tech_val}")
        print(f" 🏰 Base Principal.....: {base_val}")
        print(f" 💪 Força Bélica Total.: {forca_val}")
        print(f" 🤖 Adversário (LEGEON): {npc_val}")
        print("=" * 60)
