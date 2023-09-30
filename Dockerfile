FROM python:3.9

WORKDIR /code/

COPY ./app /code/app
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/
COPY ./models /code/models
COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN alembic upgrade head

# CMD ["uvicorn", "app.main:app"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
