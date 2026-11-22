---
name: project-docs-sync
description: Use when syncing project docs to real state.
---

# Project documentation sync

For tasks like "update IDEA.md to match the project", "organize docs into a folder", "make the list of X clear" — the user wants the written doc to match ground truth, and ground truth is always a file on disk, never an earlier doc or your assumption.

## Procedure

1. **Read the actual implementation before writing anything.** List and read the real scripts/configs/pyproject (or equivalent) that do the work being documented. Treat any existing doc (IDEA.md, HANDOFF.md, README) as a *draft to verify*, not a source of truth — diff what it claims against what the code actually does, and call out drift explicitly (e.g. "doc said tool X, code actually uses Y").
2. **When the user points at an authoritative source file** (a spreadsheet of deliverables, a ticket export, a template list), read it in full and cross-map every claim in the doc to a specific row/ID/name in that file. Don't paraphrase it into your own categories without keeping the traceability (e.g. keep the source's row number or key next to your summary line) — the user will come back and ask you to reconcile against it again.
3. **Pull structured facts from the artifact that defines them, not from a description of it.** If chapter titles, config keys, or field lists exist in actual JSON/YAML/code, parse or grep them directly (e.g. a one-line `python -c "import json; ..."` loop over all template files) instead of reconstructing them from a spreadsheet's loose text — the spreadsheet and the implementation can disagree, and the implementation wins for "what will actually be produced".
4. **When consolidating scattered docs into one structure** (e.g. a `document/` folder), do not leave full duplicate copies behind. Replace the old files with a short stub that links to the new canonical location. Duplicated content drifts the next time either copy is edited — a single source of truth is the point of consolidating.
5. **Split by topic, not by session.** One concern per file (overview, setup, usage, reference, open issues, checklist), with an index/README linking them in reading order. Don't let one file accumulate every topic across a long conversation.
6. **Make status explicit per item.** When the user asks to "make the list clear", give a literal enumerated checklist with a status marker per item (done/pending) and counts, not prose that implies the list. Call out any item from the authoritative source that has no clear home in the current structure as an open question, instead of silently dropping it.
7. When the user says content "is no longer needed", delete the file and grep the whole repo for references to it (filename, relative path) — update every referring doc in the same pass, don't leave dangling links.
