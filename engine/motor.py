from src.sistemas import Economia, AICardinal, BaseMilitar
from src.entidades import MonarcaAbsoluto, Inimigo, AI_NPC_Suporte
from src.conflito import CorrecaoLog, ConflictResolver

# ===================== MOTOR FINAL — O CICLO UNIFICADO =====================
class Engine:
    def __init__(self):
        self.turno = 0
        self.economia = Economia()
        self.cardinal = AICardinal()
        self.base = BaseMilitar("CORE NEXUS AURORA", None, self.economia, (5, 5))
        self.protagonista = MonarcaAbsoluto("CAÍQUE APOLO Ω", self.base)
        self.base.owner = self.protagonista
        self.inimigos = [Inimigo("Lord Zarkon Ω", nivel_ameaca=90, poder_psicologico=True, pos=(10, 10))]
        self.aliados = [AI_NPC_Suporte("Calia Cardinal", "Clérigo", self.base)]
        self.log_manager = CorrecaoLog()

    def ciclo(self):
        self.turno += 1
        print(f"\n{'='*110}")
        print(f"                  CICLO {self.turno} — DOMÍNIO ABSOLUTO DO MONARCA CAÍQUE")

        # 1. Manutenção de Sistemas (Economia, Base, AI Cardinal)
        self.economia.ciclo_ganho()
        self.base.ciclo_base()
        self.cardinal.salvar_realidade(self.protagonista, self.economia)

        # 2. Ações do Protagonista (Poder)
        self.protagonista.ativar_volicao()

        # 3. Conflito (Combate Psicológico e Suporte)
        if self.inimigos:
            inimigo_atual = self.inimigos[0]

            inimigo_atual.usar_poder(self.protagonista)

            for aliado in self.aliados:
                aliado.tomar_decisao_suporte(self.protagonista, inimigo_atual)

            self.protagonista.agir('atacar', inimigo_atual)

        # 4. Simulação de Gerenciamento de Conflito de Código
        if self.turno == 2:
            conteudo_falso = "<<<<<<< HEAD \n Código Antigo \n ======= \n Código Novo da Feature \n >>>>>>> feature/nova-ia"

            if ConflictResolver.simular_leitura_arquivo(conteudo_falso)[0]:
                 self.log_manager.registrar_conflito("rpg_ai_feature.py", [1, 5])

                 _, decisao = ConflictResolver.resolver_conflito(conteudo_falso, "INCOMING")
                 self.log_manager.registrar_correcao("rpg_ai_feature.py", decisao)

                 print("\n🛠️ [IA CORREÇÃO ATIVADA]: Conflito de Código resolvido com sucesso pela IA de Assistência.")

        # 5. Relatório de Status
        print(f"\n--- STATUS CRÍTICO ---")
        print(f"  Moral: {self.protagonista.moral:.1f}/100 | Índice Dimensional: {self.protagonista.indice_dimensional:.2f}")
        print(f"  Defesa Psíquica SSSS: {self.base.defesa_psiquica * 100:.0f}% Ativa")
        self.log_manager.relatorio_status()
        print(f"{'='*110}")
