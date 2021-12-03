from fastapi import Request, HTTPException, Depends
from .validation import VerifySignature, find_webhook
from sqlalchemy.orm import Session
from .database import get_database

# import hashlib
# import hmac
# import base64


async def validate_webhook(request: Request, db: Session = Depends(get_database)):
    webhook = await find_webhook(request=request, db=db)
    token = webhook.central_token
    if not await VerifySignature(request=request, token=token):
        raise HTTPException(status_code=403, detail="failure")
    return True
