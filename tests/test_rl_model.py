from app import rl_model


def test_func():
    result = rl_model.main()
    assert result is not None
    assert result is dict
