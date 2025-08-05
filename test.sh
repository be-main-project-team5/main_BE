set -eo pipefail

echo "Starting ruff"
uv run ruff format
uv run ruff check --select I --fix
uv run ruff check --fix
echo "OK"
