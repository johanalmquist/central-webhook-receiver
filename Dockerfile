FROM tiangolo/uvicorn-gunicorn:python3.9-slim

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./src /code/app

EXPOSE 8000

