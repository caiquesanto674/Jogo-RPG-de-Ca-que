# -*- coding: utf-8 -*-

import random
import datetime

# Importação necessária para a classe Mundo
from motor_apolo.entidades.entidade import Entidade

class SistemaDecisaoFonte:
    """ Centraliza todas as regras e cálculos do jogo (o 'S.D.F'). """
    def __init__(self):
        self.regras = {
            "dano_base": 10,
            "modificador_forca": 1.5,
            "cura_base_pocao": 20
        }

    def calcular_dano(self, forca):
        """ Calcula o dano de um ataque com base na força da entidade. """
        return self.regras["dano_base"] + (forca * self.regras["modificador_forca"])

    def calcular_cura(self):
        """ Calcula a quantidade de vida que uma poção restaura. """
        return self.regras["cura_base_pocao"] + random.randint(0, 10)

class Mundo:
    """ Contém e gerencia todas as entidades e o ambiente do jogo. """
    def __init__(self, servico_gps, servico_tempo):
        self.entidades = []
        self.servico_gps = servico_gps
        self.servico_tempo = servico_tempo

    def adicionar_entidade(self, entidade: Entidade):
        self.entidades.append(entidade)

# ==============================================================================
# MÓDulos DE SIMULAÇÃO E DIAGNÓSTICO
# ==============================================================================

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
