# =====================================================
# === NEXUS_GUARDIAN - PARTE 2: SISTEMA DE ANÁLISE   ===
# =====================================================
# Este módulo complementa a Parte 1 e garante:
# - Organização automática
# - Proteção contra conflitos
# - Integração segura de módulos gigantes
# - Mapeamento semântico
# - Autocura
# - Evolução guiada por IA

import re
import ast
import uuid
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional


# =====================================================
# === 5. NÚCLEO DE ANÁLISE ESTRUTURAL =================
# =====================================================
class StructuralAnalyzer:
    def __init__(self):
        self.struct_map = {}

    def map_file(self, code: str, name: str):
        """Lê o código e identifica funções, classes e imports."""
        tree = ast.parse(code)
        structure = {
            "functions": [],
            "classes": [],
            "imports": [],
            "hash": hashlib.sha256(code.encode()).hexdigest()
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                structure["functions"].append(node.name)
            elif isinstance(node, ast.ClassDef):
                structure["classes"].append(node.name)
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                structure["imports"].append(ast.dump(node))

        self.struct_map[name] = structure
        return structure

    def compare_structures(self, a: str, b: str) -> Dict[str, Any]:
        """Compara dois arquivos para ver conflitos estruturais."""
        sa = self.struct_map.get(a, {})
        sb = self.struct_map.get(b, {})

        return {
            "duplicate_functions": list(set(sa.get("functions", [])) & set(sb.get("functions", []))),
            "duplicate_classes": list(set(sa.get("classes", [])) & set(sb.get("classes", []))),
            "shared_imports": list(set(sa.get("imports", [])) & set(sb.get("imports", [])))
        }


# =====================================================
# === 6. ANALISADOR SEMÂNTICO =========================
# =====================================================
class SemanticAnalyzer:
    def __init__(self):
        self.semantic_memory = {}

    def analyze(self, code: str, file_name: str):
        """Extrai significado, propósito e domínios de cada arquivo."""
        keywords = [
            "sistema", "engine", "militar", "mundo", "rpg",
            "economia", "AI", "combate", "inventário",
            "classe", "magia", "unificação", "multiverso"
        ]

        detected = [kw for kw in keywords if kw in code.lower()]
        summary = {
            "file": file_name,
            "concepts": detected,
            "complexity": len(code) // 400
        }

        self.semantic_memory[file_name] = summary
        return summary

    def correlate(self, a: str, b: str):
        """Avalia se dois códigos pertencem ao mesmo sistema."""
        sa = set(self.semantic_memory.get(a, {}).get("concepts", []))
        sb = set(self.semantic_memory.get(b, {}).get("concepts", []))

        return {
            "semantic_overlap": list(sa & sb),
            "distance": len(sa.symmetric_difference(sb))
        }


# =====================================================
# === 7. MAPEADOR DE DEPENDÊNCIAS =====================
# =====================================================
class DependencyMap:
    def __init__(self):
        self.graph = {}

    def map_dependencies(self, file_name: str, code: str):
        """Detecta dependências simples entre arquivos."""
        imports = re.findall(r"from\s+(\w+)", code)
        self.graph[file_name] = imports
        return imports

    def get_all(self):
        return self.graph

    def detect_circular(self):
        """Verifica ciclos perigosos."""
        cycles = []
        for module, deps in self.graph.items():
            for d in deps:
                if d in self.graph and module in self.graph[d]:
                    cycles.append((module, d))
        return cycles


# =====================================================
# === 8. DETECTOR DE CONFLITOS ========================
# =====================================================
class ConflictDetector:
    def __init__(self):
        self.alerts = []

    def detect(self, struct_diff: Dict[str, List[str]]):
        """Verifica conflitos graves."""
        conflicts = []

        if struct_diff["duplicate_functions"]:
            conflicts.append(f"⚠ Funções duplicadas: {struct_diff['duplicate_functions']}")
        if struct_diff["duplicate_classes"]:
            conflicts.append(f"⚠ Classes duplicadas: {struct_diff['duplicate_classes']}")
        if struct_diff["shared_imports"]:
            conflicts.append("ℹ Imports compartilhados detectados (seguro).")

        self.alerts.extend(conflicts)
        return conflicts


# =====================================================
# === 9. MOTOR DE FUSÃO SEGURA ========================
# =====================================================
class SafeMergeEngine:
    def __init__(self):
        self.merge_log = []

    def merge(self, base: str, new: str):
        """Faz merge com proteção anti-perda."""
        merged = f"# MERGED FILE ID={uuid.uuid4()}\n"
        merged += "# ===== [BASE] =====\n" + base + "\n"
        merged += "# ===== [NEW] =====\n" + new + "\n"

        self.merge_log.append({
            "timestamp": datetime.now().isoformat(),
            "length": len(merged)
        })

        return merged


# =====================================================
# === 10. KERNEL DE MEMÓRIA EVOLUTIVA ================
# =====================================================
class NexusMemoryKernel:
    def __init__(self):
        self.records = {}

    def store(self, name: str, data: Dict[str, Any]):
        self.records[name] = {
            "data": data,
            "saved": datetime.now().isoformat()
        }

    def get(self, name: str):
        return self.records.get(name)

    def list_all(self):
        return list(self.records.keys())


# =====================================================
# === 11. NÚCLEO PRINCIPAL (JUNTA TUDO) ==============
# =====================================================
class NexusGuardianCore:
    def __init__(self):
        self.struct = StructuralAnalyzer()
        self.semantic = SemanticAnalyzer()
        self.dep = DependencyMap()
        self.conflicts = ConflictDetector()
        self.merge = SafeMergeEngine()
        self.memory = NexusMemoryKernel()

    def process_file(self, code: str, name: str):
        struct = self.struct.map_file(code, name)
        semantics = self.semantic.analyze(code, name)
        deps = self.dep.map_dependencies(name, code)

        self.memory.store(name, {
            "structure": struct,
            "semantics": semantics,
            "dependencies": deps
        })

    def check_conflicts(self, a: str, b: str):
        diff = self.struct.compare_structures(a, b)
        return self.conflicts.detect(diff)

    def merge_files(self, base: str, new: str):
        return self.merge.merge(base, new)
