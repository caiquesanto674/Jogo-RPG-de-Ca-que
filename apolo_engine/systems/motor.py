from typing import List

from ..entities.unidade import UnidadeMilitar
from ..entities.base import BaseMilitar
from ..systems.economy import Economia
from ..systems.tecnologia import Tecnologia
from ..ai.npc import AI_NPC
from ..systems.log import LogSistema, ProtocoloConfirmacao


class Engine_APOLO:
    def __init__(self, owner: str):
        self.owner = owner
        self.log = LogSistema()
        self.economia = Economia(reserva=100000)
        self.tech = Tecnologia()

        # Sistema de Múltiplas Bases
        self.bases = [
            BaseMilitar(owner, "Alpha Nexus", self.economia, nivel=2),
            BaseMilitar(owner, "Beta Centurion", self.economia, nivel=1),
        ]

        self.npc_adversario = AI_NPC("LEGEON", "analítico", 3, self.tech)

        # Unidades com poderes psicológicos e aliados (designadas para a primeira base)
        unidades_base_alpha = [
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
        self.bases[0].unidades = unidades_base_alpha

    def turno_completo(self):
        """Executa um turno completo integrando economia, subsistência e combate."""
        # 1. FASE ECONÔMICA E SUBSISTÊNCIA
        print("\n--- FASE ECONÔMICA ---")
        self.economia.gerar_renda_ciclo(self.bases)
        for base in self.bases:
            base.metabolismo_ciclo(self.tech)

        # 2. FASE MILITAR E IA
        print("\n--- FASE DE COMANDO ---")
        # Agrega unidades de todas as bases para o cálculo de força
        unidades_totais = [unidade for base in self.bases for unidade in base.unidades]
        forca_total = sum(u.calcular_forca_belica() for u in unidades_totais)
        self.log.registrar("PODER", "HIERARQUIA", f"FB Total: {forca_total:.2f}")

        acao_npc = self.npc_adversario.decisao(forca_total)
        frase_npc = self.npc_adversario.frase_comportamental(acao_npc, forca_total)
        self.log.registrar("IA", self.npc_adversario.nome, frase_npc)

        self.executar_resposta_estrategica(acao_npc, unidades_totais)

        # 3. PROTOCOLO DE SEGURANÇA
        codigo_sha = ProtocoloConfirmacao.gerar(
            acao_npc, self.npc_adversario.nome, self.npc_adversario.nivel
        )
        self.log.registrar("PROTOCOLO", "SHA-256", f"Código: {codigo_sha}")

    def executar_resposta_estrategica(
        self, acao_npc: str, unidades_totais: List[UnidadeMilitar]
    ):
        """Executa ações baseadas na decisão da IA adversária."""
        base_principal = self.bases[0]  # Ações estratégicas focam na base principal

        if acao_npc == "atacar":
            base_principal.expande("metal", 75, 7500)
            for unidade in unidades_totais:
                unidade.moral = max(60, unidade.moral - 8)
        elif acao_npc == "explorar":
            self.tech.pesquisar("IA")
            self.economia.transferir(2500, "Pesquisa Anti-Exploração")
        elif acao_npc == "negociar":
            self.economia.reserva += 5000

    def diagnostico_completo(self):
        """Relatório final detalhado de TODO o sistema."""
        print("\n" + "=" * 60)
        print("📊 DIAGNÓSTICO COMPLETO - SISTEMA CARDINALIS")
        print("=" * 60)
        print(f"💰 ECONOMIA: R$ {self.economia.reserva:,.0f}")
        print(
            f"⚙️  TECNOLOGIA: Plasma={self.tech.arvore['Plasma']} | IA={self.tech.arvore['IA']}"
        )

        unidades_totais = []
        for base in self.bases:
            print(
                f"🏰 BASE '{base.local}': Nível {base.nivel}, Saúde {base.saude_base:.1f}%, Eficiência {base.eficiencia_operacional:.2f}"
            )
            unidades_totais.extend(base.unidades)

        forca_total = sum(u.calcular_forca_belica() for u in unidades_totais)
        print(f"💪 FORÇA BÉLICA TOTAL: {forca_total:.2f}")
        print(
            f"🤖 NPC LEGEON: {self.npc_adversario.registro_acoes[-1] if self.npc_adversario.registro_acoes else 'Inativo'}"
        )
