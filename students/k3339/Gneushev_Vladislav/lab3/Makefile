.PHONY: venv start start-db build test migration migrate

venv:
	rm -rf venv
	python -m venv venv
	./venv/bin/pip install -r requirements.txt

start:
	docker compose -f docker-compose.yml up --force-recreate --remove-orphans

start-db:
	docker compose -f docker-compose.yml up postgres -d

build:
	docker compose -f docker-compose.yml build

test:
	pytest tests --disable-warnings -s

migration:
	alembic revision --autogenerate

migrate:
	alembic upgrade head