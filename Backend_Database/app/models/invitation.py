from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from app.core.database import Base

class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    code_hash = Column(String(64), unique=True, nullable=False, index=True)
    status = Column(String(20), default="PENDING", nullable=False)  # PENDING, USED, EXPIRED, REVOKED
    expires_at = Column(TIMESTAMP, nullable=False)
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )
    created_by = Column(String(100), nullable=True)
    used_at = Column(TIMESTAMP, nullable=True)
    signup_token_hash = Column(String(64), nullable=True, index=True)
