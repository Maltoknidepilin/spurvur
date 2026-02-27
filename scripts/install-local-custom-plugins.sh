#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$REPO_ROOT/.venv/bin/python"
WORKSPACE_ROOT="$(cd "$REPO_ROOT/.." && pwd)"

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: 'uv' not found in PATH. Install uv first: https://docs.astral.sh/uv/" >&2
  exit 1
fi

if [[ ! -x "$VENV_PY" ]]; then
  echo "Error: missing $VENV_PY" >&2
  echo "Run 'uv sync' in $REPO_ROOT first." >&2
  exit 1
fi

install_editable() {
  local rel_path="$1"
  local label="$2"
  local abs_path="$WORKSPACE_ROOT/$rel_path"

  if [[ ! -f "$abs_path/pyproject.toml" && ! -f "$abs_path/setup.py" ]]; then
    echo "Missing repo for $label: $abs_path (expected pyproject.toml or setup.py)" >&2
    return 2
  fi

  echo "Installing $label from $abs_path"
  uv pip install --python "$VENV_PY" -e "$abs_path"
}

# Core local deps used by custom plugins
install_editable "bendingar" "bendingar"
install_editable "fo-tokenizer" "fo-tokenizer"

# Custom Sparv plugins used by configs
install_editable "sparv-leitord-og-mark" "leitord_og_mark plugin"
install_editable "sparv-mmg-upplysingar" "mmg_metadata plugin"

echo
echo "Custom plugins installed into $REPO_ROOT/.venv"
echo "You can now run e.g.:"
echo "  sparv -d path/to/sparv/corpus-config-dir run"
