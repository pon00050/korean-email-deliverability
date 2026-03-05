# HOOKS.md — Local Privacy Enforcement Hooks

Two local-only guards prevent accidental commits of private files.
Neither is tracked by git; both must be re-created manually on a new machine.

---

## 1. Git pre-commit hook

**Catches all commits — human and AI.**

File: `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Blocks commits that include gitignored (private) files.
# --diff-filter=ACM excludes deletions — git rm --cached should not be blocked.
STAGED=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null)
BLOCKED=()
for file in $STAGED; do
    if git check-ignore -q --no-index "$file" 2>/dev/null; then
        BLOCKED+=("$file")
    fi
done
if [ ${#BLOCKED[@]} -gt 0 ]; then
    echo "" >&2
    echo "COMMIT BLOCKED — staged file(s) are in .gitignore (private):" >&2
    for f in "${BLOCKED[@]}"; do echo "  ✗  $f" >&2; done
    echo "" >&2
    echo "Unstage with:  git restore --staged <file>" >&2
    echo "Then retry:    git commit" >&2
    exit 1
fi
exit 0
```

Install on a new machine:
```bash
# Write the script above to .git/hooks/pre-commit, then:
chmod +x .git/hooks/pre-commit
```

**Note:** `--no-index` is required — without it, `git check-ignore` silently passes
files that were previously tracked, even if they are now in `.gitignore`.

---

## 2. Claude Code PreToolUse hook

**Catches Claude's `git commit` calls before they run — early warning layer.**

Files:
- `.claude/hooks/guard-private-files.py`
- `.claude/settings.json`

The hook fires before every `Bash` tool call containing `git commit`, checks staged
files against `.gitignore` using `--no-index`, and exits 2 (block + stderr to Claude)
if any match.

### `.claude/hooks/guard-private-files.py`

```python
#!/usr/bin/env python3
"""
PreToolUse hook: blocks Claude's git commit when staged files are gitignored.
"""
import sys
import json
import subprocess

data = json.load(sys.stdin)

if data.get("tool_name") != "Bash":
    sys.exit(0)

command = data.get("tool_input", {}).get("command", "")

if "git commit" not in command:
    sys.exit(0)

result = subprocess.run(
    # --diff-filter=ACM excludes deletions — git rm --cached should not be blocked.
    ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
    capture_output=True, text=True
)
staged = [f for f in result.stdout.strip().splitlines() if f]

blocked = []
for f in staged:
    check = subprocess.run(["git", "check-ignore", "-q", "--no-index", f], capture_output=True)
    if check.returncode == 0:
        blocked.append(f)

if blocked:
    print("BLOCKED by Claude Code hook — staged file(s) are in .gitignore (private):", file=sys.stderr)
    for f in blocked:
        print(f"  ✗  {f}", file=sys.stderr)
    print("Unstage with: git restore --staged <file>", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
```

### `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/guard-private-files.py"
          }
        ]
      }
    ]
  }
}
```

Install on a new machine:
```bash
mkdir -p .claude/hooks
# Write guard-private-files.py and settings.json from the snippets above
```

Both `.claude/` files are gitignored and won't survive a fresh clone.
The git pre-commit hook (§1) remains the last-resort safety net.

---

## Why both?

| Mechanism | Catches Claude's commits | Catches manual commits | Travels with repo |
|---|---|---|---|
| `.gitignore` alone | ✅ (blocks `git add`) | ✅ (blocks `git add`) | ✅ |
| Git pre-commit hook | ✅ | ✅ | ❌ |
| Claude Code PreToolUse hook | ✅ (earlier feedback) | ❌ | ❌ |

`.gitignore` is the strongest line of defence. The hooks catch the edge cases:
`git add --force`, gaps in `.gitignore`, or human error.
