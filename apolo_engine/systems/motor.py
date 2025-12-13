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
        self.log.registrar("PODER", "HIERARQUIA", f"FB Total: {forca_total:.2f}")

        # 2. DECISÃO IA ADAPTATIVA
        acao_npc = self.npc_adversario.decisao(forca_total)
        frase_npc = self.npc_adversario.frase_comportamental(acao_npc, forca_total)
        self.log.registrar("IA", self.npc_adversario.nome, frase_npc)

        # 3. RESPOSTAS ESTRATÉGICAS
        self.executar_resposta_estrategica(acao_npc)

        # 4. PROTOCOLO DE SEGURANÇA
        codigo_sha = ProtocoloConfirmacao.gerar(
            acao_npc, self.npc_adversario.nome, self.npc_adversario.nivel
        )
        self.log.registrar("PROTOCOLO", "SHA-256", f"Código: {codigo_sha}")

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
        print("📊 DIAGNÓSTICO COMPLETO - SISTEMA CARDINALIS")
        print("=" * 60)
        print(f"💰 ECONOMIA: R$ {self.economia.reserva:,.0f}")
        print(
            f"⚙️  TECNOLOGIA: Plasma={self.tech.arvore['Plasma']} | IA={self.tech.arvore['IA']}"
        )
        print(f"🏰 BASE: Nível {self.base_principal.nivel}")
        print(
            f"💪 FORÇA BÉLICA TOTAL: {sum(u.calcular_forca_belica() for u in self.unidades):.2f}"
        )
        print(
            f"🤖 NPC LEGEON: {self.npc_adversario.registro_acoes[-1] if self.npc_adversario.registro_acoes else 'Inativo'}"
        )# ============================================================
# NEXUS HYBRID ENGINE
# Motor de Jogo 2D + 3D Unificado
# Arquitetura inspirada em Unreal + Python nativo (Panda3D)
# ============================================================
# Escopo:
# - Renderização 2D/3D
# - Loop principal
# - Física
# - IA
# - ECS (Entity Component System)
# - Segurança
# - Performance
# - Testes
# - Documentação
# ============================================================

"""
Este arquivo representa a BASE UNIFICADA do motor.
Ele foi projetado para crescer até dezenas de milhares de linhas
sem quebrar arquitetura.

Tecnologia alvo:
- Panda3D (render + janela + input)
- Bullet Physics (física)
- Python 3.11+
"""

# ============================================================
# Imports base
# ============================================================

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, Vec2, NodePath, ClockObject
from panda3d.bullet import BulletWorld, BulletRigidBodyNode, BulletBoxShape
import time
import uuid
import logging
from typing import Dict, List, Type, Optional

# ============================================================
# LOGGING GLOBAL
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s | %(message)s"
)

logger = logging.getLogger("NEXUS")

# ============================================================
# CORE — ENTITY COMPONENT SYSTEM (ECS)
# ============================================================

class Component:
    """Componente base."""
    def __init__(self, owner: 'Entity'):
        self.owner = owner

    def update(self, dt: float):
        pass


class Entity:
    """Entidade genérica (Actor-style Unreal)."""
    def __init__(self, name: str = "Entity"):
        self.id = uuid.uuid4()
        self.name = name
        self.components: Dict[Type[Component], Component] = {}

    def add_component(self, component_cls: Type[Component], *args, **kwargs):
        component = component_cls(self, *args, **kwargs)
        self.components[component_cls] = component
        return component

    def get(self, component_cls: Type[Component]):
        return self.components.get(component_cls)

    def update(self, dt: float):
        for c in self.components.values():
            c.update(dt)


# ============================================================
# TRANSFORM COMPONENT (2D + 3D)
# ============================================================

class Transform(Component):
    def __init__(self, owner, position=Vec3(0,0,0)):
        super().__init__(owner)
        self.position = position
        self.rotation = Vec3(0,0,0)
        self.scale = Vec3(1,1,1)


# ============================================================
# RENDER COMPONENT
# ============================================================

class RenderComponent(Component):
    """Suporta 2D (UI/sprites) e 3D (models)."""
    def __init__(self, owner, model_path: Optional[str] = None):
        super().__init__(owner)
        self.node: Optional[NodePath] = None
        self.model_path = model_path

    def attach(self, parent: NodePath):
        if self.model_path:
            self.node = parent.attachNewNode(self.owner.name)

    def update(self, dt: float):
        transform = self.owner.get(Transform)
        if self.node and transform:
            self.node.setPos(transform.position)
            self.node.setHpr(transform.rotation)
            self.node.setScale(transform.scale)


# ============================================================
# PHYSICS SYSTEM
# ============================================================

class PhysicsWorld:
    def __init__(self):
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

    def step(self, dt: float):
        self.world.doPhysics(dt)


class RigidBody(Component):
    def __init__(self, owner, mass=1.0):
        super().__init__(owner)
        shape = BulletBoxShape(Vec3(0.5,0.5,0.5))
        self.node = BulletRigidBodyNode(owner.name)
        self.node.setMass(mass)
        self.node.addShape(shape)

    def update(self, dt: float):
        pass


# ============================================================
# AI SYSTEM — FSM + Utility
# ============================================================

class AIState:
    def enter(self, entity): pass
    def update(self, entity, dt): pass
    def exit(self, entity): pass


class AIComponent(Component):
    def __init__(self, owner):
        super().__init__(owner)
        self.state: Optional[AIState] = None

    def set_state(self, state: AIState):
        if self.state:
            self.state.exit(self.owner)
        self.state = state
        self.state.enter(self.owner)

    def update(self, dt: float):
        if self.state:
            self.state.update(self.owner, dt)


# ============================================================
# GAME LOOP
# ============================================================

class NexusGame(ShowBase):
    """Loop principal estilo Unreal (Tick)."""
    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.entities: List[Entity] = []
        self.physics = PhysicsWorld()
        self.last_time = time.time()
        self.taskMgr.add(self.game_loop, "NexusLoop")

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def game_loop(self, task):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        for e in self.entities:
            e.update(dt)

        self.physics.step(dt)
        return task.cont


# ============================================================
# SECURITY LAYER
# ============================================================

class Security:
    """Validação de inputs, arquivos e scripts."""
    @staticmethod
    def validate_path(path: str) -> bool:
        return ".." not in path


# ============================================================
# PERFORMANCE
# ============================================================

class Profiler:
    def __init__(self):
        self.samples = []

    def record(self, dt):
        self.samples.append(dt)

    def average(self):
        return sum(self.samples)/len(self.samples) if self.samples else 0


# ============================================================
# TESTS (BASE)
# ============================================================

def test_entity_component():
    e = Entity("Test")
    t = e.add_component(Transform)
    assert t.position == Vec3(0,0,0)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    logger.info("Inicializando NEXUS HYBRID ENGINE")
    game = NexusGame()

    player = Entity("Player")
    player.add_component(Transform)
    player.add_component(AIComponent)

    game.add_entity(player)
    game.run()

