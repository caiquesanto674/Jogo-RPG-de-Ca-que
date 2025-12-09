# tests/test_motor.py

from apolo_engine.systems.motor import MotorApolo


def test_inicializacao_motor():
    """
    Verifica se o MotorApolo e todos os seus subsistemas são inicializados sem erros.
    """
    try:
        motor = MotorApolo()
        assert motor is not None
        assert motor.economia is not None
        assert motor.tecnologia is not None
        assert motor.base_principal is not None
        assert motor.turno == 0
    except Exception as e:
        raise AssertionError(f"A inicialização do MotorApolo falhou com a exceção: {e}") from e


def test_executar_turno():
    """Verifica se um turno do jogo executa sem erros."""
    try:
        motor = MotorApolo()
        motor.executar_turno()
        assert motor.turno == 1
    except Exception as e:
        raise AssertionError(f"A execução do turno falhou com a exceção: {e}") from e
