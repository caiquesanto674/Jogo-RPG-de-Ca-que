# main.py (na raiz do apolo_engine)
import time
from entities.entidade import MonarcaAbsoluto, Inimigo, AI_NPC_Suporte
from entities.veiculo import VeiculoDeCombate
from world.worldmap import WorldMap
from systems.economy import Economia
from systems.base import BaseMilitar
from ai.cardinal import AICardinal
from combat.combat import calcular_efeito_psiquico

def run_demo(turns: int = 3):
    eco = Economia()
    base = BaseMilitar("CORE NEXUS AURORA", None, eco, pos=(5,5))
    monarca = MonarcaAbsoluto("CAÍQUE APOLO Ω", base)
    base.owner = monarca
    inimigo = Inimigo("Lord Zarkon Ω", nivel_ameaca=90, pos=(15,15))
    veiculo = VeiculoDeCombate("Titã Ω", "Canhão de Éter", base, pos=(8,8))
    cardinal = AICardinal()
    aliado = AI_NPC_Suporte("Calia Cardinal", base)
    world = WorldMap(30,30)

    # Pesquisa e ativa o escudo
    base.tecnologia.pesquisar("Escudo Psiônico SSSS", base)
    base.ativar_escudo_psionico()

    for turno in range(1, turns+1):
        print(f"\n=== CICLO {turno} — DOMÍNIO APOLO ===")
        base.ciclo_base()
        eco.ciclo_ganho()

        # Ataque psicológico
        resultado = inimigo.usar_poder(monarca)
        if resultado['tipo'] == 'PSICOLOGICO':
            dano_base = resultado['valor']
            if base.escudo_psionico_ativo and base.escudo_psionico_carga > 0:
                print("🛡️ [ESCUDO PSÍQUICO] Ataque de Zarkon bloqueado! Carga do escudo drenada.")
                base.escudo_psionico_carga -= 34
                if base.escudo_psionico_carga <= 0:
                    base.escudo_psionico_ativo = False
                    print("⚠️ Escudo Psiônico SSSS desativado! Carga esgotada.")
            else:
                dano_final = calcular_efeito_psiquico(dano_base, base.defesa_psiquica)
                monarca.moral = max(0.0, monarca.moral - dano_final)
                monarca.humor = "dominado_psicologicamente"
                print(f"[ATAQUE PSÍQUICO] Zarkon aplica {dano_base:.2f} -> mitigado para {dano_final:.2f}. Moral do Monarca: {monarca.moral:.2f}")

        # Ações de suporte
        decisao_aliado = aliado.tomar_decisao_suporte(monarca, inimigo)
        if decisao_aliado == 'ATACAR_INIMIGO':
            print(aliado.agir('atacar', inimigo))

        if monarca.moral < 20:
            activated = monarca.ativar_volicao()
            if activated:
                print("⚡ AGONY OVERFLOW: Monarca absorveu a dor e cresceu.")

        # Veículo tenta atacar
        print(veiculo.mover(1,1, world))
        print(veiculo.atirar(inimigo, world))

        # Monarca ataca de volta
        print(monarca.agir('atacar', inimigo))
        if inimigo.hp <= 0:
            print("🎉 Lord Zarkon derrotado!")
            break

        cardinal.salvar_realidade(eco, monarca)
        # status
        print(f"Status -> Moral: {monarca.moral:.1f} | IndiceDim: {monarca.indice_dimensional:.2f} | Mana: {eco.reservas.get('mana')}")
        time.sleep(1.2)

if __name__ == "__main__":
    run_demo(4)
