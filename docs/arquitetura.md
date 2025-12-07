# Arquitetura do APOLO MEGA SYSTEM FINAL

Este documento descreve a arquitetura do APOLO MEGA SYSTEM FINAL.

## Estrutura do Motor

O motor do jogo está localizado em `engine/motor.py` e é responsável por orquestrar o ciclo de jogo, incluindo a gerenciamento de sistemas, a execução de conflitos e a simulação de eventos.

## Módulos do Jogo (`src`)

As classes do jogo estão divididas em três módulos principais no diretório `src`:

- `entidades.py`: Contém as classes que representam os seres do jogo, como `Entidade`, `Personagem`, `MonarcaAbsoluto`, `Inimigo` e `AI_NPC_Suporte`.
- `sistemas.py`: Contém as classes que gerenciam os sistemas do jogo, como `AICardinal`, `Economia`, `Tecnologia` e `BaseMilitar`.
- `conflito.py`: Contém as classes `CorrecaoLog` e `ConflictResolver`, que simulam o sistema de autocorreção de código.

## Fluxo Geral do Jogo

O fluxo geral do jogo é iniciado a partir do `main.py`, que cria uma instância do `Engine` e executa o loop principal do jogo através do método `ciclo()`.
