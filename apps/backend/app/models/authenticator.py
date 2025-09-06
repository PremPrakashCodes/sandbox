from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Authenticator(Base):
    __tablename__ = "authenticators"

    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    credential_id = Column(String, primary_key=True, unique=True, nullable=False)
    provider_account_id = Column(String, nullable=False)
    credential_public_key = Column(String, nullable=False)
    counter = Column(Integer, nullable=False)
    credential_device_type = Column(String, nullable=False)
    credential_backed_up = Column(Boolean, nullable=False)
    transports = Column(String, nullable=True)

    user = relationship("User", back_populates="authenticators")