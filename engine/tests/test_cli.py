from pathlib import Path

from sdlc_engine.cli import main


def test_cli_claim_next_archive(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SDLC_USER", "cli-user")
    work_id = "FEAT-030-cli"
    canvas = tmp_path / "spdd" / "canvas" / f"{work_id}.md"
    canvas.parent.mkdir(parents=True)
    canvas.write_text(
        f"# {work_id}\n\n## Final Status\n\n- Status: Complete\n",
        encoding="utf-8",
    )
    assert main(["--root", str(tmp_path), "claim", work_id]) == 0
    assert main(["--root", str(tmp_path), "next"]) == 0
    assert main(["--root", str(tmp_path), "archive", work_id]) == 0
    assert (tmp_path / "spdd" / "canvas" / "archive" / f"{work_id}.md").is_file()
    assert main(["--root", str(tmp_path), "version"]) == 0


def test_cli_version_flag() -> None:
    assert main(["--version"]) == 0
