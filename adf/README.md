# Checked-in ADF library

Ticket description documents in Atlassian Document Format (ADF JSON).

- Edit with the local viewer: `./scripts/sdlc.sh viewer` (see [`docs/adf-viewer.md`](../docs/adf-viewer.md)).
- Naming: prefer `<ISSUE-KEY>.adf.json` (e.g. `ORCH-123.adf.json`).
- Last write wins; recover with git if two editors overwrite each other.
- Upload: `./scripts/sdlc.sh issues upload-adf <KEY> --file adf/<KEY>.adf.json --apply`
- Download (Jira hand-edits → file): `./scripts/sdlc.sh issues download-adf <KEY> --apply`
- Keep only framework seed examples here (`ORCH-*`). Project-specific ticket ADFs belong in consuming projects.
