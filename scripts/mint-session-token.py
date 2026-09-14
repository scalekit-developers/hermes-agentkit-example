#!/usr/bin/env python3
"""Mint a Virtual MCP session token. create_config is already done."""

import os
import sys
from datetime import timedelta

from scalekit import ScalekitClient

REQUIRED = (
    "SCALEKIT_ENVIRONMENT_URL",
    "SCALEKIT_CLIENT_ID",
    "SCALEKIT_CLIENT_SECRET",
    "SCALEKIT_IDENTIFIER",
    "SCALEKIT_MCP_CONFIG_ID",
)


def load_hermes_env() -> None:
    env_file = os.path.join(
        os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")),
        ".env",
    )
    if not os.path.isfile(env_file):
        return
    with open(env_file, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            if key and key not in os.environ:
                os.environ[key] = value


def main() -> int:
    load_hermes_env()
    missing = [name for name in REQUIRED if not os.environ.get(name)]
    if missing:
        print("Missing: " + ", ".join(missing), file=sys.stderr)
        return 1

    client = ScalekitClient(
        env_url=os.environ["SCALEKIT_ENVIRONMENT_URL"],
        client_id=os.environ["SCALEKIT_CLIENT_ID"],
        client_secret=os.environ["SCALEKIT_CLIENT_SECRET"],
    )
    response = client.actions.mcp.create_session_token(
        mcp_config_id=os.environ["SCALEKIT_MCP_CONFIG_ID"],
        identifier=os.environ["SCALEKIT_IDENTIFIER"],
        expiry=timedelta(hours=1),
    )
    if not response.token:
        print("create_session_token returned an empty token.", file=sys.stderr)
        return 1
    print(response.token)
    return 0


if __name__ == "__main__":
    sys.exit(main())
