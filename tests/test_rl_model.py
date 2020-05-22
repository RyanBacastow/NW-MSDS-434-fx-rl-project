import rl_model


def test_func():
    result = rl_model.main(curr_pair="EUR/USD", period="1d", interval="1m", window_size=25, unit_side='left')
    assert result is not None
    assert type(result) is dict
