# systems/base.py
from typing import List
from .tecnologia import Tecnologia

class ComponenteBase:
    def __init__(self, nome, consumo_mana, producao):
        self.nome = nome
        self.consumo_mana = consumo_mana
        self.producao = producao
        self.status="OPERACIONAL"

class BaseMilitar:
    def __init__(self, nome, owner, economia, pos=(5,5)):
        self.nome = nome
        self.owner = owner
        self.economia = economia
        self.recursos = economia.reservas
        self.tecnologia = Tecnologia()
        self.componentes: List[ComponenteBase] = []
        self.defesa_psiquica = 0.0
        self.escudo_psionico_ativo = False
        self.escudo_psionico_carga = 0
        self._inicializar()
    def _inicializar(self):
        self.componentes.append(ComponenteBase("Reator Éter Ω", 100, {'eter':500}))
        self.componentes.append(ComponenteBase("Lab SSSS", 200, {'materia_escura_ssss':50}))
        self.recursos.setdefault("Munição", 50)

    def ativar_escudo_psionico(self):
        """Ativa o escudo consumindo matéria escura SSSS."""
        if "Escudo Psiônico SSSS" not in self.tecnologia.arvore:
            print("A tecnologia do Escudo Psiônico SSSS não foi pesquisada.")
            return False

        custo_ativacao = 50
        if self.recursos.get('materia_escura_ssss', 0) >= custo_ativacao:
            self.recursos['materia_escura_ssss'] -= custo_ativacao
            self.escudo_psionico_ativo = True
            self.escudo_psionico_carga = 100  # Carga total
            print("🛡️ Escudo Psiônico SSSS ativado! Carga: 100%")
            return True
        else:
            print("Matéria Escura SSSS insuficiente para ativar o escudo.")
            return False

    def ciclo_base(self):
        consumo = sum(c.consumo_mana for c in self.componentes if c.status=="OPERACIONAL")
        producao = {}
        for c in self.componentes:
            if c.status=="OPERACIONAL":
                for r,q in c.producao.items():
                    producao[r]=producao.get(r,0)+q
        self.recursos['mana'] = self.recursos.get('mana',0)-consumo
        for r,q in producao.items():
            self.recursos[r]=self.recursos.get(r,0)+q
    def aplicar_upgrade_psiquico(self):
        custo = 30
        if self.recursos.get('materia_escura_ssss',0)>=custo:
            self.recursos['materia_escura_ssss'] -= custo
            self.defesa_psiquica = 0.5
            return True
        return False
