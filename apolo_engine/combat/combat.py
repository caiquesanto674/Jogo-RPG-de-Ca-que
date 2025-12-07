# combat/combat.py
def calcular_efeito_psiquico(dano_valor, mitigacao_pct):
    dano_final = dano_valor * (1.0 - mitigacao_pct)
    return max(0.0, dano_final)
