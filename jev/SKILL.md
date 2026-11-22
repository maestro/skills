---
name: jev
description: Use Jev (TypeSafe System One) to sort, classify, score or decide about piles of text, e.g. "use Jev to sort these". Jev returns typed answers (choice / score / yes-probability) fast and cheaply; it never writes text. Jev decides, Claude writes.
---

# Using Jev

Jev answers typed questions about text. Three shapes only:
- `choice`: pick one option from `criteria` (map option -> description). Returns `choice`, `probabilities`, `confidence`.
- `score`: place on an ordered `criteria` array (2-10 levels, lowest first). Returns `score` (0-based, probability-weighted), `probabilities`, `confidence`.
- `noul`: probability (0-1) a yes/no condition holds. Returns `noul` only.

## Call it
Direct API, not OpenRouter. Helper reads the key from the macOS Keychain (service `typesafe-api-key`); never print or write the key anywhere.

```
python3 -I ~/.claude/skills/jev/jev_call.py [timeout_s] < request.json
```
Request: `{"state": <text or object>, "questions": {"id": {"type", "instructions", "criteria"}}}` (model defaults to `jev-latest`).
Output: `{"ok", "latency_ms", "model", "answers", "usage": {input_tokens, output_tokens}}` or `{"ok": false, "status", "error"}`.
Endpoint: `POST https://api.typesafe.ai/v1/systemone`. The API reports no cost; only token counts.
Put several independent questions about the same text in one request (parallel, cheaper). For many texts, one request per text.

## Rules
- PRIVACY: everything sent to Jev leaves this computer. Ask the user before sending anything private or confidential.
- Jev decides, Claude writes. Do not ask Jev to generate text.
- Low certainty (choice top probability < 0.6, or noul/score near the middle) means Claude decides that item itself.
- Make each question narrow, with concrete criteria; include a "none/other" option when nothing may fit.
- On failure (ok false, 401/422/429/529, timeout), show the exact error to the user and continue without Jev.
- Docs: https://docs.typesafe.ai/llms.txt
