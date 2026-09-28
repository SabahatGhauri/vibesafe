#!/usr/bin/env bash
# Regenerate install.sh from the sources in .claude/, so the installer never
# drifts from the hook this repo runs. Run after editing either source file.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
PY="$REPO/.claude/hooks/memory_gateway.py"
SKILL="$REPO/.claude/skills/checkpoint/SKILL.md"
OUT="$HERE/install.sh"
{
  sed -n '1,/^# ---- EMBEDDED FILES ----$/p' "$HERE/install.template.sh"
  echo "write_gateway() { cat > \"\$1\" <<'MEMORY_GATEWAY_PY_EOF'"
  cat "$PY"
  echo "MEMORY_GATEWAY_PY_EOF"
  echo "}"
  echo "write_skill() { cat > \"\$1\" <<'MEMORY_GATEWAY_SKILL_EOF'"
  cat "$SKILL"
  echo "MEMORY_GATEWAY_SKILL_EOF"
  echo "}"
  sed -n '/^# ---- EMBEDDED FILES ----$/,$p' "$HERE/install.template.sh" | tail -n +2
} > "$OUT"
chmod +x "$OUT"
echo "Wrote $OUT"
