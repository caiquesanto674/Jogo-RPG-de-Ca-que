"""
Módulo de Exceções Personalizadas para o Nexus Engine.
"""

class NexusError(Exception):
    """Exceção base para todos os erros do Nexus Engine"""
    pass

class EntityError(NexusError):
    """Erro relacionado a entidades"""
    pass

class EnergyError(NexusError):
    """Erro relacionado ao sistema de energia"""
    pass

class TimeError(NexusError):
    """Erro relacionado ao sistema de tempo"""
    pass
