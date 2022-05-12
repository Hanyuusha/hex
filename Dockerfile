FROM python:3.10

RUN mkdir /app
WORKDIR /app

ADD alembic.ini /app/
ADD migrations /app/migrations/
ADD run.sh /app/
RUN chmod +x run.sh

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD app /app/app/

ENV PYTHONPATH=/app

CMD ["./run.sh"]
EXPOSE 5000