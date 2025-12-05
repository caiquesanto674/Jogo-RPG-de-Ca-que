# auto_correction_system.py
# Sistema de Auto-Correção Autônoma (Inspirado no Grande Sábio/Ciel)
#
# Este sistema simula a detecção e correção automática de falhas (bugs,
# desvios de estado) em componentes, sem intervenção humana.

import random
import time
from typing import Dict, Any, List, Optional
import logging

# Configuração de Log para rastrear as ações do sistema
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SystemState:
    """
    Representa o estado de um componente ou serviço do sistema a ser monitorado.
    Exemplo: Um servidor, uma rotina de processamento, um recurso de jogo.
    """
    def __init__(self, name: str, threshold: float, current_value: float, fix_cost: int):
        self.name = name  # Nome do componente (e.g., "Serviço de Login")
        self.threshold = threshold  # Limite crítico (abaixo disso é considerado falha)
        self.current_value = current_value  # Valor atual (e.g., Nível de Saúde/Integridade)
        self.fix_cost = fix_cost  # Custo em recursos para corrigir esta falha

    def is_buggy(self) -> bool:
        """Verifica se o componente está com falha/bug."""
        return self.current_value < self.threshold

    def __repr__(self):
        return f"Estado(Nome='{self.name}', Valor={self.current_value:.2f}, Limite={self.threshold:.2f}, Custo={self.fix_cost})"

class FailureTracker:
    """Estrutura para registrar uma falha detectada."""
    def __init__(self, component: SystemState):
        self.component_name = component.name
        self.severity = component.threshold - component.current_value
        self.fix_cost = component.fix_cost
        self.detected_time = time.time()
        logging.warning(f"Falha detectada em: {self.component_name}. Severidade: {self.severity:.2f}")

    def __repr__(self):
        return f"Rastreador(Componente='{self.component_name}', Severidade={self.severity:.2f})"

class AutoCorrectionEngine:
    """
    O núcleo da IA Cardinal (Grande Sábio).
    Monitora, diagnostica e aplica correções automaticamente.
    """
    def __init__(self, initial_resources: int = 1000):
        self.components: Dict[str, SystemState] = {}
        self.failure_queue: List[FailureTracker] = []
        self.resources = initial_resources
        self.successful_fixes = 0
        self.failed_fixes = 0
        logging.info("Motor de Auto-Correção inicializado.")

    def add_component(self, component: SystemState):
        """Adiciona um componente ao monitoramento."""
        self.components[component.name] = component

    def simulate_failure(self, component_name: str, damage: float):
        """Simula um bug ou dano em um componente."""
        if component_name in self.components:
            self.components[component_name].current_value -= damage
            logging.info(f"Simulação: {component_name} sofreu dano de {damage:.2f}. Valor atual: {self.components[component_name].current_value:.2f}")

    def monitor_and_diagnose(self):
        """
        Passo 1: Monitora todos os componentes e rastreia novas falhas.
        """
        self.failure_queue = []
        for name, component in self.components.items():
            if component.is_buggy():
                # Evita rastrear falhas já conhecidas (simplesmente limpa e adiciona)
                new_failure = FailureTracker(component)
                self.failure_queue.append(new_failure)

        if self.failure_queue:
            logging.warning(f"Diagnóstico concluído. {len(self.failure_queue)} falha(s) aguardando correção.")
        else:
            logging.info("Diagnóstico concluído. Nenhum bug ou falha crítica detectada.")

    def apply_fix(self, failure: FailureTracker) -> bool:
        """
        Passo 2: Tenta aplicar a correção (o "Find and Fix a Bug").
        """
        component = self.components.get(failure.component_name)
        if not component:
            logging.error(f"Erro: Componente '{failure.component_name}' não encontrado.")
            return False

        fix_cost = component.fix_cost

        if self.resources < fix_cost:
            logging.error(f"Não foi possível corrigir '{component.name}'. Recursos insuficientes ({self.resources}/{fix_cost}).")
            self.failed_fixes += 1
            return False

        # 1. Gasta o recurso (Executa a correção)
        self.resources -= fix_cost

        # 2. Aplica a correção (Restaura o estado do componente acima do limite)
        # Assume que o "fix" leva o valor para um estado seguro (acima do limite)
        correction_amount = component.threshold + (random.random() * 5) # Garante que seja corrigido
        component.current_value = correction_amount

        self.successful_fixes += 1
        logging.info(f"✅ Correção bem-sucedida em '{component.name}'. Valor restaurado para {component.current_value:.2f}. Recursos restantes: {self.resources}")
        return True

    def run_auto_correction_cycle(self):
        """
        Executa o ciclo completo da IA Cardinal.
        Monitorar -> Diagnosticar -> Corrigir.
        """
        logging.info("\n--- INÍCIO DO CICLO DE AUTO-CORREÇÃO ---")

        # 1. Monitorar e Diagnosticar
        self.monitor_and_diagnose()

        # 2. Aplicar Correções para todas as falhas rastreadas
        if not self.failure_queue:
            logging.info("Nenhuma correção necessária neste ciclo.")
            return

        logging.info(f"Tentando corrigir {len(self.failure_queue)} falha(s)...")

        # Processa as falhas em ordem (pode ser priorizado por severidade, mas aqui é FIFO)
        for failure in self.failure_queue:
            self.apply_fix(failure)

        logging.info("--- FIM DO CICLO DE AUTO-CORREÇÃO ---")

# ==================== EXECUÇÃO DE EXEMPLO ====================
if __name__ == "__main__":
    # 1. Inicializa a IA Cardinal
    ciel = AutoCorrectionEngine(initial_resources=1500)

    # 2. Adiciona Componentes ao sistema para monitoramento
    ciel.add_component(SystemState(
        name="Serviço de Login (Ping)", threshold=80.0, current_value=100.0, fix_cost=150
    ))
    ciel.add_component(SystemState(
        name="Banco de Dados (Estabilidade)", threshold=50.0, current_value=75.0, fix_cost=300
    ))
    ciel.add_component(SystemState(
        name="Processamento Gráfico (FPS)", threshold=30.0, current_value=60.0, fix_cost=1000
    ))

    print("\n[A] ESTADO INICIAL DO SISTEMA:")
    for comp in ciel.components.values():
        print(comp)

    # --- CICLO 1: SEM FALHAS ---
    ciel.run_auto_correction_cycle()

    # --- CICLO 2: SIMULAÇÃO DE FALHAS E CORREÇÃO ---
    print("\n[B] SIMULANDO FALHAS...")
    ciel.simulate_failure("Serviço de Login (Ping)", damage=30.0) # Falha (100 -> 70, abaixo de 80)
    ciel.simulate_failure("Banco de Dados (Estabilidade)", damage=50.0) # Falha (75 -> 25, abaixo de 50)

    # Executa o ciclo de correção
    ciel.run_auto_correction_cycle()

    print("\n[C] ESTADO PÓS-CORREÇÃO:")
    for comp in ciel.components.values():
        print(comp)

    # --- CICLO 3: FALHA QUE NÃO PODE SER CORRIGIDA (CUSTO > RECURSO) ---
    print("\n[D] SIMULANDO FALHA CARA (Processamento Gráfico)...")
    ciel.simulate_failure("Processamento Gráfico (FPS)", damage=40.0) # Falha (60 -> 20, abaixo de 30). Custo: 1000. Recursos ~900.
    ciel.run_auto_correction_cycle()

    print("\n[E] RESUMO FINAL DA IA:")
    print(f"Recursos Atuais da IA: {ciel.resources}")
    print(f"Correções Bem-Sucedidas: {ciel.successful_fixes}")
    print(f"Correções Falhas (Sem Recurso): {ciel.failed_fixes}")