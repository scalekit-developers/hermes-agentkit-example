#!/usr/bin/env bash
# List the GitHub connection, then run the proven read.
# Uses the installed Hermes host skill. Does not print secret values.
set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
SCRIPTS="$HERMES_HOME/skills/hermes-delegated-auth/scripts"
ENV_FILE="$HERMES_HOME/.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE. Copy .env.example there and fill the four names." >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
. "$ENV_FILE"
set +a

for name in SCALEKIT_ENVIRONMENT_URL SCALEKIT_CLIENT_ID SCALEKIT_CLIENT_SECRET SCALEKIT_IDENTIFIER; do
  if [[ -z "${!name:-}" ]]; then
    echo "Missing $name in $ENV_FILE." >&2
    exit 1
  fi
done

if [[ ! -f "$SCRIPTS/tool_exec.py" ]]; then
  echo "Host skill scripts not found at $SCRIPTS" >&2
  echo "Install first:" >&2
  echo "  hermes skills install scalekit-inc/authstack/kits/agentkit/host/hermes-delegated-auth" >&2
  exit 1
fi

cd "$SCRIPTS"
uv run tool_exec.py --list-connections --provider GITHUB
uv run tool_exec.py --execute-tool \
  --tool-name github_user_get_authenticated \
  --connection-name github-connect \
  --tool-input '{}'
