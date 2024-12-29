PHONY: database

database:
	docker-compose down
	docker-compose up -d

	sleep 5

	docker exec -u postgres postgresql_db \
		psql -c "CREATE DATABASE driving WITH ENCODING 'UTF-8';"

	docker exec -u postgres postgresql_db \
		psql -c "CREATE DATABASE warriors WITH ENCODING 'UTF-8';"


PHONY: warriors

warriors:
	python warriors_project/manage.py makemigrations
	python warriors_project/manage.py migrate
	python warriors_project/manage.py runserver