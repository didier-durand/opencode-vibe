import os


def on_github() -> bool:
    if (
        os.getenv("GITHUB_JOB") is not None
        and len(os.getenv("GITHUB_JOB")) > 0
        and os.getenv("GITHUB_SHA") is not None
        and len(os.getenv("GITHUB_SHA")) > 0
    ):
        return True
    return False
