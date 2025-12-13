# -*- coding: utf-8 -*-

class MemoriaIA:
    """ Armazena as experiências de uma entidade para tomada de decisão. """
    def __init__(self):
        self.memoria_curto_prazo = []  # Eventos do turno atual
        self.memoria_longo_prazo = {}   # Fatos aprendidos que persistem

    def adicionar_evento_curto_prazo(self, evento):
        self.memoria_curto_prazo.append(evento)

    def adicionar_fato_longo_prazo(self, chave, valor):
        self.memoria_longo_prazo[chave] = valor
        print(f"  -> [Memória de Longo Prazo] Fato aprendido: {chave} = {valor}")

    def limpar_memoria_curto_prazo(self):
        self.memoria_curto_prazo = []
