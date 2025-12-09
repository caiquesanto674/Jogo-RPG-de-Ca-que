"""
APOLO ENGINE – MÓDULO ATLAS
PARTE 8 – Sistema Anti-Pasta-Vazia e Fortificação Estrutural

O ATLAS monitora toda a estrutura do projeto,
criando pastas ausentes, restaurando âncoras
e impedindo que o sistema colapse.
"""

import os
from typing import List

class AtlasStructureGuard:
    def __init__(self, root: str = "apolo_engine"):
        self.root = root

        # Estrutura mínima obrigatória
        self.required_dirs = [
            "core",
            "systems",
            "entities",
            "ai",
            "world",
            "chronos",
            "diagnostic",
            "helpers",
            "config",
            "assets"
        ]

    # -------------------------------------------------------------------
    # CRIAR TODAS AS PASTAS OBRIGATÓRIAS
    # -------------------------------------------------------------------
    def ensure_structure(self):
        for d in self.required_dirs:
            full = os.path.join(self.root, d)
            if not os.path.exists(full):
                os.makedirs(full)

            self._ensure_anchor(full)

    # -------------------------------------------------------------------
    # CRIAR ARQUIVO ÂNCORA PARA IMPEDIR PASTAS VAZIAS
    # -------------------------------------------------------------------
    def _ensure_anchor(self, directory: str):
        anchor = os.path.join(directory, "__keep__.anchor")
        if not os.path.exists(anchor):
            with open(anchor, "w") as f:
                f.write(
                    "Arquivo âncora criado pelo ATLAS.\n"
                    "Impede que esta pasta fique vazia ou seja removida."
                )

    # -------------------------------------------------------------------
    # DETECTAR PASTAS PERIGOSAMENTE VAZIAS
    # -------------------------------------------------------------------
    def detect_empty_dirs(self) -> List[str]:
        empty = []
        for d in self.required_dirs:
            full = os.path.join(self.root, d)
            if os.path.exists(full) and len(os.listdir(full)) <= 1:
                empty.append(full)
        return empty

    # -------------------------------------------------------------------
    # RECUPERAR PASTAS VAZIAS AUTOMATICAMENTE
    # -------------------------------------------------------------------
    def repair_empty_dirs(self):
        for folder in self.detect_empty_dirs():
            self._ensure_anchor(folder)
