from src.economia import Economia
from src.tecnologia import Tecnologia
from src.unidades import BaseMilitar, Unidade, Arma
from src.log_global import LogGlobal
from src.sistema_auto_correcao import SistemaAutoCorrecao
from src.ia import AI_NPC
from src.ambiente import Ambiente
from src.aliados import SistemaAliados

class MotorJogo:
    def __init__(self):
        self.economia = Economia()
        self.tech = Tecnologia()
        self.base = BaseMilitar("Arcanum Prime")
        self.log = LogGlobal()
        self.sistema_correcao = SistemaAutoCorrecao()
        self.sistema_aliados = SistemaAliados(self.economia)
        self.agentes = [AI_NPC(f"Agente_{i}") for i in range(3)]
        self.base.adicionar_unidade(Unidade("Escudeiro", "Soldado", 65, [Arma("Fusil", 80, "energia")]))
        self.ambiente = Ambiente("Vale Sombrio", "floresta")

    def formar_alianca(self):
        if self.sistema_aliados.formar_alianca():
            self.base.aliados = self.sistema_aliados.aliados
            self.log.registrar("Sistema", f"Aliança formada! Total de aliados: {self.base.aliados}")
            return True
        self.log.registrar("Sistema", "Falha ao formar aliança. Recursos insuficientes.")
        return False

    def quebrar_alianca(self):
        if self.sistema_aliados.quebrar_alianca():
            self.base.aliados = self.sistema_aliados.aliados
            self.log.registrar("Sistema", f"Aliança quebrada! Total de aliados: {self.base.aliados}")
            return True
        self.log.registrar("Sistema", "Nenhuma aliança para quebrar.")
        return False

    def ciclo_turno(self, contexto="combate"):
        self.economia.operar()
        self.tech.pesquisar("Tech de Turno")
        self.ambiente.atualizar()
        self.sistema_correcao.corrigir(self.economia)
        forca_total = self.base.calcular_forca_belica_total()
        for agente in self.agentes:
            acao = agente.agir(self.ambiente.recursos, contexto, forca_total)
            self.log.registrar("AI_NPC", acao)
        print(f"Base: {self.base.nome} | Defesa: {self.base.defesa} | Aliados: {self.base.aliados} | Força Bélica: {forca_total:.2f}")
        print(f"AI Estado: {[a.evo for a in self.agentes]} | Economia: {self.economia.recursos}")
