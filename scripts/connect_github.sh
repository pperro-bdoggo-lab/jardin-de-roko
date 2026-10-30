#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Uso: $0 git@github.com:USUARIO/jardin-de-roko.git" >&2
  exit 64
fi

REMOTE_URL="$1"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: $ROOT no es un repositorio git." >&2
  exit 1
fi

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE_URL"
  echo "origin actualizado -> $REMOTE_URL"
else
  git remote add origin "$REMOTE_URL"
  echo "origin agregado -> $REMOTE_URL"
fi

if [ -z "$(git config user.name || true)" ] || [ -z "$(git config user.email || true)" ]; then
  echo
  echo "Aviso: faltan user.name/user.email. Configúralos antes del primer commit:"
  echo "  git config user.name \"Tu Nombre\""
  echo "  git config user.email \"tu@email\""
fi

if git ls-remote --exit-code --heads origin main >/dev/null 2>&1; then
  git fetch origin main
  if git show-ref --verify --quiet refs/heads/main; then
    git branch --set-upstream-to=origin/main main
    echo
    echo "Remoto listo. Para traer cambios:"
    echo "  git pull"
  else
    echo
    echo "El remoto tiene main, pero la rama local aún no tiene commits."
    echo "Para partir del remoto sin perder archivos locales:"
    echo "  git reset --mixed origin/main"
    echo "Luego revisa, haz commit y ejecuta:"
    echo "  git push -u origin main"
  fi
else
  echo
  echo "El remoto no tiene una rama main todavía (repo vacío o inaccesible)."
  echo "Cuando exista el primer commit local:"
  echo "  git add ."
  echo "  git commit -m \"Initial commit: JR-0.1 walking skeleton\""
  echo "  git push -u origin main"
fi
