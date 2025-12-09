from src.nexus_core import NexusCore


def test_nexus_core_inicializacao():
    """Verifica se o NexusCore é inicializado sem erros."""
    try:
        engine = NexusCore()
        assert engine is not None
        assert engine.turno == 0
        assert engine.protagonista.nome == "CAÍQUE APOLO Ω"
    except Exception as e:
        raise AssertionError(f"A inicialização do NexusCore falhou com a exceção: {e}") from e


def test_ciclo_do_jogo_executa():
    """Verifica se o ciclo principal do jogo executa uma vez sem levantar exceções."""
    try:
        engine = NexusCore()
        engine.ciclo()
        assert engine.turno == 1
    except Exception as e:
        raise AssertionError(f"O método ciclo() do NexusCore falhou com a exceção: {e}") from e
