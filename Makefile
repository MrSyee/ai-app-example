format:
	uv run black .
	uv run isort .
	uv run docformatter . || true

lint:
	uv run ruff check .

