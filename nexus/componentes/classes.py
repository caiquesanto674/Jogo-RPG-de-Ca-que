from typing import Any, Dict

# Definição dos perfis de classes táticas
CLASSES_NEXUS: Dict[str, Dict[str, Any]] = {
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
}
