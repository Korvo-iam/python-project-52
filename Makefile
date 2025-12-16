install:
	uv sync

build:
	./build.sh

start:
	uv run gunicorn task_manager.wsgi --bind 0.0.0.0:$PORT

render-start:
	gunicorn task_manager.wsgi --bind 0.0.0.0:${PORT}

collectstatic:
	python manage.py collectstatic --noinput || true

migrate:
	python manage.py migrate || true

PORT ?= 8000
