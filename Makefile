test:
	uv run python manage.py migrate
	uv run python manage.py test

install:
	uv sync

build:
	./build.sh

start:
	uv run gunicorn task_manager.wsgi --bind 0.0.0.0:${PORT}

dev:
	uv run python manage.py runserver 0.0.0.0:${PORT}

render-start:
	gunicorn task_manager.wsgi --bind 0.0.0.0:${PORT}

collectstatic:
	uv python manage.py collectstatic --noinput

migrate:
	uv python manage.py migrate

PORT ?= 8000
