#!/usr/bin/python3
import base64
import json
import os

import requests

MAX_VERSIONS = 6
PKG_PREFIX = "opencode"
ARCHITECTURES = ["amd64", "arm64"]

GITHUB_API_ACCEPT = "application/vnd.github+json"
GITHUB_API_VERSION = "2022-11-28"
GHCR_API_ACCEPT = "application/vnd.oci.image.index.v1+json"
GHCR_MANIFEST_LIST_TYPE = "application/vnd.docker.distribution.manifest.list.v2+json"
OCI_IMAGE_MANIFEST_TYPE = "application/vnd.oci.image.manifest.v1+json"
GHCR_SCHEMA_VERSION = 2


def get_gh_api_session(token: str = "") -> requests.Session:
    if not hasattr(get_gh_api_session, "session"):
        session = requests.Session()
        session.headers.update(
            {
                "Authorization": f"token {token}",
                "Accept": GITHUB_API_ACCEPT,
                "X-GitHub-Api-Version": GITHUB_API_VERSION,
            }
        )
        get_gh_api_session.session = session
    return get_gh_api_session.session

def get_ghcr_api_session(
    token: str = "", owner: str = "", repository: str = ""
) -> requests.Session:
    assert len(token) > 0
    assert len(owner) > 0
    assert len(repository) > 0
    if not hasattr(get_ghcr_api_session, "session"):
        session = requests.Session()
        basic_encoded: str = base64.b64encode(
            bytes(f"{owner}:{token}", "utf-8")
        ).decode("utf8")
        session.headers.update(
            {
                "Authorization": f"Basic {basic_encoded}",
            }
        )
        token_url = (
            f"https://ghcr.io/token?service=ghcr.io&scope=repository:{repository}:pull"
        )
        response = session.get(token_url)
        response.raise_for_status()
        json_resp = response.json()
        session.headers.update(
            {
                "Authorization": f"Bearer {json_resp['token']}",
                "Accept": GHCR_API_ACCEPT,
            }
        )
        get_ghcr_api_session.session = session
    return get_ghcr_api_session.session


def list_pkg_versions(token: str = "", container: str = "") -> list[dict] | None:
    assert len(token) > 0
    assert len(container) > 0
    session = get_gh_api_session(token)

    list_url: str | None = (
        f"https://api.github.com/user/packages/container/{container}/versions"
    )

    version_list = []

    while list_url is not None:
        print(f"list_url for session.get(): <{list_url}>")
        resp = session.get(list_url)
        resp.raise_for_status()
        if "link" in resp.headers and "next" in resp.links:
            list_url = resp.links["next"]["url"]
            print(f"More result pages, next is <{list_url}>")
        else:
            list_url = None

        v_list = resp.json()

        if v_list is not None:
            version_list.extend(v_list)
    if len(version_list) == 0:
        return None
    return version_list


def sort_pkg_versions(
    version_list: list[dict], max_versions: int = -1
) -> tuple[list[dict], list[dict]]:
    assert max_versions > 0
    kept_version_list: list[dict] = []
    deleted_version_list: list[dict] = []
    filtered_version_dict: dict[str, dict] = {}
    for version in version_list:
        tags = version["metadata"]["container"]["tags"]
        opencode_tag: str = ""
        for tag in tags:
            if tag.startswith(PKG_PREFIX):
                opencode_tag = tag
                filtered_version_dict[opencode_tag] = version
                break
        if opencode_tag == "":
            deleted_version_list.append(version)
    filtered_version_dict = dict(sorted(filtered_version_dict.items(), reverse=True))
    count: int = 0
    for _, version in filtered_version_dict.items():
        count += 1
        if count <= max_versions:
            kept_version_list.append(version)
        else:
            deleted_version_list.append(version)
    return (
        kept_version_list,
        deleted_version_list,
    )


def get_image_manifests(
    token: str = "",
    owner: str = "",
    repository: str = "",
    tag_prefix: str = "",
    version: dict = None,
) -> tuple[str | None, list[str] | None]:
    assert isinstance(version, dict)
    assert "/" in repository
    tags = version["metadata"]["container"]["tags"]
    opencode_tag: str = ""
    if len(tags) > 0:
        for tag in tags:
            if tag.startswith(tag_prefix):
                opencode_tag = tag
    if opencode_tag == "":
        return None, None
    #
    session = get_ghcr_api_session(token=token, owner=owner, repository=repository)
    response = session.get(f"https://ghcr.io/v2/{repository}/manifests/{opencode_tag}")
    response.raise_for_status()
    json_dict = response.json()
    assert isinstance(json_dict, dict)
    print(f"manifests for tag {opencode_tag}:")
    print(json.dumps(json_dict,indent=4))
    assert json_dict["schemaVersion"] == GHCR_SCHEMA_VERSION
    manifests = json_dict["manifests"]
    assert len(manifests) > 0
    sha256_list = []
    for manifest in manifests:
        sha256_digest = manifest["digest"]
        assert sha256_digest.startswith("sha256:")
        sha256_list.append(sha256_digest)
    return opencode_tag, sha256_list


def delete_pkg_version(session: requests.Session, container: str, version: dict) -> None:
    v_id = version["id"]
    resp = session.delete(
        f"https://api.github.com/user/packages/container/{container}/versions/{v_id}"
    )
    resp.raise_for_status()
    print(f"deleted pkg version with id: {v_id}")


if __name__ == "__main__":
    if os.getenv("GITHUB_TOKEN"):
        gh_token = os.getenv("GITHUB_TOKEN")
    else:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    assert len(gh_token) > 0

    gh_repository = os.getenv("GITHUB_REPOSITORY")
    assert len(gh_repository) > 0
    assert "/" in gh_repository

    repo_owner, oc_container = gh_repository.split("/")
    assert len(repo_owner) > 0
    assert len(oc_container) > 0

    pkg_versions = list_pkg_versions(token=gh_token, container=oc_container)
    kept_pkg_versions, deleted_pkg_versions = sort_pkg_versions(
        pkg_versions, max_versions=MAX_VERSIONS
    )
    assert isinstance(kept_pkg_versions, list)
    assert isinstance(deleted_pkg_versions, list)
    print("kept_pkg_versions:")
    print(json.dumps(kept_pkg_versions,indent=4))

    kept_manifests: dict[str, list[str]] = {}
    for pkg_version in kept_pkg_versions:
        opencode_version, version_manifests = get_image_manifests(
            token=gh_token,
            owner=repo_owner,
            repository=gh_repository,
            tag_prefix=PKG_PREFIX,
            version=pkg_version,
        )
        assert len(version_manifests) > 0
        kept_manifests[opencode_version] = version_manifests

    print(f"\n\nremoving pkg versions if more than: {MAX_VERSIONS}")
    for pkg_version in deleted_pkg_versions:
        digest = pkg_version["name"]
        assert digest.startswith("sha256:")
        for opencode_version, digests in kept_manifests.items():
            if digest in digests:
                print(f"manifest {digest} in kept versions for:  {opencode_version}")
                break
        else:
            print(f"deleting pkg version {pkg_version}")
            delete_pkg_version(session=get_gh_api_session(gh_token),container=oc_container,version=pkg_version)
