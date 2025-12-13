from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.base import BaseMilitar


class Tecnologia:
    """Gerenciamento do progresso tecnológico através de uma árvore de tecnologias."""

    def __init__(self):
        self.arvore: Dict[str, int] = {
            "IA": 1,
            "Fusao": 1,
            "Plasma": 1,
            "Biotecnologia": 1,
        }
        self.custos_pesquisa: Dict[str, Dict[str, int]] = {
            "IA": {"plasma": 100, "creditos": 1000},
            "Fusao": {"combustível": 200, "creditos": 1200},
            "Plasma": {"plasma": 150, "creditos": 800},
            "Biotecnologia": {"metal": 150, "creditos": 750},
        }

    def pesquisar(self, tema: str, base_pesquisadora: "BaseMilitar") -> bool:
        """
        Aumenta o nível de uma tecnologia, consumindo recursos e créditos da base.
        O custo aumenta com o nível da tecnologia.
        """
        if tema not in self.arvore:
            print(f"[TECNOLOGIA] Falha: Tema de pesquisa '{tema}' desconhecido.")
            return False

        nivel_atual = self.arvore[tema]
        custo = self.custos_pesquisa.get(tema, {})

        custo_recursos = {k: v * nivel_atual for k, v in custo.items() if k != "creditos"}
        custo_creditos = custo.get("creditos", 0) * nivel_atual

        # Verificar se a base tem recursos e créditos suficientes
        for recurso, valor in custo_recursos.items():
            if base_pesquisadora.recursos.get(recurso, 0) < valor:
                print(f"[TECNOLOGIA] Falha: {base_pesquisadora.local} não tem {recurso} suficiente para pesquisar {tema}.")
                return False

        if base_pesquisadora.economia.reserva < custo_creditos:
            print(f"[TECNOLOGIA] Falha: Créditos insuficientes para pesquisar {tema}.")
            return False

        # Deduzir custos
        for recurso, valor in custo_recursos.items():
            base_pesquisadora.recursos[recurso] -= valor
        base_pesquisadora.economia.transferir(custo_creditos, f"Pesquisa de {tema}")

        self.arvore[tema] += 1
        print(f"[TECNOLOGIA] Sucesso! {tema} agora está no nível {self.arvore[tema]}.")
        return True

    def __str__(self):
        return f"Tecnologia (Níveis: {self.arvore})"
