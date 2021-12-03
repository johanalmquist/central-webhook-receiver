from fastapi import Request, HTTPException
import hashlib
import hmac
import base64
from sqlalchemy.orm import Session
from .models import Webhook


async def VerifySignature(request: Request, token):
    CentralSignature = request.headers.get("X-Central-Signature")
    CentralService = request.headers.get("X-Central-Service")
    CentralDeliveryID = request.headers.get("X-Central-Delivery-ID")
    CentralDeliveryTimestamp = request.headers.get("X-Central-Delivery-Timestamp")
    body = await request.body()
    body = body.decode("utf-8")
    messagge = "{}{}{}{}".format(
        body, CentralService, CentralDeliveryID, CentralDeliveryTimestamp
    )
    message = bytes(messagge, "utf-8")
    secret = bytes(token, "utf-8")
    hash = hmac.new(secret, message, hashlib.sha256)
    hashonhash = base64.b64encode(hash.digest())
    calculatedSign = hashonhash.decode("utf-8")
    if calculatedSign == CentralSignature:
        return True

    return False


async def find_webhook(request: Request, db: Session):
    body = await request.json()
    webhook = body["webhook"]
    db_wb = db.query(Webhook).filter(Webhook.central_id == webhook).first()
    if db_wb is None:
        raise HTTPException(status_code=404, detail="Webhook not found in database")

    if db_wb.activte is False:
        raise HTTPException(status_code=403, detail="Webhook is not activte")

    return db_wb
