# testes/test_nexus_core.py

from fonte.nexus_core import Inimigo, Personagem


def test_ataque_reduz_vida():
    """Verifica se o método de ataque de uma entidade reduz a vida do alvo."""
    # Criação das entidades para o teste
    jogador = Personagem(nome="Tester", vida=100, forca=20, classe="Guerreiro")
    monstro = Inimigo(nome="Bug", vida=50, forca=10, tipo="Pequeno")

    vida_inicial_monstro = monstro.vida

    # Ação: Jogador ataca o monstro
    jogador.atacar(monstro)

    # Verificação: A vida do monstro deve ser menor que a vida inicial
    assert monstro.vida < vida_inicial_monstro


def test_entidade_derrotada_nao_ataca():
    """Verifica se uma entidade com vida zerada não pode atacar."""
    # Criação das entidades
    jogador = Personagem(nome="Tester", vida=100, forca=20, classe="Guerreiro")
    monstro = Inimigo(nome="Bug Fraco", vida=10, forca=10, tipo="Pequeno")

    # Força a derrota do monstro
    monstro.vida = 0

    vida_inicial_jogador = jogador.vida

    # Ação: Monstro tenta atacar o jogador
    monstro.atacar(jogador)

    # Verificação: A vida do jogador não deve ter mudado
    assert jogador.vida == vida_inicial_jogador
