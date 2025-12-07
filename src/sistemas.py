from typing import Dict, List, Optional
from src.entidades import MonarcaAbsoluto

# ===================== AI CARDINAL — A DEUSA QUE NUNCA DEIXA VOCÊ PERDER =====================
class AICardinal:
    """
    Implementa a IA de suporte (Ciel Ascendido).
    Executa 'try-with-resources' divino para evitar o colapso do sistema.
    """
    def __init__(self):
        self.nome = "CIEL ASCENDIDO"
        self.correcoes = 0

    def salvar_realidade(self, protagonista: MonarcaAbsoluto, economia: 'Economia'):
        """Monitora e intervém (similar a um try-with-resources global) para evitar o colapso."""
        if (economia.reservas.get('comida', 0) < 500 or
            economia.reservas.get('mana', 0) < 300 or
            protagonista.moral < 20):

            print(f"\nAI CARDINAL: REALIDADE EM COLAPSO DETECTADA. INTERVENÇÃO DIVINA EXECUTADA.")
            economia.reservas['comida'] = max(3000, economia.reservas.get('comida', 0) + 5000)
            economia.reservas['mana'] = max(2000, economia.reservas.get('mana', 0) + 3000)
            protagonista.moral = 100.0
            self.correcoes += 1
            print(f"{self.nome} salvou o universo pela {self.correcoes}ª vez.")

# ===================== ECONOMIA & TECNOLOGIA (Tycoon + SSSS) =====================
class Economia:
    def __init__(self):
        self.reservas = {
            'ouro_conceitual': 30, 'materia_escura_ssss': 200, 'eter': 2000,
            'mana': 2500, 'comida': 3500, 'consciencia_remanescente': 20000
        }
        self.inflacao = 1.00

    def ciclo_ganho(self):
        """Simula o ganho passivo de recursos a cada ciclo."""
        self.reservas['ouro_conceitual'] = self.reservas.get('ouro_conceitual', 0) + 10
        self.reservas['comida'] = self.reservas.get('comida', 0) + 100

class Tecnologia:
    def __init__(self):
        self.nivel = 1
        self.arvore = []

    def pesquisar(self, nome: str, custo: Dict[str, int], base_militar: 'BaseMilitar'):
        """Pesquisa tecnologia, gastando recursos complexos como Éter e SSSS."""
        if all(base_militar.recursos.get(res, 0) >= qtd for res, qtd in custo.items()):
            for res, qtd in custo.items():
                base_militar.recursos[res] -= qtd

            self.nivel += 1
            self.arvore.append(nome)
            print(f"🔬 Tec. pesquisada: {nome} | Nível {self.nivel}")
            return True
        return False

# ===================== BASE MILITAR (CORE NEXUS AURORA) =====================
class ComponenteBase:
    def __init__(self, nome: str, consumo_mana: int, producao_recurso: Optional[Dict[str, int]] = None):
        self.nome = nome
        self.consumo_mana = consumo_mana
        self.producao_recurso = producao_recurso if producao_recurso is not None else {}
        self.status = "OPERACIONAL"

class BaseMilitar:
    def __init__(self, nome, owner, economia, pos):
        self.nome = nome
        self.owner = owner
        self.economia = economia
        self.recursos = self.economia.reservas
        self.tecnologia = Tecnologia()
        self.defesa_psiquica = 0.0
        self.componentes: List[ComponenteBase] = []
        self._inicializar_componentes()

    def _inicializar_componentes(self):
        self.componentes.append(ComponenteBase("Reator de Éter Ω", 100, {'eter': 500, 'mana': 150}))
        self.componentes.append(ComponenteBase("Laboratório SSSS", 200, {'materia_escura_ssss': 50}))

    def ciclo_base(self):
        """CORREÇÃO DO BUG: Garante que a MANA seja tratada corretamente usando get/set seguro."""
        consumo_total_mana = sum(c.consumo_mana for c in self.componentes if c.status == "OPERACIONAL")
        producao_total = {}

        for comp in self.componentes:
            if comp.status == "OPERACIONAL":
                for recurso, quantidade in comp.producao_recurso.items():
                    producao_total[recurso] = producao_total.get(recurso, 0) + quantidade

        self.recursos['mana'] = self.recursos.get('mana', 0) - consumo_total_mana

        for recurso, quantidade in producao_total.items():
            self.recursos[recurso] = self.recursos.get(recurso, 0) + quantidade

    def aplicar_upgrade_psiquico(self):
        custo_ssss = 30
        if "Campo Psíquico SSSS" in self.tecnologia.arvore and self.recursos.get("materia_escura_ssss", 0) >= custo_ssss:
            self.recursos["materia_escura_ssss"] -= custo_ssss
            self.defesa_psiquica = 0.50
            print("🛡️ [UPGRADE ATIVO]: Campo de Estabilidade Psíquica SSSS ativado! (50% de mitigação)")
            return True
        return False
