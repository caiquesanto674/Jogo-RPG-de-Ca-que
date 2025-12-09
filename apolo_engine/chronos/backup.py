"""
APOLO ENGINE – Módulo CRONOS
PARTE 7 – Sistema de Backup Automático e Proteção Temporal

Este módulo é responsável por garantir que NENHUM arquivo
do projeto será perdido, sobrescrito ou apagado sem registro.
"""

import os
import shutil
from datetime import datetime
from typing import List

class CronosBackup:
    def __init__(self, root: str = ".", backup_root: str = "./.apolo_backups"):
        self.root = root
        self.backup_root = backup_root

        if not os.path.exists(self.backup_root):
            os.makedirs(self.backup_root)

    # --------------------------------------------
    # CRIAR UM PONTO DE RESTAURAÇÃO COMPLETO
    # --------------------------------------------
    def create_snapshot(self) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        snapshot_path = os.path.join(self.backup_root, f"snapshot_{timestamp}")

        shutil.copytree(self.root, snapshot_path, dirs_exist_ok=True)

        return snapshot_path

    # --------------------------------------------
    # LISTAR TODOS OS SNAPSHOTS EXISTENTES
    # --------------------------------------------
    def list_snapshots(self) -> List[str]:
        if not os.path.exists(self.backup_root):
            return []
        return sorted(os.listdir(self.backup_root))

    # --------------------------------------------
    # RESTAURAR UM SNAPSHOT COMPLETO
    # --------------------------------------------
    def restore_snapshot(self, snapshot_name: str):
        snapshot_path = os.path.join(self.backup_root, snapshot_name)
        if not os.path.exists(snapshot_path):
            raise FileNotFoundError(f"Snapshot {snapshot_name} não existe.")

        # Restaurar tudo
        for item in os.listdir(snapshot_path):
            src = os.path.join(snapshot_path, item)
            dst = os.path.join(self.root, item)

            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
