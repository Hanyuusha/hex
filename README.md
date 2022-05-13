#### HEX
Попытка накидать [Hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))

Для простого CRUD она к сожелени избыточна, поэтому куда воткнуть `domain layer` я не нашёл, но в остальном постарался соблюсти концепцию.

### Requirements
1. Python >= 3.10
2. Docker, docker-compose

### Быстрый запуск
Запускает инфру и билдит приложение

`make app`

### Подготовка к запуску
1. `pip install -r requirements.txt`
2. `make infra`
3. Выставить необходимые переменные окружения через `export ENV_NAME=value`
4. Запуск миграций `alembic upgrade head`

### WEB API
`make web`

### CLI
`python -m app --store=<STORE TYPE> --uid=<USER ID>`

### Запуск тестов
`make test`

### Линтер
`make lint`

### Описание переменных окружения


| ENV         | Описание                               | required | default        |
|-------------|----------------------------------------|----------|----------------|
| DB_USER     | DB Login                               | +        |                |
| DB_PASSWORD | DB password                            | +        |                |
| DB_HOST     | host:port                              | -        | localhost:5557 |
| DB_NAME     | DB name                                | -        | db             |
| REDIS_HOST  | Redis host                             | -        | localhost      |
| REDIS_PORT  | Redis port                             | -        | 6379           |
| REDIS_DB    | Redis DB                               | -        | 1              |
| STORE_MODE  | Store "redis" or "sql"                 | -        | redis          |
| API_TYPE    | Тип используемого API "fast", "flask"  | -        | fast           |


