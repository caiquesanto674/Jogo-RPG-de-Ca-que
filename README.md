# Nexus Engine: Um Motor de Jogo Tático em Python

Bem-vindo ao Nexus Engine, um motor de jogo modular para simulações táticas e de estratégia, construído em Python. Este projeto foi projetado para ser escalável, permitindo a fácil adição de novas mecânicas de jogo, unidades e sistemas.

## Arquitetura do Projeto

O Nexus Engine segue uma arquitetura modular para separar claramente as diferentes responsabilidades do sistema. A estrutura de diretórios principal é a seguinte:

```
nexus/
├── componentes/
│   ├── classes.py      # Dicionário com os perfis das classes (Tanque, etc.)
│   ├── unidade.py      # A classe principal UnidadeMilitar
│   ├── base.py         # A classe para bases militares
│   └── npc.py          # A classe para a IA dos NPCs
├── sistemas/
│   ├── motor.py        # O coração do jogo, orquestra os sistemas
│   ├── economia.py     # Lógica econômica central
│   ├── tecnologia.py   # O sistema de árvore de tecnologias
│   └── log.py          # Sistema de logging
└── utils/
    └── ...             # Módulos de utilidades (vazio por enquanto)

tests/
└── ...                 # Testes para os componentes e sistemas

main.py                 # Ponto de entrada principal da aplicação
```

## Guia de Início Rápido

Siga os passos abaixo para configurar seu ambiente de desenvolvimento e executar o Nexus Engine.

### 1. Pré-requisitos

- Python 3.8 ou superior

### 2. Instalação

Primeiro, clone este repositório para a sua máquina local. Em seguida, crie um ambiente virtual e instale as dependências:

```bash
# Crie e ative um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate

# Instale as dependências de desenvolvimento
pip install -r requirements.txt
```

### 3. Executando a Simulação

Para executar a simulação principal do jogo, execute o script `main.py` a partir do diretório raiz do projeto:

```bash
python3 main.py
```

Você verá a saída do console mostrando o progresso dos turnos, o estado da economia e as ações dos agentes de IA.

### 4. Executando os Testes

Para garantir que todos os componentes do motor do jogo estejam funcionando corretamente, você pode executar a suíte de testes completa. Atualmente, não há testes implementados, mas quando houver, eles poderão ser executados com:

```bash
python3 -m unittest discover tests
```
