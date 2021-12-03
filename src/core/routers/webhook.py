from fastapi import APIRouter, Depends
from ...core.database import get_database
from sqlalchemy.orm import Session
from ...core.schemas import WebhookDBIn
from ...core.models import Webhook

router = APIRouter(prefix="/core", tags=["core"])


@router.post("/")
async def create_webhook(webhook: WebhookDBIn, db: Session = Depends(get_database)):
    db_webhook = Webhook(**webhook.dict())
    db.add(db_webhook)
    db.commit()
    db.refresh(db_webhook)
    return db_webhook
