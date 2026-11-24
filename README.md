# Credit Risk Early Warning System

**Status: Phase 1 — initial environment and software skeleton only.**

Educational portfolio project: monthly early-warning surveillance of
residential mortgages. The proposed target is future reported 90+ delinquency
within six reporting months, **not** regulatory PD or prevented credit loss.

This repository contains no Freddie Mac source records. Initial tests use
**entirely invented** loan-month data.

## Windows / PowerShell setup

Prerequisites: Git and Python 3.12 on PATH, plus an internet connection for
initial package installation.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

If `py -3.12` does not exist but `python --version` reports 3.12,
replace the first line with `python -m venv .venv`.

Activation is optional: `./.venv/Scripts/Activate.ps1` (PowerShell). Calling
`./.venv/Scripts/python.exe` directly does not require changing PowerShell's
script-execution policy.

## Next step

Phase 2 will examine the real Freddie Mac data dictionary, file structures,
reporting delay, access and publication limitations. No source data should be
published merely because it can be downloaded.

## Main layout

- `configs/` — configuration without secrets.
- `data/fixtures/` — synthetic illustrative CSV.
- `data/raw/`, `data/interim/`, `data/processed/` — private local data.
- `src/credit_risk_ews/` — reusable code.
- `tests/` — automatic tests.
- `docs/` — requirements, glossary, risks and architecture decisions.

See `docs/architecture.md` for scope and `docs/adr/0001-environment-and-layout.md`
for implementation decisions.
