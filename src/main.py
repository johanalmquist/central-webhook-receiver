import requests
from fastapi import Depends, FastAPI, Request

from .core import models
from .core.database import engine
from .core.dependencies import validate_webhook
from .core.logging import log
from .core.routers import webhook

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(webhook.router)


@app.get("/")
async def root():
    return {"message": "Hello you!"}


@app.post("/webhook")
async def parse_comming(request: Request, is_okey: bool = Depends(validate_webhook)):
    # rediect to action url
    url = "http://notification:8001/slack"
    body = await request.json()
    data = {"message": body["text"]}
    try:
        requests.post(url=url, json=data, timeout=120)
        return True
    except requests.exceptions.ReadTimeout:
        log.warning(message="Did a timed out!")
        return None
