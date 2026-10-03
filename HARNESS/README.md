# Project Harness

## Purpose

This directory contains compact project context for AI-assisted development.

The harness exists to reduce unnecessary repository exploration and preserve durable project knowledge between tasks.

It is a navigation layer, not a replacement for source code.

If HARNESS conflicts with source code, dependency metadata, or runtime configuration, the actual project files are authoritative.

## Files

### STRUCTURE.md

Compact map of the repository and application source tree.

Contains:

- important directories;
- important modules;
- one-line responsibility descriptions;
- navigation hints.

It must not contain every generated file or every implementation detail.

### NOTES.md

Durable developer knowledge that is not obvious from the directory structure.

Examples:

- architectural conventions;
- non-obvious data flows;
- known integration behavior;
- important implementation decisions;
- project-specific pitfalls.

Do not use NOTES as task history.

### FORBIDDEN.md

Hard restrictions for agents.

Contains:

- paths that should not be explored;
- files that should not be modified;
- security restrictions;
- architectural actions that are prohibited.

Restrictions should be explicit and short.

### HISTORY.md

Compact history of meaningful completed changes.

It is not a Git log.

Record only changes that may help future development or investigation.

Keep recent entries and remove obsolete detail when the file becomes too large.

### STACK.md

Current technical stack.

Contains:

- Python version;
- package manager;
- major frameworks;
- database;
- cache/queue infrastructure;
- packaging tools;
- important libraries and versions.

Versions must come from project dependency metadata, not memory or assumptions.

## Reading Strategy

Do not automatically read every HARNESS file for every task.

Default:

1. `STRUCTURE.md`
2. `FORBIDDEN.md`

Add `NOTES.md` for architecture or behavior investigation.

Add `STACK.md` for dependency or infrastructure work.

Read `HISTORY.md` only when historical context can affect the task.

## Maintenance Rules

HARNESS must remain compact.

Do not copy source code into HARNESS.

Do not store:

- raw diffs;
- stack traces;
- logs;
- secrets;
- temporary debugging information;
- complete dependency lock files;
- long explanations of implementation details.

Use short factual statements.

Update only information that remains useful after the current task ends.

## Source of Truth

Priority when information conflicts:

1. actual source/configuration;
2. dependency metadata;
3. HARNESS;
4. previous agent summaries.

Agents should correct stale HARNESS information when discovered during a task.