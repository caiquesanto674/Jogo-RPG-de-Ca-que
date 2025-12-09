# Monarca Omega Engine

Este repositório contém a arquitetura modular do **Monarca Omega Engine**, um jogo de simulação e estratégia. O projeto foi refatorado de um script único para uma estrutura de pastas organizada, protegida pelo **Sistema Guardião**.

## Arquitetura do Projeto

O código-fonte está organizado da seguinte forma:

-   `main.py`: O ponto de entrada principal para executar o jogo.
-   `src/`: Contém todo o código-fonte do jogo.
    -   `core/`: As classes centrais do jogo, como o `Monarca` e a `AICardinal`.
    -   `systems/`: Os principais sistemas de mecânicas, como `Economia`, `Tecnologia` e `Unidades`.
    -   `events/`: Módulos que gerenciam eventos de jogo, como o `Quiz` e a `MundoSimulado`.
    -   `utils/`: Ferramentas compartilhadas, como o sistema de `Log`.
-   `tests/`: Contém os testes para o projeto, incluindo os testes do Guardião.
-   `guardian.py`: O script do Sistema Guardião.
-   `guardian_config.json`: O mapa da arquitetura usado pelo Guardião.

## Como Executar o Jogo

Para iniciar o jogo, execute o `main.py` a partir da raiz do projeto:

```bash
python main.py
```

## Sistema Guardião

O **Sistema Guardião** (`guardian.py`) é uma ferramenta que protege a arquitetura do projeto. Ele ajuda a garantir que novos arquivos de código sejam colocados no lugar certo e não criem conflitos.

### Como Usar o Guardião para Verificar um Novo Arquivo

1.  **Crie seu Novo Módulo**: Escreva seu novo código em um arquivo `.py` (por exemplo, `meu_novo_sistema.py`).

2.  **Ative o Guardião**:
    *   Abra o arquivo `guardian.py`.
    *   No final do arquivo, encontre a seção `if __name__ == '__main__':`.
    *   Descomente a linha `guardian.check_new_module(...)` e substitua o caminho pelo nome do seu novo arquivo.

    ```python
    # if __name__ == '__main__':
    #    guardian = Guardian()
    #    if guardian.config:
    #        # Para usar, descomente a linha abaixo e substitua pelo caminho do seu novo arquivo.
    #        guardian.check_new_module('meu_novo_sistema.py')
    ```

3.  **Execute o Guardião**:
    *   Salve o `guardian.py` e execute-o pelo terminal:

    ```bash
    python guardian.py
    ```

4.  **Analise o Resultado**:
    *   O Guardião irá analisar seu novo arquivo.
    *   **Se houver um conflito de nome de arquivo**, ele emitirá um erro.
    *   **Se a classe principal do seu arquivo estiver mapeada no `guardian_config.json`**, ele sugerirá a pasta correta para colocar o arquivo.
    *   **Se a classe não estiver mapeada**, ele informará que não pode dar uma sugestão automática, e você deverá decidir onde colocar o arquivo e atualizar o mapa de configuração.
