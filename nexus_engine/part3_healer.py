# ============================================================
# === NEXUS_GUARDIAN - PARTE 3: AUTOCURA E EXPANSÃO GLOBAL ===
# ============================================================

import re
import difflib
import hashlib
from datetime import datetime

from .part1_core import NexusEngine
from .part2_analyzer import NexusGuardianCore


# ============================================================
# === 12. MOTOR DE AUTOCURA ==================================
# ============================================================
class AutoHealEngine:
    def __init__(self):
        self.fix_log = []

    def heal_syntax(self, code: str) -> str:
        """
        Scanner básico: identifica padrões comuns quebrados e ajusta.
        Pode ser expandido futuramente com ML.
        """
        fixed = code

        # Corrigir indentação quebrada
        fixed = re.sub(r"\t", "    ", fixed)

        # Fechar parênteses faltando
        if fixed.count("(") > fixed.count(")"):
            fixed += ")" * (fixed.count("(") - fixed.count(")"))

        # Fechar chaves/colchetes se necessário
        for open_b, close_b in [("{", "}"), ("[", "]")]:
            diff_b = fixed.count(open_b) - fixed.count(close_b)
            if diff_b > 0:
                fixed += close_b * diff_b

        self.fix_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": "syntax_heal",
            "delta": len(fixed) - len(code)
        })

        return fixed

    def heal_structure(self, code: str) -> str:
        """
        Repara duplicação mal-formada e reorganiza blocos.
        """
        lines = code.split("\n")
        cleaned = []
        seen_defs = set()

        for l in lines:
            # Remover repetições acidentais de "def def"
            l = re.sub(r"def\s+def", "def", l)

            # Evitar duplicações idênticas
            if l.strip().startswith("def "):
                if l in seen_defs:
                    continue
                seen_defs.add(l)

            cleaned.append(l)

        return "\n".join(cleaned)


# ============================================================
# === 13. SISTEMA INTELIGENTE DE PATCH ========================
# ============================================================
class PatchSystem:
    def __init__(self):
        self.patches = []

    def generate_patch(self, original: str, modified: str):
        diff = difflib.unified_diff(
            original.split("\n"),
            modified.split("\n"),
            lineterm="",
            fromfile="original",
            tofile="modified"
        )

        patch_text = "\n".join(diff)
        patch_id = hashlib.sha1(patch_text.encode()).hexdigest()

        patch_record = {
            "id": patch_id,
            "timestamp": datetime.now().isoformat(),
            "patch": patch_text
        }

        self.patches.append(patch_record)
        return patch_record

    def apply_patch(self, base: str, patch_text: str):
        patched = difflib.restore(patch_text.split("\n"), 1)
        return "\n".join(patched)


# ============================================================
# === 14. EXECUTOR DE TESTES INTERNOS ========================
# ============================================================
class InternalTestExecutor:
    def __init__(self):
        self.test_results = []

    def run_basic_tests(self, code: str):
        result = {"timestamp": datetime.now().isoformat(), "tests": {}}

        # Teste 1: sintaxe
        try:
            compile(code, "<string>", "exec")
            result["tests"]["syntax"] = "OK"
        except Exception as e:
            result["tests"]["syntax"] = f"ERROR: {e}"

        # Teste 2: busca por funções essenciais
        essential = ["class", "def", "import"]
        result["tests"]["structure"] = {
            k: ("FOUND" if k in code else "MISSING") for k in essential
        }

        self.test_results.append(result)
        return result


# ============================================================
# === 15. SUPER CONECTOR DE SISTEMAS GIGANTES ================
# ============================================================
class SystemHyperConnector:
    def __init__(self):
        self.links = {}

    def connect(self, name_a: str, name_b: str, reason: str):
        """Cria conexão explicita entre módulos enormes."""
        key = f"{name_a} -> {name_b}"

        self.links[key] = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason
        }

    def get_links(self):
        return self.links


# ============================================================
# === 16. GERADOR DE PACOTE COMPLETO (.ZIP FUTURO) ===========
# ============================================================
class PackageBuilder:
    def __init__(self):
        self.package_manifest = {}

    def register_file(self, name: str, content: str):
        self.package_manifest[name] = {
            "size": len(content),
            "hash": hashlib.md5(content.encode()).hexdigest(),
            "saved": datetime.now().isoformat()
        }

    def build_manifest(self):
        return self.package_manifest


# ============================================================
# === 17. NÚCLEO PRINCIPAL – PARTE 3 ==========================
# ============================================================
class NexusGuardianCoreV3:
    """Integra Partes 1, 2 e 3 em uma única maquina evolutiva."""
    def __init__(self, v1_core, v2_core):
        self.v1 = v1_core
        self.v2 = v2_core

        self.autoheal = AutoHealEngine()
        self.patch = PatchSystem()
        self.tests = InternalTestExecutor()
        self.hyper = SystemHyperConnector()
        self.package = PackageBuilder()

    def process_large_file(self, code: str, name: str):
        """Pipeline completo de processamento para arquivos gigantes."""

        # Cura inicial
        healed = self.autoheal.heal_syntax(code)
        healed = self.autoheal.heal_structure(healed)

        # Testes rápidos
        test_data = self.tests.run_basic_tests(healed)

        # Registrar no sistema global
        self.v2.process_file(healed, name)
        self.package.register_file(name, healed)

        return {
            "healed_code": healed,
            "tests": test_data
        }

    def link_systems(self, a: str, b: str, reason: str):
        self.hyper.connect(a, b, reason)

    def generate_patch(self, original: str, fixed: str):
        return self.patch.generate_patch(original, fixed)

    def build_package_manifest(self):
        return self.package.build_manifest()
