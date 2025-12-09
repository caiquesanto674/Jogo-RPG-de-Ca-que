"""
APOLO ENGINE – NEXUS DIAGNOSTIC CORE (NDC)
Módulo 6 – Sistema de inspeção profunda, detecção de conflitos e análise estrutural

Este módulo é o cérebro neutro que avalia tudo no projeto.
Nada passa despercebido.
"""

import os
import ast
import hashlib
from datetime import datetime
from typing import Dict, List, Any

class FileReport:
    """Representa um relatório completo de um arquivo inspecionado."""
    def __init__(self, path: str):
        self.path = path
        self.lines = 0
        self.size_kb = 0
        self.functions = []
        self.classes = []
        self.hash = ""
        self.last_modified = None

class NexusDiagnosticCore:
    """
    Núcleo de Diagnóstico do APOLO ENGINE.
    Responsável por analisar conflitos, padrões de erro e integridade total do código.
    """

    def __init__(self, root: str = "."):
        self.root = root
        self.reports: Dict[str, FileReport] = {}
        self.warnings: List[str] = []
        self.errors: List[str] = []

    # ------------------------------------------------------------------
    # SCAN TOTAL DA ESTRUTURA
    # ------------------------------------------------------------------
    def scan_project(self):
        for root, dirs, files in os.walk(self.root):
            for file in files:
                if file.endswith(".py"):
                    fullpath = os.path.join(root, file)
                    self._analyze_file(fullpath)

    # ------------------------------------------------------------------
    # ANALISAR ARQUIVO INDIVIDUAL
    # ------------------------------------------------------------------
    def _analyze_file(self, path: str):
        report = FileReport(path)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read()
            report.lines = data.count("\n")
            report.size_kb = len(data) / 1024
            report.hash = hashlib.md5(data.encode()).hexdigest()
            report.last_modified = datetime.fromtimestamp(os.path.getmtime(path))

        try:
            tree = ast.parse(data)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    report.functions.append(node.name)
                if isinstance(node, ast.ClassDef):
                    report.classes.append(node.name)
        except SyntaxError:
            self.errors.append(f"ERRO DE SINTAXE no arquivo: {path}")

        self.reports[path] = report

    # ------------------------------------------------------------------
    # 6.2 – DETECTOR DE NOME DUPLICADO
    # ------------------------------------------------------------------
    def detect_name_conflicts(self):
        function_map = {}
        class_map = {}

        for rep in self.reports.values():
            for func in rep.functions:
                function_map.setdefault(func, []).append(rep.path)
            for cls in rep.classes:
                class_map.setdefault(cls, []).append(rep.path)

        for name, paths in function_map.items():
            if len(paths) > 1:
                self.warnings.append(
                    f"FUNÇÃO DUPLICADA: '{name}' aparece em {paths}"
                )

        for name, paths in class_map.items():
            if len(paths) > 1:
                self.warnings.append(
                    f"CLASSE DUPLICADA: '{name}' aparece em {paths}"
                )

    # ------------------------------------------------------------------
    # 6.3 – DETECÇÃO DE ARQUIVOS SUSPEITOS
    # ------------------------------------------------------------------
    def detect_suspicious_files(self):
        for rep in self.reports.values():
            if rep.lines < 3:
                self.warnings.append(f"Arquivo MUITO pequeno: {rep.path}")

            if rep.size_kb > 512:
                self.warnings.append(f"Arquivo gigante detectado: {rep.path}")

    # ------------------------------------------------------------------
    # 6.4 – GERAR RELATÓRIO FINAL
    # ------------------------------------------------------------------
    def generate_report(self) -> Dict[str, Any]:
        return {
            "total_files": len(self.reports),
            "warnings": self.warnings,
            "errors": self.errors,
            "files": {
                path: {
                    "lines": rep.lines,
                    "size_kb": rep.size_kb,
                    "functions": rep.functions,
                    "classes": rep.classes,
                    "last_modified": rep.last_modified.isoformat(),
                    "hash": rep.hash
                }
                for path, rep in self.reports.items()
            }
        }

# ----------------------------------------------------------------------
# MÉTODO DE EXECUÇÃO DIRETA
# ----------------------------------------------------------------------
if __name__ == "__main__":
    core = NexusDiagnosticCore(root=".")
    core.scan_project()
    core.detect_name_conflicts()
    core.detect_suspicious_files()
    report = core.generate_report()
    print("===== RELATÓRIO DO NEXUS DIAGNOSTIC CORE =====")
    print(report)
