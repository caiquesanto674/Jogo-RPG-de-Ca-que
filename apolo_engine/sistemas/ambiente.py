# -*- coding: utf-8 -*-

import datetime

class Mundo:
    """ Contém e gerencia todas as entidades e o ambiente do jogo. """
    def __init__(self, servico_gps, servico_tempo):
        self.entidades = []
        self.servico_gps = servico_gps
        self.servico_tempo = servico_tempo

    def adicionar_entidade(self, entidade):
        self.entidades.append(entidade)

class SistemaDeDiagnostico:
    """ Ferramentas para monitorar a saúde do jogo e simular falhas. """
    def verificar_integridade(self, mundo):
        print("\n[Diagnóstico] Verificando integridade do sistema...")
        for entidade in mundo.entidades:
            if entidade.vida <= 0:
                print(f"[Diagnóstico] Alerta: Entidade '{entidade.nome}' com vida inválida.")

class ServicoGPS:
    """ Simula um serviço de GPS. """
    def obter_localizacao(self):
        return (-23.5505, -46.6333)

class ServicoDeTempo:
    """ Simula um serviço de tempo. """
    def obter_hora_atual(self):
        return datetime.datetime.now()
