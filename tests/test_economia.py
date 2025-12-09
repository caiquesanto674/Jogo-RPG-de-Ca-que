# tests/test_economia.py

from apolo_engine.systems.economia import SistemaEconomia


def test_geracao_recursos():
    """Verifica se o sistema de economia gera recursos corretamente."""
    economia = SistemaEconomia(taxa_base_producao=1.0)
    recursos_iniciais = economia.recursos["MineraisRaros"]

    aumento = economia.gerar_recursos("MineraisRaros", taxa_multiplicador=2.0)

    assert aumento > 0
    assert economia.recursos["MineraisRaros"] == recursos_iniciais + aumento


def test_compra_recurso_sucesso():
    """Verifica se a compra de recursos com créditos suficientes funciona."""
    economia = SistemaEconomia()
    creditos_iniciais = economia.recursos["Creditos"]

    sucesso = economia.comprar_recurso("MineraisRaros", 10)

    assert sucesso is True
    assert economia.recursos["Creditos"] < creditos_iniciais
