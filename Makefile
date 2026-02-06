test:
	python3 manage.py migrate
	python3 manage.py test

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
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate

PORT ?= 8000
