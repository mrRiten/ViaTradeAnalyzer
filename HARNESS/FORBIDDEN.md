# Forbidden Paths and Actions

## Secrets and Security

Do not inspect, print, copy, summarize, or commit values from `.env`, `.env.*`, credential files, private keys, or token files.

Never hardcode credentials or disable TLS certificate verification to bypass connection errors.

## Dependencies and Generated Files

Do not recursively inspect or modify `.venv/`, `venv/`, dependency source, caches, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, or `.ruff_cache/`.

Do not inspect or modify `.git/` internals during normal work. Use Git commands when history or repository state is relevant.

`data/` contains tracked runtime/generated CSV artifacts. Do not edit these files manually unless the task explicitly targets data. Fix producing logic under `src/` rather than patching generated results.

## Architecture

Preserve the existing responsibility flow:

`instrument API/source and MOEX clients -> trade worker -> CSV storage -> analyzers and strategies`

Keep HTTP/exchange access in API or MOEX services, orchestration in the worker/analyzer services, persistence in CSV services/repositories, and indicator/signal rules in screeners/strategies.

Do not introduce new architectural layers or dependencies without a concrete requirement.

## Exploration and Changes

Do not recursively scan the repository by default. Start from HARNESS and inspect targeted source paths.

Do not perform unrelated refactoring, silently change behavior outside the task scope, or rename existing misspelled paths and APIs (`intarfaces`, `Screnners`, `screnne`, `InstumentType`) incidentally.

Do not change dependency versions unless the task requires it.

## Validation

Do not run `src/main.py` as a routine validation command. It performs network requests and can overwrite tracked CSV files under `data/`.

Prefer side-effect-free checks such as `python -m compileall src` and focused tests when available.

Do not report a command, test, build, or validation as successful unless it was actually executed successfully.

## HARNESS

Never store secrets, raw logs, raw diffs, complete source files, temporary debugging notes, or speculative conclusions in HARNESS.

HARNESS must contain compact, durable project knowledge only.
