# Apolo Engine: Um Motor de Jogo Tático em Python

Bem-vindo ao Apolo Engine, um motor de jogo modular para simulações táticas e de estratégia, construído em Python. Este projeto foi projetado para ser escalável, permitindo a fácil adição de novas mecânicas de jogo, unidades e sistemas.

## Arquitetura do Projeto

O Apolo Engine segue uma arquitetura modular para separar claramente as diferentes responsabilidades do sistema. A estrutura de diretórios principal é a seguinte:

```
apolo_engine/
├── entities/
│   ├── classes.py      # Dicionário com os perfis das classes (Tanque, etc.)
│   └── unidade.py      # A classe principal UnidadeMilitar
├── systems/
│   └── tecnologia.py   # O sistema de árvore de tecnologias
├── ambiente.py         # Gerenciamento do ambiente de jogo
├── economia.py         # Lógica econômica central
├── ia.py               # Módulos de Inteligência Artificial
├── log_global.py       # Sistema de logging
├── motor_jogo.py       # O coração do jogo, orquestra os sistemas
└── ...                 # Outros módulos principais

tests/
├── entities/
│   └── test_unidade.py # Testes para a classe UnidadeMilitar
└── test_motor_jogo.py  # Testes de integração para o motor principal
```

## Guia de Início Rápido

Siga os passos abaixo para configurar seu ambiente de desenvolvimento e executar o Apolo Engine.

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

Para garantir que todos os componentes do motor do jogo estejam funcionando corretamente, você pode executar a suíte de testes completa:

```bash
python3 -m unittest discover tests
```

Todos os testes devem passar, indicando que a base de código está estável.
