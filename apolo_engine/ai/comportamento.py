from enum import Enum, auto


class EstadoIA(Enum):
    """Define os possíveis estados de comportamento da IA da base."""
    CONSERVADOR = auto()  # Foco em acumular recursos, evitar riscos.
    EXPANSIONISTA = auto()  # Foco em crescimento e upgrade da base.
    DEFENSIVO = auto()  # Foco em se recuperar de danos, evitar gastos.


class ComportamentoBase:
    def __init__(self, estado_inicial: EstadoIA = EstadoIA.CONSERVADOR):
        self.estado_atual = estado_inicial
        print(f"[IA] Comportamento iniciado no estado: {self.estado_atual.name}")

    def definir_estado(self, novo_estado: EstadoIA):
        """Altera o estado de comportamento da IA."""
        if self.estado_atual != novo_estado:
            self.estado_atual = novo_estado
            print(f"[IA] Transição de estado para: {self.estado_atual.name}")
