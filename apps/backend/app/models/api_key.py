from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.enums import ApiScope
from uuid import uuid4
import secrets
import hashlib


def generate_api_key():
    """Generate a new API key with prefix"""
    return f"sk-{secrets.token_urlsafe(32)}"


def hash_api_key(key: str) -> str:
    """One-way hash of the API key using SHA-256"""
    return hashlib.sha256(key.encode()).hexdigest()


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    organization_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)
    name = Column(String, nullable=False)
    key_hash = Column(String, nullable=False, unique=True, index=True)  # Store SHA-256 hash of the key
    key_prefix = Column(String, nullable=False)  # Store first and last chars for identification (e.g., "sk-abc...efg")
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    scopes = Column(ARRAY(Enum(ApiScope)), nullable=False, default=[])  # Array of permission scopes

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User", back_populates="api_keys")
    organization = relationship("Organization", back_populates="api_keys")