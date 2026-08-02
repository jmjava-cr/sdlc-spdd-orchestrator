"""ADF Viewer lifecycle APIs on the ops console (mocked process)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

pytest.importorskip("flask")

from sdlc_engine.installer.app import create_app
from sdlc_engine.installer import viewer_runtime as vr


class _FakeProc:
    def __init__(self, pid: int = 4242) -> None:
        self.pid = pid


def test_viewer_url_and_probe_tcp_closed() -> None:
    assert vr.viewer_url("127.0.0.1", 5050) == "http://127.0.0.1:5050/"
    probe = vr.probe_viewer("127.0.0.1", 1, timeout=0.05)  # port 1 unlikely open
    assert probe["tcp_open"] is False
    assert probe["http_ok"] is False


def test_api_adf_status_default(tmp_path: Path) -> None:
    app = create_app(tmp_path)
    client = app.test_client()
    res = client.post("/api/adf", json={"target": str(tmp_path)})
    assert res.status_code == 200
    body = res.get_json()
    assert body["ok"] is True
    assert "5050" in body["url"]
    assert body["process"]["alive"] is False
    assert "sdlc_engine.viewer" in body["cli"]


def test_api_adf_start_stop_restart(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[list[str]] = []
    fake_pid = {"n": 9001}

    def fake_popen(cmd: list[str], **kwargs: Any) -> _FakeProc:
        calls.append(list(cmd))
        fake_pid["n"] += 1
        return _FakeProc(fake_pid["n"])

    monkeypatch.setattr(vr.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(vr, "_tcp_open", lambda *a, **k: False)
    monkeypatch.setattr(vr, "_pid_alive", lambda pid: True)
    monkeypatch.setattr(vr, "probe_viewer", lambda host="127.0.0.1", port=5050, **k: {
        "host": host,
        "port": port,
        "tcp_open": True,
        "http_ok": True,
        "url": f"http://{host}:{port}/",
        "detail": "HTTP 200",
    })
    monkeypatch.setattr(vr, "_run", lambda *a, **k: {"ok": True, "log": "", "exit_code": 0})

    killed: list[int] = []

    def fake_kill(pid: int, sig: int = 0) -> None:
        if sig != 0:
            killed.append(pid)

    def fake_killpg(pid: int, sig: int) -> None:
        killed.append(pid)

    monkeypatch.setattr(vr.os, "kill", fake_kill)
    monkeypatch.setattr(vr.os, "killpg", fake_killpg)
    monkeypatch.setattr(vr.time, "sleep", lambda *_a, **_k: None)

    app = create_app(tmp_path)
    client = app.test_client()

    start = client.post(
        "/api/adf/start",
        json={"target": str(tmp_path), "host": "127.0.0.1", "port": 5050},
    )
    assert start.status_code == 200
    body = start.get_json()
    assert body["ok"] is True
    assert body["result"]["ok"] is True
    assert calls and "sdlc_engine.viewer" in calls[0]
    assert (tmp_path / ".sdlc" / "adf-viewer-runtime.json").is_file()

    # Already running → 400
    again = client.post(
        "/api/adf/start",
        json={"target": str(tmp_path), "host": "127.0.0.1", "port": 5050},
    )
    assert again.status_code == 400
    assert again.get_json()["ok"] is False

    stop = client.post("/api/adf/stop", json={"target": str(tmp_path)})
    assert stop.status_code == 200
    assert stop.get_json()["ok"] is True
    assert not (tmp_path / ".sdlc" / "adf-viewer-runtime.json").is_file()

    # Restart after stop
    monkeypatch.setattr(vr, "_pid_alive", lambda pid: False)
    restart = client.post(
        "/api/adf/restart",
        json={"target": str(tmp_path), "port": 5055},
    )
    assert restart.status_code == 200
    assert restart.get_json()["ok"] is True
    assert any("5055" in c for c in calls[-1])


def test_start_viewer_missing_target(tmp_path: Path) -> None:
    missing = tmp_path / "gone"
    result = vr.start_viewer(missing)
    assert result["ok"] is False
    assert "not found" in result["error"]


def test_start_viewer_port_in_use(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(vr, "_pid_alive", lambda pid: False)
    monkeypatch.setattr(vr, "_tcp_open", lambda *a, **k: True)
    result = vr.start_viewer(tmp_path, port=5050)
    assert result["ok"] is False
    assert "already in use" in result["error"]
