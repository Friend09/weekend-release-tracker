# Weekend release tracker

A small Python service for learning branches, pull requests, automated tests,
and deployment to development and production using GitHub Actions.

Use fictional data only. This app does not store data.

## Local setup

Run these commands from this repository's root directory:

```bash
uv sync --locked
```

The committed `pyproject.toml` declares dependencies; `uv.lock` records their
resolved versions. uv creates the local `.venv` environment.

## Run tests

```bash
uv run --locked python -m pytest -q
```

The initial app has 12 test cases. The optional days-conversion exercise adds more.

## Start the local app

```bash
uv run --locked python -m flask --app app run --host 127.0.0.1 --port 5050
```

Open http://127.0.0.1:5050/ in a browser. Stop the server with Control-C.

## Routes

| Route                   | Purpose                                           |
| ----------------------- | ------------------------------------------------- |
| `/`                     | Show the release message, environment, and commit |
| `/health`               | Report readiness, environment, and commit         |
| `/api/hours?minutes=90` | Return 90 minutes as 1.5 hours                    |

The conversion route accepts integer minutes from 0 through 1440 and returns
HTTP 400 for invalid input.

## GitHub Setup

merging into main branch requires a PR

## Release workflow

Work on a feature branch and open a pull request into `main`.
CI must pass before a normal merge. Once the delivery lesson is configured,
the merged commit is tested and deployed to development. Production waits
for approval, then deploys the same commit. Confirm the live commit at
`/health` in each environment.

Keep credentials and deploy-hook URLs in the configured GitHub environment
secrets, never in source files or notes.
