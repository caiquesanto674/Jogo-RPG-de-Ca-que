# Guia do Agente para o Projeto Nexus

Olá! Este guia foi criado para ajudar você a entender a estrutura e a arquitetura do motor de jogo Nexus.

## Visão Geral

O Nexus é um motor de jogo para um RPG tático e de estratégia, escrito em Python. O projeto foi recentemente unificado a partir de duas versões anteriores (`nexus_unificado.py` e `apolo_engine`) para combinar uma ampla gama de mecânicas de jogo com um sistema de combate tático detalhado.

Toda a documentação, comentários e nomes de variáveis estão em **Português do Brasil**.

## Arquitetura do Projeto

O código-fonte principal está localizado no diretório `nexus/`, que é um pacote Python. A estrutura é a seguinte:

```
nexus/
├── componentes/
│   ├── classes_unidades.py  # Dicionário com os perfis das classes (Tanque, etc.)
│   └── entidades.py         # Classes principais do jogo (UnidadeCombate, BaseMilitar, etc.)
│
├── sistemas/
│   ├── ia.py                # Módulos de Inteligência Artificial (NPCs, IA de reparo).
│   ├── mecanicas_jogo.py    # Sistemas centrais (Economia, Ambiente, Missões).
│   ├── motor.py             # O coração do jogo, que orquestra os sistemas.
│   └── tecnologia.py        # O sistema de árvore de tecnologias.
│
└── utils/
    └── helpers.py           # Funções auxiliares, constantes e classes de suporte (Log, etc.).

main.py                      # Ponto de entrada principal para executar a simulação.
```

### Detalhes dos Módulos

*   **`nexus/componentes`**: Contém as "peças" do jogo. `entidades.py` define os objetos do jogo (unidades, bases), enquanto `classes_unidades.py` define os arquétipos e atributos base dessas unidades.
*   **`nexus/sistemas`**: Contém a lógica e as mecânicas. `motor.py` é o orquestrador principal, `ia.py` lida com o comportamento dos NPCs, e os outros arquivos gerenciam sistemas específicos como economia e tecnologia.
*   **`nexus/utils`**: Contém código de suporte que é usado em todo o projeto.

## Como Executar o Jogo

Para executar a simulação principal, utilize o seguinte comando a partir do diretório raiz do projeto:

```bash
python3 main.py
```

A saída da simulação será exibida no console e também será salva no arquivo `log_nexus_unificado.log`.

## Pontos Importantes

*   O sistema de combate é baseado no conceito de **Força Bélica**, que é um cálculo dinâmico que leva em conta a classe da unidade, moral, tecnologia e outros fatores táticos. A lógica está em `entidades.py`.
*   A IA principal (`AI_NPC`) possui um sistema de evolução simples, que reage ao ambiente e ao resultado de suas ações.
*   O idioma principal do código e dos comentários é o **Português do Brasil**. Mantenha a consistência.
