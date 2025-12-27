import importlib


def test_game_api_importable():
    # Module is present and importable (may be empty)
    mod = importlib.import_module("aiden.game_api")
    assert mod is not None
