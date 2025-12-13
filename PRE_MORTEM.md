# Análise Pré-Mortem: Riscos Potenciais do Projeto Nexus

Este documento descreve os riscos potenciais que podem impactar o desenvolvimento e o sucesso do jogo. A análise pré-mortem é um exercício para antecipar falhas antes que elas aconteçam.

## 1. Risco de Complexidade e Código Monolítico

- **Problema:** O código-fonte está unificado em um único arquivo (`nexus_unificado.py`). À medida que novas funcionalidades (economia, tecnologia, salvar/carregar) são adicionadas, este arquivo se tornará excessivamente grande e complexo.
- **Impacto Potencial:**
    - Dificuldade de manutenção e depuração.
    - Maior probabilidade de introduzir bugs que afetam múltiplos sistemas.
    - Dificuldade para novos desenvolvedores (ou para o próprio autor no futuro) entenderem o código.
- **Mitigação:**
    - Considerar uma refatoração futura para uma estrutura modular (por exemplo, separar classes em arquivos diferentes dentro de um diretório `game_modules/`).
    - Adicionar comentários claros e documentação (docstrings) para cada função e classe.

## 2. Risco de Desbalanceamento da Jogabilidade

- **Problema:** A introdução de um sistema econômico mais complexo (gastos com unidades e tecnologias) e uma árvore de tecnologia estruturada pode facilmente levar a um jogo desbalanceado.
- **Impacto Potencial:**
    - O jogador pode encontrar estratégias "quebradas" que tornam o jogo muito fácil ou frustrante.
    - A economia pode entrar em colapso (muito recurso ou muito pouco), tornando a jogabilidade impossível.
- **Mitigação:**
    - Testar exaustivamente as interações entre os sistemas.
    - Manter os custos e benefícios (por exemplo, de unidades e tecnologias) em uma seção de configuração de fácil ajuste.
    - Implementar limites (por exemplo, número máximo de unidades) para evitar explorações.

## 3. Risco de Corrupção de Dados Salvos (Save/Load)

- **Problema:** A funcionalidade de salvar e carregar o estado do jogo é crítica. Se a estrutura dos dados do jogo mudar no futuro (por exemplo, uma classe ganha um novo atributo), os arquivos salvos antigos podem se tornar incompatíveis ou corrompidos.
- **Impacto Potencial:**
    - Perda de progresso do jogador, causando grande frustração.
    - Bugs difíceis de reproduzir que só ocorrem ao carregar um estado de jogo específico.
- **Mitigação:**
    - Implementar um sistema de versionamento para os arquivos de salvamento.
    - Escrever scripts de migração que possam atualizar arquivos de salvamento de versões antigas para a nova estrutura.
    - Realizar testes rigorosos do sistema de salvar/carregar sempre que a estrutura de dados for alterada.

## 4. Risco de "Scope Creep" (Escopo Descontrolado)

- **Problema:** O pedido inicial é amplo e abrange muitas áreas do jogo. Há o risco de adicionar cada vez mais funcionalidades sem um plano claro, tornando o projeto interminável.
- **Impacto Potencial:**
    - O projeto nunca chega a um estado "concluído".
    - A qualidade do código diminui à medida que novas funcionalidades são adicionadas apressadamente.
- **Mitigação:**
    - Definir um escopo claro para a versão atual.
    - Manter um backlog de ideias e funcionalidades para serem implementadas em versões futuras.
    - Focar em entregar um ciclo de jogo completo e polido antes de expandir com mais conteúdo.
