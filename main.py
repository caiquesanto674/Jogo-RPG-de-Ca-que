# PONTO DE ENTRADA PRINCIPAL DO APOLO ENGINE
# ============================================
# Este arquivo importa e executa o motor principal do jogo.

from apolo_engine.motor import ATLAS, Personagem, APOLO, Missao

if __name__ == "__main__":
    ATLAS.criar_regiao("Vale Inicial")

    p1 = Personagem("Kael", "Guerreiro")
    p2 = Personagem("Mira", "Arqueira")

    APOLO.registrar_personagem(p1)
    APOLO.registrar_personagem(p2)

    p1.atacar(p2)

    m1 = Missao("Defender o Vale", "Proteja o Vale Inicial de invasores.")
    APOLO.registrar_missao(m1)
    m1.atualizar(20)

    APOLO.atualizar()
