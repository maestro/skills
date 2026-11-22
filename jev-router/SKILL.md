---
name: jev-router
description: Turn the Jev model router on or off, or show its status. Use when the user says "jev router on", "jev router off", "jev router status", "ルーターをオンにして", or similar. While ON, each user message is sized by Jev and routed to a helper agent (haiku/sonnet/opus/fable).
disable-model-invocation: true
---

# Jev router switch

Run exactly one command, then show its output to the user unchanged:

- on:     `python3 -I ~/.claude/jev-router/router.py on`
- off:    `python3 -I ~/.claude/jev-router/router.py off`
- status: `python3 -I ~/.claude/jev-router/router.py status`

After `on`, remind the user: while ON, every message they send (except those starting with `/`, `!` or `#`) is sent directly to TypeSafe (api.typesafe.ai), the company that makes Jev. Keep it OFF for private work.

How it works: a UserPromptSubmit hook (`router.py hook`) asks Jev to size the message as tiny / everyday / large / hardest. When Jev is at least 60% sure and the message is self-contained, the hook tells Claude to hand the job to the matching helper agent (`jev-tiny` Haiku, `jev-everyday` Sonnet, `jev-large` Opus, `jev-hardest` Fable) and relay the result. Otherwise Claude handles it. Any Jev error or timeout (3.5 s) makes the hook do nothing. Claude Code cannot switch the main model per message, so this delegation is the closest equivalent.
