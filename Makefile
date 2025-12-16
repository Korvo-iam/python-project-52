install:
	uv sync

build:
	./build.sh

start:
	cd hexlet-code && uv run gunicorn task_manager.wsgi --bind 0.0.0.0:$PORT

render-start:
	cd hexlet-code && gunicorn task_manager.wsgi --bind 0.0.0.0:${PORT}

collectstatic:
	cd hexlet-code && python manage.py collectstatic --noinput || true

migrate:
	cd hexlet-code && python manage.py migrate || true

PORT ?= 8000
