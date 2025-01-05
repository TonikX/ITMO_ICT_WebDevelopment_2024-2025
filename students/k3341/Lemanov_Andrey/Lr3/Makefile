debug:
	docker-compose up --build --force-recreate --remove-orphans

up:
	docker-compose up --build -d --force-recreate

down:
	docker-compose down

local:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

test:
	pip install -e .
	pip install pytest pytest-cov pytest-mock
	pytest --cov=app --cov-report=html -v
