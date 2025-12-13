from enum import Enum, auto


class PersonalidadeIA(Enum):
    AGRESSIVA = auto()
    CAUTELOSA = auto()
    OPORTUNISTA = auto()
    IMPREVISIVEL = auto()
    PADRAO = auto()


# Parâmetros que definem o comportamento de cada personalidade.
# - chance_erro: A probabilidade base de tomar uma decisão "imperfeita".
# - foco_ataque: Modificador para a tendência de atacar (valores > 1.0 aumentam a chance).
# - foco_defesa: Modificador para a tendência de recuar/defender (valores > 1.0 aumentam a chance).
PARAMETROS_PERSONALIDADE = {
    PersonalidadeIA.AGRESSIVA: {
        "descricao": "Agressiva",
        "chance_erro": 0.15,  # Comete mais erros por ser impulsiva.
        "foco_ataque": 1.5,
        "foco_defesa": 0.5,
    },
    PersonalidadeIA.CAUTELOSA: {
        "descricao": "Cautelosa",
        "chance_erro": 0.05,  # Comete poucos erros.
        "foco_ataque": 0.6,
        "foco_defesa": 1.4,
    },
    PersonalidadeIA.OPORTUNISTA: {
        "descricao": "Oportunista",
        "chance_erro": 0.10,  # Erra ao julgar mal uma oportunidade.
        "foco_ataque": 1.1,
        "foco_defesa": 0.9,
    },
    PersonalidadeIA.IMPREVISIVEL: {
        "descricao": "Imprevisível",
        "chance_erro": 0.30,  # Alta chance de fazer algo inesperado.
        "foco_ataque": 1.0,
        "foco_defesa": 1.0,
    },
    PersonalidadeIA.PADRAO: {
        "descricao": "Padrão",
        "chance_erro": 0.10,
        "foco_ataque": 1.0,
        "foco_defesa": 1.0,
    },
}
