# main.py (na raiz do apolo_engine)
import time
from entities.entidade import MonarcaAbsoluto, Inimigo
from entities.veiculo import VeiculoDeCombate
from world.worldmap import WorldMap
from systems.economy import Economia
from systems.base import BaseMilitar
from ai.cardinal import AICardinal, AI_NPC_Suporte
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

    for turno in range(1, turns+1):
        print(f"\n=== CICLO {turno} — DOMÍNIO APOLO ===")
        base.ciclo_base()
        eco.ciclo_ganho()

        # Ataque psicológico
        resultado = inimigo.usar_poder(monarca)
        if resultado['tipo'] == 'PSICOLOGICO':
            dano = calcular_efeito_psiquico(resultado['valor'], base.defesa_psiquica)
            print(f"[ATAQUE PSÍQUICO] Zarkon aplica {resultado['valor']:.2f} -> mitigado para {dano:.2f}. Moral antiga -> {monarca.moral:.2f}")

        # Ações de suporte
        aliado.tomar_decisao_suporte(monarca, inimigo)
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
