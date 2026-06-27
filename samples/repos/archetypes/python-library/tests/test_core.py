from acme_widget import normalize_name


def test_normalize_name() -> None:
    assert normalize_name("Release Proof") == "release-proof"
