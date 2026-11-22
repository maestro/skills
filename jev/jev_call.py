#!/usr/bin/env python3
"""Call Jev (TypeSafe System One) directly.

stdin : JSON {"state": ..., "questions": {...}}  (model defaults to jev-latest)
stdout: JSON {"ok", "latency_ms", "model", "answers", "usage"} or {"ok": false, "status", "error"}
The API key is read from the macOS Keychain (service typesafe-api-key) and never printed.
"""
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request

URL = "https://api.typesafe.ai/v1/systemone"
TIMEOUT = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0


def get_key():
    out = subprocess.run(
        ["security", "find-generic-password", "-a", subprocess.getoutput("id -un"),
         "-s", "typesafe-api-key", "-w"],
        capture_output=True, text=True, timeout=5,
    )
    if out.returncode != 0:
        raise RuntimeError("API key not found in Keychain (service typesafe-api-key)")
    return out.stdout.strip()


def main():
    body = json.load(sys.stdin)
    body.setdefault("model", "jev-latest")
    start = time.monotonic()
    try:
        req = urllib.request.Request(
            URL,
            data=json.dumps(body).encode(),
            headers={"Authorization": "Bearer " + get_key(), "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.load(resp)
        data.update(ok=True, latency_ms=round((time.monotonic() - start) * 1000))
        print(json.dumps(data, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        print(json.dumps({"ok": False, "status": e.code,
                          "error": e.read().decode(errors="replace")[:1000],
                          "latency_ms": round((time.monotonic() - start) * 1000)}))
    except Exception as e:  # timeout, DNS, keychain, etc.
        print(json.dumps({"ok": False, "status": None, "error": f"{type(e).__name__}: {e}",
                          "latency_ms": round((time.monotonic() - start) * 1000)}))


main()
