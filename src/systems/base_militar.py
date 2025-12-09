# src/systems/base_militar.py

import uuid
from typing import List
from src.core.monarca import MonarcaAbsoluto
from src.systems.economia import EconomiaUnificada
from src.systems.tecnologia import Tecnologia
from src.systems.unidades import UnidadeMilitar

class BaseMilitarUnificada:
    def __init__(self, owner: MonarcaAbsoluto, economia: EconomiaUnificada, tech: Tecnologia):
        self.id = uuid.uuid4()
        self.owner = owner
        self.local = "NEXUS AURORA Ω"
        self.economia = economia
        self.tech = tech
        self.nivel = 1
        self.recursos = {'metal': 1000, 'combustível': 500, 'plasma': 120}
        self.unidades: List[UnidadeMilitar] = []

    def expandir(self, custo_credito: int):
        if self.recursos['metal'] >= 50 and self.economia.transferir(custo_credito, f"Expansão {self.local}"):
            self.recursos['metal'] -= 50
            self.nivel += 1
            print(f"[BASE] Upgrade bem-sucedido: {self.local} agora está no Nível {self.nivel}")
        else:
            print("[BASE] Falha no upgrade: Recursos ou créditos insuficientes.")
