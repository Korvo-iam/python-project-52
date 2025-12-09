install:
	uv sync

build:
	./build.sh

start:
	uv run gunicorn hexlet_code.wsgi --bind 0.0.0.0:$PORT

render-start:
	gunicorn hexlet_code.wsgi --bind 0.0.0.0:$PORT

collectstatic:
	python manage.py collectstatic --noinput || true

migrate:
	python manage.py migrate || true

PORT ?= 8000
