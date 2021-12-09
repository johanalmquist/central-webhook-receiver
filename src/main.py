import json

import pika
from fastapi import Depends, FastAPI, Request

from .core import models
from .core.database import engine
from .core.dependencies import validate_webhook
from .core.routers import webhook

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(webhook.router)


@app.get("/")
async def root():
    return {"message": "Hello you!"}


@app.post("/webhook")
async def parse_comming(request: Request, is_okey: bool = Depends(validate_webhook)):
    body = await request.json()
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="new-ap")
    channel.basic_publish(exchange="", routing_key="new-ap", body=json.dumps(body))
    connection.close()
