# systems/tecnologia.py
from typing import Dict

class Tecnologia:
    def __init__(self):
        self.nivel = 1
        self.arvore = []
        self.pesquisas_disponiveis = {
            "Escudo Psiônico SSSS": {"materia_escura_ssss": 100, "eter": 500}
        }

    def pesquisar(self, nome: str, base_militar):
        """Pesquisa uma nova tecnologia se os recursos estiverem disponíveis."""
        if nome not in self.pesquisas_disponiveis:
            print(f"Tecnologia '{nome}' desconhecida.")
            return False

        custo = self.pesquisas_disponiveis[nome]
        recursos_suficientes = all(base_militar.recursos.get(res, 0) >= qtd for res, qtd in custo.items())

        if recursos_suficientes:
            for res, qtd in custo.items():
                base_militar.recursos[res] -= qtd

            self.nivel += 1
            self.arvore.append(nome)
            print(f"🔬 Tecnologia pesquisada: {nome} | Nível Tecnológico da Base: {self.nivel}")
            return True
        else:
            print(f"Recursos insuficientes para pesquisar {nome}.")
            return False
