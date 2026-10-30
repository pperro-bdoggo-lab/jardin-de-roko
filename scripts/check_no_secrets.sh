#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PATTERN='(sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|api[_-]?key[[:space:]]*[:=][[:space:]]*["'"'"'][A-Za-z0-9_-]{12,}|password[[:space:]]*[:=][[:space:]]*["'"'"'][^"'"'"']{8,})'

matches="$(
  grep -RInE "$PATTERN" . \
    --exclude-dir=.git \
    --exclude-dir=.venv \
    --exclude-dir=node_modules \
    --exclude-dir=__pycache__ \
    --exclude=.env.example \
    --exclude=check_no_secrets.sh || true
)"

if [ -n "$matches" ]; then
  echo "Posibles secretos detectados:" >&2
  echo "$matches" >&2
  exit 1
fi

echo "OK: no se detectaron secretos evidentes."
