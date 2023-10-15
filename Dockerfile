FROM python:3.9

WORKDIR /code/

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./alembic.ini /code/alembic.ini
COPY ./alembic /code/alembic
COPY ./.env /code/.env
COPY ./entrypoint.sh /code/entrypoint.sh
COPY ./models /code/models

COPY ./app /code/app

CMD ["./entrypoint.sh"]
