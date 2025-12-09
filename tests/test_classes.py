from src.base_militar import BaseMilitar
from src.classes import MonarcaAbsoluto
from src.economia import Economia


def test_monarca_inicializacao():
    """Verifica se o Monarca Absoluto é inicializado com status de OWNER."""
    # Mock de dependências para isolar o teste
    economia_mock = Economia()
    base_mock = BaseMilitar("Mock Base", None, economia_mock, (0, 0))

    monarca = MonarcaAbsoluto("CAÍQUE APOLO Ω", base_mock)

    assert monarca.hp == 9999
    assert monarca.cargo == "OWNER"
    assert monarca.moral == 100.0


def test_ativar_volicao_agony_overflow():
    """Verifica se a mecânica Agony Overflow ativa corretamente."""
    economia_mock = Economia()
    base_mock = BaseMilitar("Mock Base", None, economia_mock, (0, 0))
    monarca = MonarcaAbsoluto("CAÍQUE APOLO Ω", base_mock)

    # Com moral alta, não deve ativar
    monarca.moral = 50
    assert monarca.ativar_volicao() is False

    # Com moral baixa, deve ativar
    monarca.moral = 19
    assert monarca.ativar_volicao() is True
    assert monarca.ativacao_overflow is True
    assert monarca.moral == 70  # Moral é restaurada
