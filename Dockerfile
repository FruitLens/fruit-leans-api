FROM python:3.9

WORKDIR /code

COPY ./alembic.ini /code/alembic.ini
COPY ./alembic /code/alembic

COPY ./.env /code/.env

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
