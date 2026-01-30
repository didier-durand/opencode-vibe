import os

from src.utils import on_github


def test_on_github():
    if os.getenv("GITHUB_JOB") is not None:
        assert on_github() is True
    else:
        assert on_github() is False
