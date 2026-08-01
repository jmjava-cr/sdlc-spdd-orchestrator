"""python -m sdlc_engine.viewer --root … --port 5050"""

from __future__ import annotations

import argparse
from pathlib import Path

from .app import run_viewer


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="ADF WYSIWYG ticket viewer")
    p.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repo root containing adf/ (default: cwd)",
    )
    p.add_argument("--host", default="127.0.0.1", help="Bind address (default 127.0.0.1)")
    p.add_argument("--port", type=int, default=5050)
    p.add_argument("--debug", action="store_true")
    p.add_argument(
        "--lan",
        action="store_true",
        help="Bind 0.0.0.0 for LAN access (opt-in; default is localhost only)",
    )
    args = p.parse_args(argv)
    root = args.root or Path.cwd()
    host = "0.0.0.0" if args.lan else args.host
    run_viewer(root, host=host, port=args.port, debug=args.debug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
