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
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

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
nosetests.xml
coverage.xml
*,cover
.hypothesis/

# Jupyter Notebook checkpoints
.ipynb_checkpoints

# VS Code / PyCharm / IDE configs
.vscode/
.idea/

# Logs, temp files
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
        "# LORE / UNIVERSO APOLO\n\nHistória, ambientação, personagens centrais, cronograma narrativo — preencha conforme o enredo.\n",
}

def create_structure():
    for d in structure:
        os.makedirs(d, exist_ok=True)
    for path, content in files.items():
        dirpath = os.path.dirname(path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.lstrip('\n'))
    print(f"Estrutura do projeto '{PROJECT}' criada com sucesso.")
    print("Pastas criadas:", structure)
    print("Arquivos iniciais:", list(files.keys()))

if __name__ == "__main__":
    create_structure()
