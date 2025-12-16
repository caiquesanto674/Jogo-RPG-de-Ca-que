# CONCEITOS AVANÇADOS DE DESIGN - APOLO ENGINE

Este documento detalha as mecânicas avançadas que governam o Apolo Engine, projetadas para criar uma simulação estratégica profunda e emergente.

## 1. A Base Militar como um Organismo Vivo

A mecânica central do jogo é a representação de cada `BaseMilitar` não como uma simples estrutura, mas como um **organismo vivo e autônomo**. Este conceito se manifesta através de três atributos vitais:

- **Saúde da Base (`saude_base`):** Representa a integridade estrutural, o moral das tropas e a estabilidade geral da base. Uma saúde baixa pode levar a falhas operacionais e, em casos extremos, à perda da base.

- **Eficiência Operacional (`eficiencia_operacional`):** Um multiplicador que afeta quase todas as ações da base, desde a geração de renda até a velocidade de pesquisa. Uma base com alta eficiência é um motor poderoso para o império.

- **Metabolismo e Subsistência:** Assim como um organismo vivo, a base precisa consumir recursos a cada "ciclo" (turno) para se manter. O `metabolismo_ciclo` calcula o `custo_subsistencia` com base no nível da base e no número de unidades aquarteladas.

### O Ciclo de Vida e Morte

O ciclo de feedback é direto e punitivo, seguindo o princípio de "luz e escuridão":

1.  **Sucesso na Subsistência:** Pagar o custo de subsistência não apenas mantém a base, mas a fortalece. A saúde e a eficiência são levemente regeneradas, recompensando o planejamento econômico.
2.  **Falha na Subsistência:** A incapacidade de pagar o custo inicia uma espiral de decadência. A saúde e a eficiência caem drasticamente. Uma eficiência menor reduz a geração de renda, tornando ainda mais difícil pagar a subsistência no próximo ciclo. Esta é uma "espiral da morte" que pode levar ao colapso de uma base se não for gerenciada com cuidado.

## 2. Economia Dinâmica e Interdependente

A economia não é um sistema passivo. Ela está diretamente ligada à saúde do seu império:

- **Geração de Renda (`gerar_renda_ciclo`):** A renda do seu império não é um valor fixo. Ela é a soma da contribuição de todas as suas bases, e a contribuição de cada base é diretamente proporcional à sua `eficiencia_operacional`. Cuidar das suas bases é cuidar da sua economia.

- **Recursos como Sangue:** Os créditos (`reserva`) funcionam como o sangue do império. Eles são necessários para tudo: expansão, pesquisa e, mais importante, a subsistência das bases. Uma má gestão financeira pode levar à falência em cascata de múltiplas bases.

## 3. IA e o Código de Confirmação

A `AI_NPC` (LEGEON) opera com um sistema de **comportamento emergente** baseado na sua força bélica. As decisões da IA não são aleatórias, mas uma resposta calculada ao poder do jogador.

Para garantir a integridade e a auditabilidade das decisões da IA, foi implementado o `ProtocoloConfirmacao`. A cada turno, a IA gera um código `SHA-256` único baseado em sua ação, nome e nível. Este "código de confirmação" serve como uma assinatura digital, provando que a decisão da IA não foi adulterada e segue as regras predefinidas do universo do jogo. É uma manifestação da "Volição Ativa e Kernel 2.5", uma regra fundamental do Apolo Engine.
