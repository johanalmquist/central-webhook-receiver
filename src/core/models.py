from sqlalchemy import Column, Integer, String, Boolean

from .database import Base


class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255), unique=True, index=True, nullable=False)
    description = Column(String(length=255), nullable=True)
    central_id = Column(String(length=255), unique=True, index=True, nullable=False)
    central_token = Column(String(length=255), unique=True, index=True, nullable=False)
    action_url = Column(String(length=255), unique=True, nullable=False)
    activte = Column(Boolean, default=0)
