.PHONY: server

server:
	python src/manage.py runserver

.PHONY: migrations

migrations:
	python src/manage.py makemigrations
	python src/manage.py migrate

.PHONY: psql

psql:
	docker exec -u ${POSTGRES_USERNAME} -it db psql -d ${POSTGRES_DB}

.PHOMY: formatting

formatting:
	isort .
	black .