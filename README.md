# Hermes + AgentKit example

Companion to the how-to: [Use AgentKit with Hermes](https://docs.scalekit.com/agentkit/hermes/).

This repo is not a Hermes clone. It shows the install, env names, and one GitHub read that we already ran on a live host.

Hermes is the host. Scalekit stores the tokens. The host skill is `hermes-delegated-auth`.

## Install the host skill

```bash
hermes skills install scalekit-inc/authstack/kits/agentkit/host/hermes-delegated-auth
```

Then check:

```bash
hermes skills list
```

The table should list `hermes-delegated-auth` as enabled. In chat, use `/hermes-delegated-auth`.

## Configure env

Copy `.env.example` to `~/.hermes/.env` (or merge the four names into the file you already have).

| Name | What it is |
|---|---|
| `SCALEKIT_ENVIRONMENT_URL` | Dashboard → Developers → Settings → API Credentials |
| `SCALEKIT_CLIENT_ID` | Same page |
| `SCALEKIT_CLIENT_SECRET` | Same page. Do not commit it. |
| `SCALEKIT_IDENTIFIER` | Opaque user id you choose. Sample: `usr_8f3a2c` |

`SCALEKIT_IDENTIFIER` is a lookup label. It is not a dashboard credential. Do not use an email.

Create a **GitHub** connection in **Dashboard → AgentKit → Connections**. Copy the exact Connection name. This example uses `github-connect`.

## Authorize, then read

From the installed skill scripts:

```bash
cd "${HERMES_HOME:-$HOME/.hermes}/skills/hermes-delegated-auth/scripts"

uv run tool_exec.py --list-connections --provider GITHUB
uv run tool_exec.py --generate-link --connection-name github-connect
```

If status is not `ACTIVE`, open the magic link, then run `--generate-link` again.

Proven read:

```bash
uv run tool_exec.py --execute-tool \
  --tool-name github_user_get_authenticated \
  --connection-name github-connect \
  --tool-input '{}'
```

Or from this repo:

```bash
./scripts/github-whoami.sh
```

That call returns the GitHub login for `SCALEKIT_IDENTIFIER`. We ran it live against `github-connect`.

In Hermes chat:

```text
/hermes-delegated-auth who am I on GitHub?
```

## What this example does not cover

- Gmail. This environment has no Gmail connection. Do not treat unread mail as proven here.
- App-code SDKs. That is [integrate AgentKit in app code](https://docs.scalekit.com/agentkit/quickstart/), not this host skill.

## License

MIT
