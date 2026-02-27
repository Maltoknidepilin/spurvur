#!/usr/bin/env bash
set -euo pipefail

dry_run=false
if [[ "${1-}" == "--dry-run" ]]; then
  dry_run=true
elif [[ "${1-}" == "-h" || "${1-}" == "--help" ]]; then
  echo "Usage: $0 [--dry-run]"
  exit 0
elif [[ -n "${1-}" ]]; then
  echo "Unknown argument: $1" >&2
  echo "Usage: $0 [--dry-run]" >&2
  exit 2
fi

shell_name="${SHELL##*/}"
case "$shell_name" in
  zsh)
    rc_file="$HOME/.zshrc"
    ;;
  bash)
    rc_file="$HOME/.bashrc"
    ;;
  *)
    rc_file="$HOME/.zshrc"
    echo "Unsupported shell '$shell_name'; defaulting to zsh rc: $rc_file"
    ;;
esac

start_marker="# >>> sparv-uv-completion >>>"
end_marker="# <<< sparv-uv-completion <<<"

if [ ! -f "$rc_file" ]; then
  echo "No rc file found at $rc_file; nothing to uninstall."
  exit 0
fi

if ! grep -Fq "$start_marker" "$rc_file"; then
  echo "No Sparv completion block found in $rc_file; nothing to uninstall."
  exit 0
fi

if $dry_run; then
  echo "[dry-run] Would remove Sparv completion block from $rc_file"
  exit 0
fi

tmp_file="$(mktemp)"
awk -v start="$start_marker" -v end="$end_marker" '
  BEGIN {in_block=0}
  $0 == start {in_block=1; next}
  $0 == end {in_block=0; next}
  !in_block {print}
' "$rc_file" > "$tmp_file"
mv "$tmp_file" "$rc_file"

echo "Removed Sparv completion block from $rc_file"
echo "Restart your shell (or run: source \"$rc_file\")"
