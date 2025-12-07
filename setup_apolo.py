#!/usr/bin/env python3
import os

PROJECT = "apolo_engine"

structure = [
    os.path.join(PROJECT, "ai"),
    os.path.join(PROJECT, "world"),
    os.path.join(PROJECT, "entities"),
    os.path.join(PROJECT, "systems"),
    os.path.join(PROJECT, "combat"),
    os.path.join(PROJECT, "docs"),
    "tests",  # pasta de testes
]

files = {
    os.path.join(PROJECT, ".gitignore"): """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
dist/
/*.egg-info/
.installed.cfg

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
*,cover
.hypothesis/

# IDEs
.vscode/
.idea/

# Logs, temp
*.log
*.tmp
*.swp
*.swo
""",
    os.path.join(PROJECT, "README.md"):
        "# APOLO — O DOMÍNIO ÔMEGA\n\nProjeto base para engine do jogo APOLO. Estrutura modular para AI, mundo, entidades, sistemas, combate, interface e documentação.\n",
    os.path.join(PROJECT, "main.py"):
        "# main.py — Ponto de entrada do jogo\n\nif __name__ == '__main__':\n    print('APOLO engine iniciada')\n",
    os.path.join(PROJECT, "docs", "GDD_README.md"):
        "# GDD APOLO\n\nDesign Document do jogo — documente mecânicas, lore, classes, sistemas, fluxo de jogo, etc.\n",
    os.path.join(PROJECT, "docs", "LORE.md"):
        "# LORE / UNIVERSO APOLO\n\nHistória e narrativa do universo. Preencha com a lore completa.\n",
    os.path.join("tests", "test_basic.py"):
        """import unittest

# Testes básicos de integridade do projeto APOLO

class TestBasicoAPOLO(unittest.TestCase):
    def test_imports(self):
        # Testa se módulos essenciais importam sem erro
        import apolo_engine
        from apolo_engine.entities.entidade import Entidade
        from apolo_engine.systems.economy import Economia
        from apolo_engine.systems.base import BaseMilitar
        from apolo_engine.ai.cardinal import AICardinal
        # Apenas assegura que as classes existem
        self.assertTrue(Entidade is not None)
        self.assertTrue(Economia is not None)
        self.assertTrue(BaseMilitar is not None)
        self.assertTrue(AICardinal is not None)

    def test_economia_inicia(self):
        from apolo_engine.systems.economy import Economia
        eco = Economia()
        self.assertTrue(isinstance(eco.reservas, dict))
        # Reserva inicial deve ter 'eter' e 'mana'
        self.assertIn('eter', eco.reservas)
        self.assertIn('mana', eco.reservas)

if __name__ == '__main__':
    unittest.main()
""",
    os.path.join("requirements.txt"):
        "# Dependências recomendadas para APOLO\npytest>=7.0\n"
}

def create_structure():
    for d in structure:
        os.makedirs(d, exist_ok=True)
    for path, content in files.items():
        dirpath = os.path.dirname(path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        # Escreve o conteúdo — sobrescreve se já existir
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.lstrip('\n'))
    print(f"Estrutura do projeto '{PROJECT}' criada com sucesso.")
    print("Pastas criadas:", structure)
    print("Arquivos iniciais:", list(files.keys()))

if __name__ == "__main__":
    create_structure()
