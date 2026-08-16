from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean
from app.core.database import Base

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False)
    otp_hash = Column(String(64), nullable=False)
    session_token = Column(String(64), unique=True, nullable=False, index=True)
    expires_at = Column(TIMESTAMP, nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    used = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )
