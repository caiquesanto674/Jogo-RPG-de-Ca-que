from src.base_militar import BaseMilitar, VeiculoDeCombate
from src.classes import Inimigo, MonarcaAbsoluto
from src.economia import Economia
from src.ia import AI_NPC_Suporte, AICardinal
from src.universo import WorldMap
from src.utils import (
    MAPA_TAMANHO,
    CorrecaoLog,
    Diagnostico,
    auto_correction,
    gerar_codigo_confirmacao,
)


# ===================== MOTOR FINAL — O CICLO UNIFICADO (Engine) =====================
class NexusCore:
    def __init__(self):
        self.turno = 0
        self.economia = Economia()
        self.world_map = WorldMap(*MAPA_TAMANHO)
        self.cardinal = AICardinal()
        self.base = BaseMilitar("CORE NEXUS AURORA", None, self.economia, (5, 5))
        self.protagonista = MonarcaAbsoluto("CAÍQUE APOLO Ω", self.base)
        self.base.owner = self.protagonista
        self.inimigos = [Inimigo("Lord Zarkon Ω", nivel_ameaca=90, pos=(15, 15))]  # Posição longe
        self.aliados = [AI_NPC_Suporte("Calia Cardinal", base=self.base)]
        self.veiculos = [
            VeiculoDeCombate("Titã Ω", "Canhão de Éter", self.base, (8, 8), alcance_max=5)
        ]
        self.diagnostico = Diagnostico(self)
        self.log_manager = CorrecaoLog()
        self.base.veiculos = self.veiculos  # Link for diagnostics

    def ciclo(self):
        self.turno += 1
        print(f"\n{'='*110}")
        print(f"                  CICLO {self.turno} — DOMÍNIO ABSOLUTO DO MONARCA CAÍQUE")

        # 1. Sistemas de Suporte (Diagnóstico/Correção/Cardinal)
        self.diagnostico.check_integridade()
        auto_correction(self)
        self.cardinal.salvar_realidade(self.protagonista, self.economia)

        # 2. Manutenção Econômica e Base (Tycoon)
        self.economia.ciclo_ganho()
        self.base.ciclo_base()

        # 3. Ações do Protagonista (Poder)
        self.protagonista.ativar_volicao()

        # 4. Conflito Tático (Combate Psico-Bélico)
        if self.inimigos:
            inimigo_atual = self.inimigos[0]

            # A. Ação do Inimigo (Ataque Psicológico)
            inimigo_atual.usar_poder(self.protagonista)

            # B. Ação Bélica (Veículo) - Movimento e Ataque
            print("\n--- AÇÃO BÉLICA ---")
            for veiculo in self.veiculos:
                if self.turno == 1:
                    print(veiculo.mover(1, 1, self.world_map))  # Tenta mover
                print(veiculo.atirar(inimigo_atual, self.world_map))

            # C. Ação do Aliado (Suporte Tático Inteligente)
            print("\n--- SUPORTE TÁTICO ---")
            for aliado in self.aliados:
                aliado.tomar_decisao_suporte(self.protagonista, inimigo_atual)

            # D. Resposta do Protagonista
            self.protagonista.agir("atacar", inimigo_atual)

            if inimigo_atual.hp <= 0:
                print(
                    f"🎉 Vitória! {inimigo_atual.nome} foi erradicado. Novo Inimigo se aproxima..."
                )
                self.inimigos.pop(0)

        # 5. Relatório de Status
        print("\n--- STATUS CRÍTICO ---")
        print(
            f"  Moral: {self.protagonista.moral:.1f}/100 | "
            f"Índice Dimensional: {self.protagonista.indice_dimensional:.2f}"
        )
        print(f"  Defesa Psíquica SSSS: {self.base.defesa_psiquica * 100:.0f}% Ativa")
        print(
            f"  Recursos (M. Escura/Éter): "
            f"{self.economia.reservas['materia_escura_ssss']}/"
            f"{self.economia.reservas['eter']}"
        )

        codigo = gerar_codigo_confirmacao(
            "ASSALTO_FINAL", self.protagonista.cargo, self.base.tecnologia.nivel
        )
        print(f"  [PROTOCOLO]: Código de Confirmação Final: {codigo}")
        print(f"{'='*110}")
