# Project History

This file records meaningful project changes that may help future agents understand the current architecture or behavior.

This is not a replacement for Git history.

## Format

Use:

`YYYY-MM-DD — area — short factual description`

Examples:

`2026-09-22 — architecture — moved SLA calculation from Telegram handler to application service`

`2026-09-22 — dependencies — upgraded SQLAlchemy and adjusted repository API`

`2026-09-22 — bot — added queued notification delivery through Redis worker`

## Current History

- 2026-09-25 — bot — extended `/employ` with NEON and exact full-name employee lookup, including ambiguous-result handling.
- 2026-09-22 — SLA — routed escalation recipients by each executor's active Telegram-binding role group.
- 2026-09-22 — database — added persistent Telegram-binding role catalog and active assignment repository.
- 2026-09-22 — harness — documented the current module map, runtime composition, queued delivery, scheduled jobs, and resolved stack.

## What to Record

Record changes involving:

- architecture;
- important business behavior;
- module responsibilities;
- integrations;
- database behavior;
- dependency changes with behavioral impact;
- important bug fixes whose cause may matter later.

## What Not to Record

Do not record:

- formatting;
- typo fixes;
- import sorting;
- temporary debugging;
- trivial renames;
- every changed file;
- raw diffs;
- failed implementation attempts.

## Size Policy

Keep approximately the latest 15-25 meaningful entries.

When the file becomes large:

1. remove obsolete entries;
2. merge closely related historical entries where useful;
3. preserve information still relevant to current architecture.

Git remains the source for complete historical detail.
