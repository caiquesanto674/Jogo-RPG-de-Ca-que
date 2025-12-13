"""
Módulo de Funções Utilitárias e Helpers para o Nexus Engine.
"""

from nexus_engine.core.engine import NexusEngine
from nexus_engine.entities.entity import Entidade

def criar_entidade_padrao(nome: str, classe: str = "Guerreiro") -> Entidade:
    """
    Cria uma entidade com configurações padrão baseada na classe.
    """
    config_classes = {
        "Guerreiro": {"hp_base": 120, "energia_base": 400},
        "Mago": {"hp_base": 80, "energia_base": 800},
    }

    config = config_classes.get(classe, config_classes["Guerreiro"])
    entidade = Entidade(
        nome=nome,
        hp_base=config["hp_base"],
        energia_base=config["energia_base"]
    )

    return entidade
