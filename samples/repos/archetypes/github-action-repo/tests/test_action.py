from scripts.main import render


def test_render() -> None:
    assert render(" repo ") == "proof subject: repo"
