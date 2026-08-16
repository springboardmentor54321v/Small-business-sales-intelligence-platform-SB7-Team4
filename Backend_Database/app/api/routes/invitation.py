import datetime
import hashlib
import secrets
import os
from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.core.database import get_db
from app.models.invitation import Invitation
from app.models.otp import OTP
from app.services.email_service import send_invitation_email, send_otp_email

router = APIRouter(
    prefix="/invitations",
    tags=["Invitations"]
)

# ---------------- Pydantic Request Models ---------------- #
class CreateInvitationRequest(BaseModel):
    email: EmailStr
    role: str

class VerifyInvitationRequest(BaseModel):
    email: EmailStr
    code: str

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str
    session_token: str

class CompleteSignupRequest(BaseModel):
    email: EmailStr
    signup_token: str

# ---------------- Helper Functions ---------------- #
def generate_invitation_code() -> str:
    """Generate 12-character uppercase alphanumeric code without ambiguous letters."""
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(secrets.choice(chars) for _ in range(12))

def generate_otp_code() -> str:
    """Generate 6-digit verification code."""
    return "".join(secrets.choice("0123456789") for _ in range(6))

def hash_value(value: str) -> str:
    """Returns SHA-256 hash of a string."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

# ---------------- Endpoints ---------------- #

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_invitation(
    req: CreateInvitationRequest,
    x_user_role: str = Header(None),
    x_user_id: str = Header(None),
    db: Session = Depends(get_db)
):
    # Verify permission (only Business Owner or Admin can invite)
    if x_user_role not in ["Business Owner", "Admin", "Owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Only Business Owners can invite users."
        )

    # Validate recipient email doesn't have an active pending invitation
    existing_inv = db.query(Invitation).filter(
        Invitation.email == req.email,
        Invitation.status == "PENDING",
        Invitation.expires_at > datetime.datetime.now()
    ).first()
    if existing_inv:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Active invitation for this email already exists."
        )

    # Generate code & hash
    code = generate_invitation_code()
    code_hash = hash_value(code)
    
    expires_at = datetime.datetime.now() + datetime.timedelta(hours=24)

    new_invitation = Invitation(
        email=req.email,
        role=req.role,
        code_hash=code_hash,
        status="PENDING",
        expires_at=expires_at,
        created_by=x_user_id
    )
    db.add(new_invitation)
    db.commit()
    db.refresh(new_invitation)

    # Send email (on Render, FRONTEND_URL is set or defaults to Render frontend)
    frontend_url = os.getenv("FRONTEND_URL", "https://marketmind-ai-app.onrender.com")
    signup_url = f"{frontend_url}/?page=Signup"
    
    email_success = send_invitation_email(req.email, code, signup_url)
    if not email_success:
        # We don't fail the request, but log it
        pass

    return {
        "message": "Invitation created successfully",
        "invitation": {
            "id": new_invitation.id,
            "email": new_invitation.email,
            "role": new_invitation.role,
            "status": new_invitation.status,
            "expires_at": new_invitation.expires_at.isoformat()
        },
        "code_sim": code if not os.getenv("RESEND_API_KEY") else None  # Sim code for tests/dev
    }

@router.get("/")
def list_invitations(
    x_user_role: str = Header(None),
    db: Session = Depends(get_db)
):
    if x_user_role not in ["Business Owner", "Admin", "Owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Access restricted."
        )
        
    invitations = db.query(Invitation).order_by(Invitation.created_at.desc()).all()
    return [
        {
            "id": inv.id,
            "email": inv.email,
            "role": inv.role,
            "status": inv.status if inv.expires_at > datetime.datetime.now() or inv.status != "PENDING" else "EXPIRED",
            "expires_at": inv.expires_at.isoformat(),
            "created_at": inv.created_at.isoformat() if inv.created_at else None
        }
        for inv in invitations
    ]

@router.delete("/{id}")
def revoke_invitation(
    id: int,
    x_user_role: str = Header(None),
    db: Session = Depends(get_db)
):
    if x_user_role not in ["Business Owner", "Admin", "Owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Access restricted."
        )

    inv = db.query(Invitation).filter(Invitation.id == id).first()
    if not inv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found."
        )

    inv.status = "REVOKED"
    db.commit()
    return {"message": "Invitation revoked successfully."}

@router.post("/verify-invitation")
def verify_invitation(req: VerifyInvitationRequest, db: Session = Depends(get_db)):
    code_hash = hash_value(req.code)
    
    # Query invitation matching email & code_hash
    inv = db.query(Invitation).filter(
        Invitation.email == req.email,
        Invitation.code_hash == code_hash
    ).first()

    if not inv or inv.status != "PENDING" or inv.expires_at < datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired invitation."
        )

    # Generate session token + OTP
    session_token = secrets.token_hex(16)
    otp = generate_otp_code()
    otp_hash = hash_value(otp)
    
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=5)

    new_otp = OTP(
        email=req.email,
        otp_hash=otp_hash,
        session_token=session_token,
        expires_at=expires_at,
        attempts=0,
        used=False
    )
    db.add(new_otp)
    db.commit()

    # Send OTP email
    send_otp_email(req.email, otp)

    return {
        "message": "Invitation verified. OTP sent.",
        "session_token": session_token,
        "otp_sim": otp if not os.getenv("RESEND_API_KEY") else None  # Sim code for tests/dev
    }

@router.post("/verify-otp")
def verify_otp(req: VerifyOtpRequest, db: Session = Depends(get_db)):
    otp_record = db.query(OTP).filter(
        OTP.email == req.email,
        OTP.session_token == req.session_token,
        OTP.used == False
    ).first()

    if not otp_record or otp_record.expires_at < datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code."
        )

    if otp_record.attempts >= 5:
        otp_record.used = True
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Too many verification attempts. Please request a new code."
        )

    req_otp_hash = hash_value(req.otp)
    if otp_record.otp_hash != req_otp_hash:
        otp_record.attempts += 1
        db.commit()
        
        remaining = 5 - otp_record.attempts
        if remaining <= 0:
            otp_record.used = True
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Too many verification attempts. Please request a new code."
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code."
        )

    # OTP is correct! Mark used
    otp_record.used = True
    
    # Generate signup_token & save hash on invitation
    signup_token = secrets.token_hex(32)
    signup_token_hash = hash_value(signup_token)
    
    # Find invitation and attach token hash
    inv = db.query(Invitation).filter(
        Invitation.email == req.email,
        Invitation.status == "PENDING"
    ).first()
    
    if not inv:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired invitation."
        )
        
    inv.signup_token_hash = signup_token_hash
    db.commit()

    return {
        "message": "OTP verified successfully.",
        "signup_token": signup_token
    }

@router.post("/complete-signup")
def complete_signup(req: CompleteSignupRequest, db: Session = Depends(get_db)):
    signup_token_hash = hash_value(req.signup_token)
    
    # Query invitation matching email & token hash
    inv = db.query(Invitation).filter(
        Invitation.email == req.email,
        Invitation.signup_token_hash == signup_token_hash,
        Invitation.status == "PENDING"
    ).first()

    if not inv or inv.expires_at < datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired invitation."
        )

    # Return roles & configuration
    return {
        "email": inv.email,
        "role": inv.role,
        "message": "Verification success"
    }

@router.post("/mark-used")
def mark_used(req: CompleteSignupRequest, db: Session = Depends(get_db)):
    signup_token_hash = hash_value(req.signup_token)
    
    inv = db.query(Invitation).filter(
        Invitation.email == req.email,
        Invitation.signup_token_hash == signup_token_hash,
        Invitation.status == "PENDING"
    ).first()

    if not inv:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired invitation."
        )

    inv.status = "USED"
    inv.used_at = datetime.datetime.now()
    db.commit()
    
    return {"message": "Invitation marked as used."}
