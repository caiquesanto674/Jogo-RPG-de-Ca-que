# -*- coding: utf-8 -*-

class SistemaDecisaoFonte:
    def __init__(self):
        self.regras = {
            "dano_base": 10,
            "modificador_forca": 1.5
        }

    def calcular_dano(self, forca):
        return self.regras["dano_base"] * (forca * self.regras["modificador_forca"])

class Personagem:
    def __init__(self, nome, forca, vida):
        self.nome = nome
        self.forca = forca
        self.vida = vida

    def atacar(self, inimigo, sistema_decisao):
        dano = sistema_decisao.calcular_dano(self.forca)
        print(f"{self.nome} ataca {inimigo.nome} e causa {dano} de dano!")
        inimigo.vida -= dano

class Inimigo:
    def __init__(self, nome, forca, vida):
        self.nome = nome
        self.forca = forca
        self.vida = vida

def main():
    # Inicialização do sistema e dos personagens
    sdf = SistemaDecisaoFonte()
    jogador = Personagem("Herói", 10, 100)
    monstro = Inimigo("Ogro", 5, 80)

    # Loop de combate simples
    while jogador.vida > 0 and monstro.vida > 0:
        jogador.atacar(monstro, sdf)
        if monstro.vida <= 0:
            print(f"{monstro.nome} foi derrotado!")
            break

        # Turno do inimigo (simplificado)
        dano_inimigo = 5  # Dano fixo para simplificar
        print(f"{monstro.nome} ataca {jogador.nome} e causa {dano_inimigo} de dano!")
        jogador.vida -= dano_inimigo

        if jogador.vida <= 0:
            print(f"{jogador.nome} foi derrotado!")
            break

        print(f"Vida do {jogador.nome}: {jogador.vida}")
        print(f"Vida do {monstro.nome}: {monstro.vida}")
        input("Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
