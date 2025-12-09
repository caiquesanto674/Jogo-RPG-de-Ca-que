# Arquivo: fonte/nexus_core.py

"""
Núcleo do Multiverso RPG.
Contém as classes principais para o jogo (Entidade, Personagem, Inimigo, etc.)
e a lógica central de combate e inventário.
"""

from typing import Any, Dict


class Inventario:
    """Gerencia o inventário de uma entidade."""

    def __init__(self):
        # O inventário é um dicionário {item_nome: quantidade}
        self.itens: Dict[str, Any] = {}

    def adicionar_item(self, item_nome: str, item_propriedades: Any, quantidade: int = 1):
        """Adiciona um item ao inventário."""
        # Simplificação: armazena as propriedades do item na primeira vez
        if item_nome not in self.itens:
            self.itens[item_nome] = {
                "quantidade": 0,
                "propriedades": item_propriedades,
            }

        self.itens[item_nome]["quantidade"] += quantidade
        print(f"{item_nome} adicionado ao inventário.")

    def remover_item(self, item_nome: str, quantidade: int = 1) -> bool:
        """Remove um item do inventário. Retorna True se bem-sucedido."""
        if item_nome in self.itens and self.itens[item_nome]["quantidade"] >= quantidade:
            self.itens[item_nome]["quantidade"] -= quantidade
            if self.itens[item_nome]["quantidade"] == 0:
                del self.itens[item_nome]
            print(f"{item_nome} removido do inventário.")
            return True
        print(f"Erro: Não há {item_nome} suficiente para remover.")
        return False

    def usar_pocao(self, item_nome: str, entidade: "Entidade") -> bool:
        """
        Tenta usar uma poção, se existir.
        Note que a lógica de cura real deve estar na Entidade.
        """
        if self.remover_item(item_nome):
            if item_nome == "Poção de Cura Simples":
                # Lógica de cura - o valor real pode vir das propriedades
                cura = 15
                entidade.vida += cura
                entidade.vida = min(entidade.vida, entidade.vida_maxima)
                print(f"{entidade.nome} usou Poção de Cura Simples e curou {cura} de vida.")
                return True
        return False


class Entidade:
    """Classe base para qualquer ser vivo ou objeto interativo no jogo."""

    def __init__(self, nome: str, vida: int, forca: int):
        self.nome = nome
        self.vida_maxima = vida
        self.vida = vida
        self.forca = forca
        self.inventario = Inventario()
        print(f"Entidade '{self.nome}' criada.")

    def esta_vivo(self) -> bool:
        """Verifica se a entidade ainda tem vida."""
        return self.vida > 0

    def calcular_dano(self, defesa_alvo: int) -> int:
        """Calcula o dano base a ser infligido."""
        # Fórmula de dano simples: Força - (Defesa do Alvo / 2)
        dano_base = self.forca - (defesa_alvo // 2)
        return max(1, dano_base)  # Garante pelo menos 1 de dano

    def atacar(self, outra_entidade: "Entidade"):
        """Realiza uma ação de ataque contra outra entidade."""
        if not self.esta_vivo():
            print(f"{self.nome} não pode atacar, pois está fora de combate.")
            return

        # Para simplificar, assumimos que todas as entidades têm uma defesa básica
        dano = self.calcular_dano(outra_entidade.forca)

        outra_entidade.vida -= dano
        outra_entidade.vida = max(0, outra_entidade.vida)  # Vida não pode ser negativa

        print(f"{self.nome} atacou {outra_entidade.nome} e causou {dano} de dano.")

        if not outra_entidade.esta_vivo():
            print(f"{outra_entidade.nome} foi derrotado(a).")


class Personagem(Entidade):
    """Representa o personagem jogável."""

    def __init__(self, nome: str, vida: int, forca: int, classe: str):
        super().__init__(nome, vida, forca)
        self.classe = classe
        # Adiciona um item inicial para teste
        self.inventario.adicionar_item("Poção de Cura Simples", {"cura": 15}, 2)
        print(f"Personagem '{self.nome}' da classe {self.classe} pronto para o Multiverso!")


class Inimigo(Entidade):
    """Representa um inimigo controlado pela IA."""

    def __init__(self, nome: str, vida: int, forca: int, tipo: str):
        super().__init__(nome, vida, forca)
        self.tipo = tipo
        print(f"Inimigo '{self.nome}' ({self.tipo}) surgiu.")

    # Lógica de IA simples para o inimigo atacar automaticamente
    def acao_ia(self, alvo: "Entidade"):
        """Decisão de ação simples da IA."""
        if self.esta_vivo() and alvo.esta_vivo():
            # A IA do inimigo sempre ataca
            self.atacar(alvo)


# Função de demonstração do sistema
def iniciar_combate_simples():
    """Demonstra o uso das classes."""
    print("\n--- INICIANDO COMBATE SIMPLES ---")

    jogador = Personagem(nome="Herói Cardinal", vida=100, forca=25, classe="Nexus Lord")
    monstro = Inimigo(nome="Slime de Conflito", vida=50, forca=10, tipo="Elementar")

    # Adiciona algo no inventário do jogador (já adicionado na inicialização)
    jogador.inventario.usar_pocao("Poção de Cura Simples", jogador)

    print("\n--- TURNO 1 ---")
    jogador.atacar(monstro)
    monstro.acao_ia(jogador)

    print("\n--- STATUS FINAIS ---")
    print(f"Vida de {jogador.nome}: {jogador.vida}/{jogador.vida_maxima}")
    print(f"Vida de {monstro.nome}: {monstro.vida}/{monstro.vida_maxima}")

    if jogador.esta_vivo() and not monstro.esta_vivo():
        print("Vitória! O Guardião do Código funcionou!")
