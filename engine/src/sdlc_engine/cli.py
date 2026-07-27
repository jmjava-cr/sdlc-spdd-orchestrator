"""CLI entrypoint: sdlc-engine / python -m sdlc_engine."""

from __future__ import annotations

import argparse
import subprocess
import sys

from . import __version__
from .archive import ArchiveService
from .pointer import PointerError, PointerStore
from .project import Project
from .registry import TeamRegistry
from .workflow import WorkflowEngine


def _project(args: argparse.Namespace) -> Project:
    return Project.resolve(getattr(args, "root", None))


def cmd_next(args: argparse.Namespace) -> int:
    print(WorkflowEngine(_project(args)).next_text(), end="")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    eng = WorkflowEngine(_project(args))
    if args.json:
        print(eng.status_json(args.work_id))
    else:
        wid = args.work_id or eng.pointer.get() or "(none)"
        print(f"Pointer: {eng.pointer.get() or '(none)'}")
        print(f"Work ID: {wid}")
        if eng.pointer.get() or args.work_id:
            print(eng.status_json(args.work_id))
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    state = WorkflowEngine(_project(args)).resume(args.work_id, phase=args.phase, force=args.force)
    print(f"Resumed {state.work_id} at phase: {state.phase}")
    return 0


def cmd_advance(args: argparse.Namespace) -> int:
    state = WorkflowEngine(_project(args)).advance(to=args.to)
    print(f"Advanced to phase: {state.phase}")
    return 0


def cmd_skip(args: argparse.Namespace) -> int:
    state = WorkflowEngine(_project(args)).skip(args.phase, reason=args.reason)
    print(f"Skipped {args.phase}; now at {state.phase}")
    return 0


def cmd_shelf(args: argparse.Namespace) -> int:
    state = WorkflowEngine(_project(args)).shelf(reason=args.reason)
    if state is None:
        print("No active pointer to shelf", file=sys.stderr)
        return 1
    print(f"Shelved {state.work_id}: {args.reason}")
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    state = WorkflowEngine(_project(args)).sync(args.work_id)
    print(f"Synced {state.work_id} -> phase {state.phase}")
    return 0


def cmd_list_shelved(args: argparse.Namespace) -> int:
    rows = WorkflowEngine(_project(args)).list_shelved()
    if not rows:
        print("(no shelved work)")
        return 0
    for wid, phase, at, reason in rows:
        print(f"{wid}\t{phase}\t{at}\t{reason}")
    return 0


def cmd_claim(args: argparse.Namespace) -> int:
    reg = TeamRegistry(_project(args))
    try:
        row = reg.claim(
            args.work_id,
            force=args.force,
            phase=args.phase,
            branch=args.branch or "",
            pr=args.pr or "",
            jira=args.jira or "",
            note=args.note or "",
        )
    except PermissionError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"Claimed {row.work_id} as {row.owner} (phase={row.phase})")
    print("Team registry updated — commit agent-context/work-registry.tsv to share with teammates.")
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    TeamRegistry(_project(args)).release(reason=args.reason)
    print("Released / shelved active work")
    return 0


def cmd_team(args: argparse.Namespace) -> int:
    print(TeamRegistry(_project(args)).team_text(), end="")
    return 0


def cmd_list_work(args: argparse.Namespace) -> int:
    print(TeamRegistry(_project(args)).list_work_text(), end="")
    return 0


def cmd_sync_team(args: argparse.Namespace) -> int:
    TeamRegistry(_project(args)).refresh_done_status()
    print("Team registry refreshed from canvas Final Status.")
    return 0


def cmd_archive(args: argparse.Namespace) -> int:
    svc = ArchiveService(_project(args))
    try:
        if args.all:
            svc.archive_eligible(dry_run=args.dry_run)
        else:
            svc.archive_work(args.work_id, dry_run=args.dry_run, force=args.force)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


def cmd_pointer(args: argparse.Namespace) -> int:
    store = PointerStore(_project(args))
    try:
        if args.pointer_cmd == "get":
            print(store.get())
        elif args.pointer_cmd == "set":
            store.set(args.work_id)
            print(f"pointer set to: {args.work_id}")
        elif args.pointer_cmd == "reset":
            store.reset()
            print("pointer cleared")
        else:
            return 2
    except PointerError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


def cmd_version(_: argparse.Namespace) -> int:
    print(__version__)
    return 0


def cmd_shell(args: argparse.Namespace) -> int:
    """Bridge to remaining v1 shell scripts under scripts/."""
    root = _project(args).root
    script = root / "scripts" / args.script
    if not script.is_file():
        # also allow bare names that live in scripts/
        candidate = root / "scripts" / f"{args.script}.sh"
        script = candidate if candidate.is_file() else script
    if not script.is_file():
        print(f"shell bridge: script not found: {args.script}", file=sys.stderr)
        return 1
    return subprocess.call([str(script), *args.script_args], cwd=root)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sdlc-engine",
        description="SDLC-SPDD Python orchestration engine (v2)",
    )
    p.add_argument("--root", help="Project root (default: SDLC_ROOT or git toplevel)")
    p.add_argument("--version", action="store_true", help="Print engine version")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("next", help="Show what to do now").set_defaults(func=cmd_next)

    st = sub.add_parser("status", help="Show workflow status")
    st.add_argument("--json", action="store_true")
    st.add_argument("--work-id")
    st.set_defaults(func=cmd_status)

    rs = sub.add_parser("resume", help="Resume a Work ID")
    rs.add_argument("work_id")
    rs.add_argument("--phase")
    rs.add_argument("--force", action="store_true")
    rs.set_defaults(func=cmd_resume)

    adv = sub.add_parser("advance", help="Advance workflow phase")
    adv.add_argument("--to")
    adv.set_defaults(func=cmd_advance)

    sk = sub.add_parser("skip", help="Skip a phase")
    sk.add_argument("phase")
    sk.add_argument("--reason", default="manual skip")
    sk.set_defaults(func=cmd_skip)

    sh = sub.add_parser("shelf", help="Shelf active work")
    sh.add_argument("--reason", default="manual shelf")
    sh.set_defaults(func=cmd_shelf)

    sy = sub.add_parser("sync", help="Sync workflow state from artifacts")
    sy.add_argument("--work-id")
    sy.set_defaults(func=cmd_sync)

    sub.add_parser("list-shelved", help="List shelved work").set_defaults(func=cmd_list_shelved)

    cl = sub.add_parser("claim", help="Claim a Work ID")
    cl.add_argument("work_id")
    cl.add_argument("--force", action="store_true")
    cl.add_argument("--phase")
    cl.add_argument("--branch")
    cl.add_argument("--pr")
    cl.add_argument("--jira")
    cl.add_argument("--note")
    cl.set_defaults(func=cmd_claim)

    rel = sub.add_parser("release", help="Release/shelf active claim")
    rel.add_argument("--reason", default="released")
    rel.set_defaults(func=cmd_release)

    sub.add_parser("team", help="Show team registry").set_defaults(func=cmd_team)
    sub.add_parser("list-work", help="List Work IDs").set_defaults(func=cmd_list_work)
    sub.add_parser("sync-team", help="Refresh done/cancelled from canvases").set_defaults(func=cmd_sync_team)

    ar = sub.add_parser("archive", help="Archive completed/cancelled work")
    ar.add_argument("work_id", nargs="?")
    ar.add_argument("--all", action="store_true")
    ar.add_argument("--dry-run", action="store_true")
    ar.add_argument("--force", action="store_true")
    ar.set_defaults(func=cmd_archive)

    ptr = sub.add_parser("pointer", help="Pointer get/set/reset")
    ptr.add_argument("pointer_cmd", choices=["get", "set", "reset"])
    ptr.add_argument("work_id", nargs="?")
    ptr.set_defaults(func=cmd_pointer)

    shell = sub.add_parser("shell", help="Run a v1 scripts/*.sh via bridge")
    shell.add_argument("script")
    shell.add_argument("script_args", nargs=argparse.REMAINDER)
    shell.set_defaults(func=cmd_shell)

    sub.add_parser("version", help="Print version").set_defaults(func=cmd_version)
    return p


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "version", False) and not getattr(args, "command", None):
        return cmd_version(args)
    if not getattr(args, "command", None):
        # default to next for parity with sdlc.sh
        args.command = "next"
        args.func = cmd_next
    try:
        return int(args.func(args))
    except Exception as exc:  # noqa: BLE001 - CLI boundary
        print(f"sdlc-engine: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
