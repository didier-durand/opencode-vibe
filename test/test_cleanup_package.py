import os

import pytest

from src.cleanup_package import list_pkg_versions
from src.utils import on_github


@pytest.mark.skipif(on_github(), reason="not working on GitHub")
def test_list_versions():
    token = os.getenv("GITHUB_TOKEN")
    if token is not None:
        repo = os.getenv("GITHUB_REPOSITORY")
        if repo is not None and "/" in repo:
            container = os.getenv("GITHUB_REPOSITORY").split("/")[-1]
            versions = list_pkg_versions(
                token=os.getenv("GITHUB_TOKEN"), container=container
            )
            print(f"versions: {len(versions)}")
            if versions is not None and len(versions) > 0:
                for version in versions:
                    assert isinstance(version, dict)
                    # print(version)
