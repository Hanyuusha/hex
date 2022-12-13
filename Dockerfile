FROM python:3.10

RUN useradd -u 1337 app --create-home
USER app

WORKDIR /home/app

ADD poetry.lock /home/app
ADD pyproject.toml /home/app
ADD alembic.ini /home/app
ADD migrations /home/app/migrations/

ENV PATH="$PATH:/home/app/.local/bin"

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry install --only main

ADD app /home/app/app

CMD ["poetry", "run", "python", "-m", "app", "web"]
EXPOSE 5000