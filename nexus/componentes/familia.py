from typing import List


class MembroFamilia:
    """Sistema de Saga e Herança, gestão de herdeiros (Vida Escolar/Drama/Romance)."""

    def __init__(self, nome: str, talento: str):
        self.nome, self.talento = nome, talento
        self.herdeiros: List[MembroFamilia] = []

    def nova_geracao(self, herdeiro: "MembroFamilia"):
        self.herdeiros.append(herdeiro)
