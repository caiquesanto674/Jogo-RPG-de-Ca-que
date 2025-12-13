# ============================================================
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
            self.node = loader.loadModel(self.model_path)
            self.node.reparentTo(parent)
        else:
            # Se não houver modelo, cria um nó vazio para posicionamento
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
        transform = self.owner.get(Transform)
        if transform:
            transform.position = self.node.getPos()
            transform.rotation = self.node.getHpr()


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


class StateIdle(AIState):
    def enter(self, entity):
        logger.info(f"{entity.name} está ocioso.")
        self.idle_time = time.time()

    def update(self, entity, dt):
        if time.time() - self.idle_time > 3:  # Fica ocioso por 3s
            entity.get(AIComponent).set_state(StatePatrol())


class StatePatrol(AIState):
    def enter(self, entity):
        logger.info(f"{entity.name} está patrulhando.")
        self.patrol_time = time.time()
        rb = entity.get(RigidBody)
        if rb:
            rb.node.applyCentralForce(Vec3(5, 0, 0))

    def update(self, entity, dt):
        if time.time() - self.patrol_time > 5:  # Patrulha por 5s
            entity.get(AIComponent).set_state(StateIdle())


# ============================================================
# GAME LOOP
# ============================================================

class NexusGame(ShowBase):
    """Loop principal estilo Unreal (Tick)."""
    def __init__(self):
        super().__init__()
        self.disableMouse()
        self.camera.setPos(0, -20, 20)
        self.camera.lookAt(0, 0, 0)
        self.entities: List[Entity] = []
        self.physics = PhysicsWorld()
        self.last_time = time.time()
        self.taskMgr.add(self.game_loop, "NexusLoop")

    def add_entity(self, entity: Entity):
        self.entities.append(entity)

        # Conecta a física ao mundo
        rb = entity.get(RigidBody)
        if rb:
            self.physics.world.attachRigidBody(rb.node)

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
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    logger.info("Inicializando NEXUS HYBRID ENGINE")
    game = NexusGame()

    # Cria o chão
    ground = Entity("Ground")
    ground_transform = ground.add_component(Transform, position=Vec3(0, 0, -1))
    ground_render = ground.add_component(RenderComponent, model_path="models/box.egg")
    ground_render.attach(game.render)
    # A escala do chão precisa ser grande
    ground_transform.scale = Vec3(20, 20, 1)

    # Física para o chão (estático)
    ground_shape = BulletBoxShape(Vec3(10, 10, 0.5))
    ground_node = BulletRigidBodyNode('GroundNode')
    ground_node.addShape(ground_shape)
    ground_np = game.render.attachNewNode(ground_node)
    ground_np.setPos(0, 0, -0.5)
    game.physics.world.attachRigidBody(ground_node)


    # Cria o jogador
    player = Entity("Player")
    player_transform = player.add_component(Transform, position=Vec3(0, 0, 5))
    player_render = player.add_component(RenderComponent, model_path="models/box.egg")
    player_render.attach(game.render)

    # Conecta física e renderização para o jogador
    player_rb = player.add_component(RigidBody, mass=1.0)
    player_rb_np = game.render.attachNewNode(player_rb.node)
    player_rb_np.setPos(player_transform.position)

    # Link a renderização para seguir a física
    player_render.node.reparentTo(player_rb_np)

    # Adiciona IA ao jogador
    player_ai = player.add_component(AIComponent)
    player_ai.set_state(StateIdle())

    game.add_entity(player)
    game.run()
