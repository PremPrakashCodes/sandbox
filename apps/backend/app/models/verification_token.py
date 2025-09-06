from sqlalchemy import Column, String, DateTime
from app.core.database import Base


class VerificationToken(Base):
    __tablename__ = "verification_tokens"

    identifier = Column(String, primary_key=True, nullable=False)
    token = Column(String, primary_key=True, nullable=False)
    expires = Column(DateTime(timezone=True), nullable=False)