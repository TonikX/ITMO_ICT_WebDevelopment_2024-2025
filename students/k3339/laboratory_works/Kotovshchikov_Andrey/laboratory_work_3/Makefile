managepy = src/manage.py


PHONY: server

server:
	python $(managepy) makemigrations
	python $(managepy) migrate
	python $(managepy) runserver


PHONY: database

database:
	docker-compose down
	docker-compose --env-file docker.env up -d

	sleep 6

	docker exec -u postgres postgresql \
		psql -c "CREATE USER $(POSTGRES_USERNAME) WITH PASSWORD '$(POSTGRES_PASSWORD)'"

	docker exec -u postgres postgresql \
		psql -c "ALTER DATABASE $(POSTGRES_DB) OWNER TO $(POSTGRES_USERNAME);"   


PHONY: psql

psql:
	docker exec -it postgresql psql -U $(POSTGRES_USERNAME) -d $(POSTGRES_DB)