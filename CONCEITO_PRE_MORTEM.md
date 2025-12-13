# Análise Pre-Mortem: Apolo Engine

Este documento descreve uma análise "pre-mortem" do Apolo Engine, identificando potenciais riscos e problemas de design que podem impactar o desenvolvimento, a manutenibilidade e a escalabilidade do projeto. O objetivo é antecipar desafios antes que eles se tornem críticos.

## 1. Riscos Identificados

### 1.1. Documentação Desatualizada (`README.md`)

- **Observação:** O `README.md` atual descreve uma arquitetura que não corresponde à implementação real. Ele menciona um arquivo `apolo_engine/motor_jogo.py` que não existe, enquanto o ponto de entrada principal é `principal.py`, que utiliza `apolo_engine/systems/motor.py`.
- **Risco:** Dificulta a entrada de novos desenvolvedores, causa confusão sobre a estrutura do projeto e pode levar a erros de implementação. Um `README` incorreto é pior do que nenhum `README`.

### 1.2. Alto Acoplamento no Motor Principal (`Engine_APOLO`)

- **Observação:** A classe `Engine_APOLO` em `apolo_engine/systems/motor.py` está fortemente acoplada a várias outras classes, como `Economia`, `Tecnologia`, `BaseMilitar`, e `AI_NPC`. Ela instancia diretamente esses objetos em seu construtor.
- **Risco:**
    - **Dificuldade de Teste:** Isolar e testar a lógica do motor sem instanciar todo o ecossistema de dependências é quase impossível.
    - **Baixa Manutenibilidade:** Alterações em qualquer um dos subsistemas (`Economia`, `Tecnologia`, etc.) podem exigir modificações diretas no motor, violando o Princípio de Aberto/Fechado.
    - **Inflexibilidade:** Torna difícil substituir ou adicionar novas implementações de subsistemas (por exemplo, um novo tipo de IA ou um modelo econômico diferente) sem alterar o núcleo do motor.

### 1.3. Lógica de Jogo "Hardcoded"

- **Observação:** A lógica de resposta estratégica no método `executar_resposta_estrategica` está "hardcoded" (fixa no código). As ações da IA (`atacar`, `explorar`, `negociar`) e suas consequências são definidas em uma estrutura `if/elif`.
- **Risco:**
    - **Escalabilidade Limitada:** Adicionar novas ações ou modificar as existentes exige alterar o código-fonte do motor, tornando o sistema rígido e difícil de expandir.
    - **Falta de Balanceamento:** A lógica de jogo e os valores (por exemplo, `economia.reserva += 5000`) estão espalhados pelo código, dificultando o ajuste e o balanceamento do jogo. O ideal seria que esses dados viessem de arquivos de configuração (JSON, YAML).

### 1.4. IA Simplista e Previsível

- **Observação:** A `AI_NPC` baseia suas decisões apenas na força bélica total do jogador e possui um conjunto limitado de ações.
- **Risco:** A IA pode se tornar previsível e fácil de explorar, diminuindo o desafio e o interesse do jogo a longo prazo. Ela não considera outros fatores importantes, como o estado da economia do jogador, suas tecnologias ou a composição de seu exército.

## 2. Recomendações Estratégicas

### 2.1. Atualização e Sincronização da Documentação

- **Ação:** Atualizar o `README.md` para refletir a arquitetura atual do projeto. Incluir um diagrama de arquitetura simplificado e instruções claras sobre como executar e testar o jogo.
- **Benefício:** Melhora a clareza do projeto e acelera a integração de novos colaboradores.

### 2.2. Implementar Inversão de Controle (IoC) e Injeção de Dependência (DI)

- **Ação:** Refatorar a classe `Engine_APOLO` para receber suas dependências (`Economia`, `Tecnologia`, etc.) como parâmetros no construtor, em vez de criá-las internamente.
- **Benefício:**
    - **Desacoplamento:** Reduz a dependência direta entre o motor e os subsistemas.
    - **Testabilidade:** Permite "mockar" as dependências em testes unitários, facilitando a verificação isolada da lógica do motor.
    - **Flexibilidade:** Facilita a substituição de implementações, permitindo, por exemplo, testar diferentes modelos de IA ou economia.

### 2.3. Adotar uma Arquitetura Orientada a Dados (Data-Driven)

- **Ação:** Externalizar a lógica de jogo e os parâmetros de balanceamento para arquivos de configuração (ex: `config/acoes_ia.json`). O motor leria esses arquivos para determinar as ações possíveis e suas consequências.
- **Benefício:** Permite que designers de jogos (ou mesmo jogadores) modifiquem o comportamento do jogo sem tocar no código-fonte, acelerando o processo de iteração e balanceamento.

### 2.4. Evoluir a Inteligência Artificial

- **Ação:** Expandir o modelo de decisão da `AI_NPC` para considerar mais variáveis do estado do jogo (economia, nível tecnológico, etc.). Introduzir um sistema de "pesos" ou uma máquina de estados finitos (FSM) para tornar o comportamento da IA mais dinâmico e menos previsível.
- **Benefício:** Aumenta a profundidade estratégica e o replay value do jogo, oferecendo um desafio mais robusto e adaptativo.
