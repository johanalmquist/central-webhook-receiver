FROM python:3.9

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./src /code/app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
