FROM python:3.10

RUN useradd -u 8877 zerotwo

RUN mkdir /app
WORKDIR /app

ADD alembic.ini /app/
ADD migrations /app/migrations/
ADD run.sh /app/
RUN chmod +x run.sh

ADD poetry.lock /app/
ADD pyproject.toml /app/

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false --local
RUN poetry install --no-dev

ADD app /app/app/

ENV PYTHONPATH=/app

RUN chown -R zerotwo /app
USER zerotwo

CMD ["./run.sh"]
EXPOSE 5000