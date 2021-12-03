from pydantic import BaseModel
from typing import Optional


class WebhookDBIn(BaseModel):
    name: str
    description: Optional[str] = None
    central_id: str
    central_token: str
    action_url: str
    activte: Optional[int] = 0
