from apolo_engine.ambiente import Ambiente
from apolo_engine.economia import Economia
from apolo_engine.ia import AI_NPC
from apolo_engine.log_global import LogGlobal
from apolo_engine.sistema_auto_correcao import SistemaAutoCorrecao
from apolo_engine.systems.tecnologia import Tecnologia
from apolo_engine.entities.unidade import UnidadeMilitar


class Base:  # Placeholder for a future, more advanced Base class
    def __init__(self, nome):
        self.nome = nome
        self.unidades = []
        self.defesa = 120  # Keep a defense value for now

    def adicionar_unidade(self, unidade):
        self.unidades.append(unidade)


class MotorJogo:
    def __init__(self):
        self.economia = Economia()
        self.tech = Tecnologia()
        self.base = Base("Arcanum Prime")
        self.log = LogGlobal()
        self.sistema_correcao = SistemaAutoCorrecao()
        self.agentes = [AI_NPC(f"Agente_{i}") for i in range(3)]

        # We now create a 'Tanque' unit, which is a defined class
        tanque = UnidadeMilitar(nome="Tanque T-1", classe="Tanque", tech=self.tech)
        self.base.adicionar_unidade(tanque)

        self.ambiente = Ambiente("Vale Sombrio", "floresta")

    def ciclo_turno(self, contexto="combate"):
        self.economia.operar()
        self.tech.pesquisar("Tech de Turno")
        self.ambiente.atualizar()
        self.sistema_correcao.corrigir(self.economia)
        for agente in self.agentes:
            acao = agente.agir(self.ambiente.recursos, contexto)
            self.log.registrar("AI_NPC", acao)

        # Let's calculate and print the combined force of all units in the base
        forca_total = sum(u.calcular_forca_belica() for u in self.base.unidades)

        print(f"Base: {self.base.nome} | Defesa: {self.base.defesa} | Força Bélica Total: {forca_total:.2f}")
        print(f"AI Estado: {[a.evo for a in self.agentes]} | Economia: {self.economia.recursos}")
