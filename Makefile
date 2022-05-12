.PHONY: lint test infra app

lint:
	flake8 app/

test:
	pytest app/

infra:
	docker-compose -f docker-compose.infra.yaml up --remove-orphans

app:
	docker-compose -f docker-compose.app.yaml up --remove-orphans

web:
	hypercorn "app.api.flask.factory:create_asgi_app()" -b 127.0.0.1:5000 --reload