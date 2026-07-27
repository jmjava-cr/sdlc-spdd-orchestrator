import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-github-integration",
        action="store_true",
        default=False,
        help="Run live GitHub Issues integration tests",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    # Auto-enable when env asks for create/integration, otherwise require the flag
    # or SDLC_GITHUB_INTEGRATION=1 so default `pytest -q` stays offline-safe.
    import os

    enabled = (
        config.getoption("--run-github-integration")
        or os.environ.get("SDLC_GITHUB_INTEGRATION", "0") == "1"
        or os.environ.get("SDLC_GITHUB_ISSUE_CREATE", "0") == "1"
    )
    if enabled:
        return
    skip = pytest.mark.skip(
        reason="need --run-github-integration or SDLC_GITHUB_INTEGRATION=1"
    )
    for item in items:
        if "github_integration" in item.keywords:
            item.add_marker(skip)
