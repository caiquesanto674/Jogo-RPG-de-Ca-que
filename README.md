# Sistema de Auto-Correção Autônoma (AI Cardinal)
Este sistema implementa uma IA Cardinal que monitora ativamente a saúde e a estabilidade dos componentes do sistema, diagnosticando e corrigindo falhas (bugs) automaticamente, sem intervenção humana. O design é baseado no conceito de um "Grande Sábio" ou "Ciel" que garante a integridade do ecossistema do jogo/aplicação.

## Estrutura do Sistema
O sistema é composto por três classes principais que interagem no ciclo de Monitoramento -> Diagnóstico -> Correção.

### 1. SystemState (Estado do Componente)
Representa qualquer módulo ou serviço dentro do sistema (ex: Servidor, Banco de Dados, Lógica de Combate).

| Atributo      | Descrição                                                               |
|---------------|-------------------------------------------------------------------------|
| `name`        | Nome do componente monitorado.                                          |
| `threshold`   | O valor mínimo de saúde/integridade. Abaixo deste valor, é um bug ou falha. |
| `current_value`| O valor atual de saúde/integridade do componente.                      |
| `fix_cost`    | O custo, em recursos da IA, para aplicar a correção.                     |

### 2. FailureTracker (Rastreador de Falhas)
Um objeto que registra uma falha no momento em que é detectada. Contém informações como nome do componente, severidade da falha e custo da correção.

### 3. AutoCorrectionEngine (O Cérebro da IA Cardinal)
A classe principal que gerencia todo o ciclo de vida da auto-correção.

#### Ciclo de Operação:
1.  **`monitor_and_diagnose()`**: A IA Cardinal itera sobre todos os `SystemState` registrados. Se `current_value` for menor que `threshold`, um novo `FailureTracker` é criado e adicionado à fila de correções (`failure_queue`).
2.  **`apply_fix(failure)`**: Executa o processo de "Find and Fix a Bug".
    *   Verifica se os `resources` da IA são suficientes para o `fix_cost`.
    *   Se for suficiente, consome o recurso e restaura o `current_value` do componente para um estado seguro (acima do `threshold`).
    *   Registra a correção como bem-sucedida ou falha (por falta de recursos).
3.  **`run_auto_correction_cycle()`**: Orquestra a execução sequencial do diagnóstico e da aplicação das correções.

## Como Executar
O sistema pode ser executado diretamente através do arquivo `auto_correction_system.py`:
```bash
python auto_correction_system.py
```
O log exibirá as seguintes etapas:
* A simulação de dano nos componentes.
* O diagnóstico da IA (detectando falhas).
* As tentativas de correção (sucesso e falha por recurso).
* O estado final dos componentes.

## Testes de Unidade
O arquivo `test_auto_correction.py` garante a integridade do sistema, testando cenários como:
* Detecção correta de componentes com falha (`is_buggy`).
* Correção bem-sucedida (o componente é restaurado e o recurso é gasto).
* Falha na correção por falta de recursos (os recursos não são gastos e o componente permanece com falha).

Para executar os testes (em ambiente com `unittest` instalado):
```bash
python -m unittest test_auto_correction.py
```
