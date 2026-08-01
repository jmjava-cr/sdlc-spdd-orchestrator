import os

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-github-integration",
        action="store_true",
        default=False,
        help="Run live GitHub Issues integration tests",
    )
    parser.addoption(
        "--run-viewer-e2e",
        action="store_true",
        default=False,
        help="Run Playwright ADF viewer GUI tests (needs chromium)",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    # Auto-enable when env asks for create/integration, otherwise require the flag
    # or SDLC_GITHUB_INTEGRATION=1 so default `pytest -q` stays offline-safe.
    gh_enabled = (
        config.getoption("--run-github-integration")
        or os.environ.get("SDLC_GITHUB_INTEGRATION", "0") == "1"
        or os.environ.get("SDLC_GITHUB_ISSUE_CREATE", "0") == "1"
    )
    e2e_enabled = (
        config.getoption("--run-viewer-e2e")
        or os.environ.get("SDLC_VIEWER_E2E", "0") == "1"
    )
    skip_gh = pytest.mark.skip(
        reason="need --run-github-integration or SDLC_GITHUB_INTEGRATION=1"
    )
    skip_e2e = pytest.mark.skip(
        reason="need --run-viewer-e2e or SDLC_VIEWER_E2E=1 (and playwright chromium)"
    )
    for item in items:
        if not gh_enabled and "github_integration" in item.keywords:
            item.add_marker(skip_gh)
        if not e2e_enabled and "viewer_e2e" in item.keywords:
            item.add_marker(skip_e2e)
