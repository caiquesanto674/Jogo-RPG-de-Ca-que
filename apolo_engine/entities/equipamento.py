# Em apolo_engine/entities/equipamento.py


class Item:
    """Classe base para todos os itens."""

    def __init__(self, nome: str, tipo: str, peso: float):
        # ... atributos base ...
        self.nome = nome
        self.tipo = tipo
        self.peso = peso


class Arma(Item):
    """Define armas e seus modificadores de dano."""

    def calcular_dano_modificado(self, forca_base: int) -> int:
        """Aplica bônus e penalidades da arma."""
        # ... lógica de dano ...
        pass


def gerenciar_slots_equipamento(entidade: object, item: Item, slot: str) -> bool:
    """Tenta equipar ou desequipar um item em um slot específico (cabeça, peito, arma)."""
    # ... lógica de gestão de inventário e slots ...
    pass
