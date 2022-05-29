[![codecov](https://codecov.io/gh/Hanyuusha/hex/branch/master/graph/badge.svg?token=U6DSSZ29RW)](https://codecov.io/gh/Hanyuusha/hex)


#### HEX
Попытка накидать [Hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))

### Requirements
1. Python >= 3.10
2. Docker, docker-compose

### Быстрый запуск
Запускает инфраструктуру, собирает приложение, поднимает WEB API [compose file](/local/docker-compose.app.yaml).

`make app`

### Подготовка к запуску
1. Установка poetry: `pip install poetry`
2. Установка зависимостей: `poetry install`
3. Поднятие локальной инфраструктуры: `make infra`
4. Выставить необходимые переменные окружения через: `export ENV_NAME=value`
5. Запуск миграций: `poetry run alembic upgrade head`

### WEB API
`make web`

### Интерактивный шелл
`make cli`

### Запуск тестов
`make test`

### Линтер
`make lint`

### Swagger
При запуске с `API_TYPE=fast` swagger будет автоматически доступен по адресу [/docs](/docs)

### Описание переменных окружения


| ENV          | Описание                                   | required | default   |
|--------------|--------------------------------------------|----------|-----------|
| DB_USER      | DB Login                                   | +        |           |
| DB_PASSWORD  | DB password                                | +        |           |
| DB_HOST      | DB host                                    | -        | localhost |
| DB_PORT      | DB port                                    | -        | 5557      |
| DB_NAME      | DB name                                    | -        | db        |
| REDIS_HOST   | Redis host                                 | -        | localhost |
| REDIS_PORT   | Redis port                                 | -        | 6379      |
| REDIS_DB     | Redis DB                                   | -        | 1         |
| STORE_TYPE   | Тип хранилища "redis" или "sql"            | -        | redis     |
| API_TYPE     | Тип используемого API "fast", "flask"      | -        | fast      |
| BIND_ADDRESS | Адрес на котором будет работать приложение | -        | localhost |
| BIND_PORT    | Порт на котором будет работать приложение  | -        | 5000      |


