#!/usr/bin/env bash
# Smoke tests for the memory gateway installer and hook. Runs entirely in a
# throwaway HOME and git repo; touches nothing real. Exit 0 = all passed.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
export HOME="$TMP/home"; mkdir -p "$HOME"
FAIL=0
check() { if eval "$2"; then echo "ok   - $1"; else echo "FAIL - $1"; FAIL=1; fi; }
G="$HOME/.claude/hooks/memory_gateway.py"
gw() { python3 "$G" "$@" --global; }
gitq() { git -c user.email=t@t -c user.name=t "$@"; }

# install.sh must match its sources
cp "$HERE/install.sh" "$TMP/before.sh"; bash "$HERE/build.sh" >/dev/null
check "install.sh is up to date with its sources (run build.sh)" 'cmp -s "$TMP/before.sh" "$HERE/install.sh"'

# a user's own hook must survive install and uninstall
mkdir -p "$HOME/.claude"
echo '{"hooks":{"Stop":[{"matcher":"","hooks":[{"type":"command","command":"echo mine"}]}]},"theme":"dark"}' > "$HOME/.claude/settings.json"
bash "$HERE/install.sh" >/dev/null && bash "$HERE/install.sh" >/dev/null
check "install is idempotent (3 hooks, not 6)" '[ "$(grep -c memory_gateway.py "$HOME/.claude/settings.json")" = 3 ]'
check "status reports installed" 'bash "$HERE/install.sh" status >/dev/null'
check "existing user hook kept" 'grep -q "echo mine" "$HOME/.claude/settings.json"'

REPO="$TMP/repo"; git init -q "$REPO"; gitq -C "$REPO" commit -q --allow-empty -m init
export CLAUDE_PROJECT_DIR="$REPO"; cd "$REPO"
cat > "$TMP/t.jsonl" <<'J'
{"type":"user","message":{"role":"user","content":"Fix the login redirect"}}
{"type":"user","message":{"role":"user","content":[{"type":"tool_result","content":"x"}]}}
{"type":"user","message":{"role":"user","content":"<system-reminder>noise</system-reminder>"}}
not json
J
echo "{\"transcript_path\":\"$TMP/t.jsonl\"}" | gw snapshot
OUT="$(echo '{"session_id":"s","source":"compact"}' | gw restore)"
check "compaction restores the user's request" '[[ "$OUT" == *"Fix the login redirect"* ]]'
check "tool results and reminders are filtered" '[[ "$OUT" != *noise* ]]'
check "snapshot is stored outside the repo" '[ -z "$(git -C "$REPO" status --short)" ]'
check "stop is quiet with no new commits" '[ -z "$(echo "{\"session_id\":\"s\"}" | gw stop)" ]'
gitq commit -q --allow-empty -m work
check "stop nudges after a commit without notes" '[[ "$(echo "{\"session_id\":\"s\"}" | gw stop)" == *block* ]]'
check "stop nudges only once per commit" '[ -z "$(echo "{\"session_id\":\"s\"}" | gw stop)" ]'
gitq commit -q --allow-empty -m more; sleep 1
mkdir -p .claude/memory; echo notes > .claude/memory/NOTES.md
check "stop is quiet once notes are updated" '[ -z "$(echo "{\"session_id\":\"s\"}" | gw stop)" ]'
check "stop never loops" '[ -z "$(echo "{\"session_id\":\"s\",\"stop_hook_active\":true}" | gw stop)" ]'
check "bad input never fails the session" 'echo garbage | gw restore >/dev/null'
mkdir -p .claude/hooks; touch .claude/hooks/memory_gateway.py
check "global copy steps aside for a repo's own copy" '[ -z "$(echo {} | gw restore)" ]'

bash "$HERE/install.sh" uninstall >/dev/null
check "uninstall removes our hooks" '! grep -q memory_gateway.py "$HOME/.claude/settings.json"'
check "uninstall keeps the user's hook and settings" 'grep -q "echo mine" "$HOME/.claude/settings.json" && grep -q dark "$HOME/.claude/settings.json"'
check "status reports not installed" '! bash "$HERE/install.sh" status >/dev/null'

mkdir -p "$HOME/.claude/skills/checkpoint"; echo "my own skill" > "$HOME/.claude/skills/checkpoint/SKILL.md"
bash "$HERE/install.sh" >/dev/null
check "a user's own /checkpoint skill is not overwritten" 'grep -q "my own skill" "$HOME/.claude/skills/checkpoint/SKILL.md"'

[ "$FAIL" = 0 ] && echo "all tests passed" || { echo "some tests FAILED"; exit 1; }
