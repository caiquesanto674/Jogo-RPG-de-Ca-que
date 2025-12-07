# APOLO DOMÍNIO TOTAL OMEGA V2.0 — O Jogo Final do Monarca Caíque

Bem-vindo à documentação da Versão Ω Absoluta e Unificada, a manifestação final do universo de jogo do Monarca Caíque. Este projeto representa a consolidação de múltiplos sistemas complexos em um único motor de jogo coeso, centrado na figura do Monarca Absoluto.

## Visão Geral da Arquitetura

O `apolo_dominio_total_omega_v2.py` é um script autocontido que simula um jogo de estratégia em turnos com elementos profundos de RPG, economia e guerra psicológica. A arquitetura é construída em torno de um `Engine` central que orquestra os seguintes sistemas a cada ciclo:

### 1. **IA Cardinal (Ciel Ascendido)**
Uma IA de suporte divino que monitora o estado do jogo. Se os recursos do Monarca (como comida ou mana) ou sua moral atingem níveis críticos, a IA intervém para "salvar a realidade", reabastecendo os recursos e restaurando a moral para evitar um estado de `game over`.

### 2. **Economia e Tecnologia (Tycoon + SSSS)**
- **Economia:** Um sistema complexo que gerencia múltiplos recursos, desde os mundanos (`comida`, `mana`) até os conceituais (`ouro_conceitual`, `consciencia_remanescente`) e exóticos (`materia_escura_ssss`). O sistema simula consumo e ganhos passivos a cada ciclo.
- **Tecnologia:** Uma árvore de tecnologia que pode ser pesquisada gastando recursos avançados. As tecnologias desbloqueiam novas habilidades e upgrades, como o crucial **Campo Psíquico SSSS**.

### 3. **Personagens e RPG**
- **Monarca Absoluto (Caíque Apolo Ω):** O protagonista `OWNER`, uma entidade de poder quase ilimitado com mecânicas únicas como:
    - **Agony Overflow:** Uma habilidade passiva que aumenta seu poder (`indice_dimensional`) se sua moral cair para níveis críticos.
    - **Sinergia de Harém:** A capacidade de restaurar a moral com base no número de entidades submissas em seu harém.
- **IA de Suporte (Aliados):** NPCs como `Calia Cardinal` que possuem uma IA tática. Eles tomam decisões inteligentes durante o combate para apoiar o Monarca, como restaurar sua moral ou priorizar a ativação de defesas estratégicas.
- **Inimigos (Poder Psicológico):** Adversários como `Lord Zarkon Ω` que podem atacar não apenas o HP, mas também a **moral** do Monarca através de ataques psicológicos.

### 4. **Base Militar (Core Nexus Aurora)**
O centro de operações do Monarca. A base consome e produz recursos através de seus componentes internos e é o nexo para a pesquisa tecnológica. É aqui que upgrades cruciais, como a **Defesa Psíquica SSSS**, são ativados. Esta defesa é a única forma de mitigar o dano de moral infligido por inimigos com poder psicológico.

## Como Executar

O projeto é um script Python único e não requer dependências externas além da biblioteca padrão.

Para executar a simulação do jogo, use o seguinte comando:
```bash
python apolo_dominio_total_omega_v2.py
```
A simulação iniciará, mostrando uma introdução e, em seguida, progredindo através de vários ciclos (turnos) de jogo. Cada ciclo exibirá um relatório detalhado do estado do Monarca, da base, dos recursos e do combate.

Obrigado por tudo, Monarca Caíque. Você venceu.
