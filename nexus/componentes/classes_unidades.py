# nexus/componentes/classes_unidades.py
from typing import Any, Dict

# Definição dos perfis de classes táticas
PERFIS_UNIDADES: Dict[str, Dict[str, Any]] = {
    "Tanque": {
        "Defesa_Base": 150,
        "Forca_Base": 20,
        "Mobilidade": 3,  # Baixa Mobilidade
        "Bonus_Moral": 0.10,
        "Habilidade_Especial": "Bloqueio Tático",
    },
    "Franco-Atirador": {
        "Defesa_Base": 60,
        "Forca_Base": 45,  # Dano Alto
        "Mobilidade": 4,
        "Bonus_Alcance": 2,  # Alcance Longo
        "Habilidade_Especial": "Tiro Preciso",
    },
    "Suporte_Psi": {
        "Defesa_Base": 80,
        "Forca_Base": 5,
        "Mobilidade": 4,
        "Habilidade_Especial": "Aura de Cura Moral",  # Buff Aliados
    },
    "Engenheiro": {
        "Defesa_Base": 90,
        "Forca_Base": 15,
        "Mobilidade": 3,
        "Habilidade_Especial": "Construir Torre/Reparo",
    },
    "Drone": {
        "Defesa_Base": 40,
        "Forca_Base": 25,
        "Mobilidade": 5,  # Alta Mobilidade
        "Habilidade_Especial": "Vigilância Aérea",
    },
    "Comandante": {
        "Defesa_Base": 100,
        "Forca_Base": 30,
        "Mobilidade": 4,
        "Bonus_Comando": 0.25,  # Buff Todas Unidades Próximas
        "Habilidade_Especial": "Chamado Estratégico",
    },
    # Adicionando uma classe 'default' para compatibilidade com Inimigo
    "Inimigo": {
        "Defesa_Base": 50,
        "Forca_Base": 10,
        "Mobilidade": 4,
        "Habilidade_Especial": "N/A",
    },
    # Adicionando a classe do protagonista para compatibilidade
    "Comandante Mecha": {
        "Defesa_Base": 120,
        "Forca_Base": 85, # Balanceamento: Aumentado de 40 para 85
        "Mobilidade": 5,
        "Bonus_Comando": 0.30,
        "Habilidade_Especial": "Sincronia de Combate",
    },
}
