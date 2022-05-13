.PHONY: lint test infra app

lint:
	flake8 app/

test:
	pytest app/

infra:
	docker-compose -f local/docker-compose.infra.yaml up --remove-orphans

app:
	docker build . -t hex:latest
	docker-compose -f local/docker-compose.app.yaml up --remove-orphans

web:
	hypercorn "app.api.factory:app()" -b 127.0.0.1:5000 --reload