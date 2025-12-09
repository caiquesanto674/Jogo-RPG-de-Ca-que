from src.economia import Economia


def test_economia_inicializacao():
    """Verifica se a economia é inicializada com os recursos conceituais corretos."""
    economia = Economia()
    assert economia.reservas["ouro_conceitual"] == 30
    assert economia.reservas["materia_escura_ssss"] == 200
    assert economia.reservas["eter"] == 2000


def test_ciclo_ganho_consome_recursos():
    """Verifica se o ciclo de ganhos (que na verdade é de consumo) reduz os recursos."""
    economia = Economia()
    comida_inicial = economia.reservas["comida"]
    mana_inicial = economia.reservas["mana"]

    economia.ciclo_ganho()

    assert economia.reservas["comida"] < comida_inicial
    assert economia.reservas["mana"] < mana_inicial
