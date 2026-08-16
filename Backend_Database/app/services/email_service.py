import os
import logging
import httpx

logger = logging.getLogger("EmailService")

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM", "MarketMind AI <onboarding@resend.dev>")

def send_email_via_resend(to_email: str, subject: str, html_content: str) -> bool:
    """Send an email using Resend REST API or fallback to logging if API key is not configured."""
    if not RESEND_API_KEY:
        logger.warning(
            f"[EMAIL SERVICE SIMULATION]\n"
            f"To: {to_email}\n"
            f"Subject: {subject}\n"
            f"Body:\n{html_content}\n"
            f"----------------------------------------"
        )
        # Always return True for simulations/local tests
        return True

    try:
        response = httpx.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": EMAIL_FROM,
                "to": [to_email],
                "subject": subject,
                "html": html_content
            },
            timeout=10.0
        )
        if response.status_code in [200, 201]:
            logger.info(f"Email sent successfully to {to_email}")
            return True
        else:
            logger.error(f"Resend returned error status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error sending email via Resend to {to_email}: {str(e)}")
        return False

def send_invitation_email(to_email: str, code: str, signup_url: str) -> bool:
    """Send signup invitation containing code and registration URL."""
    subject = "You're invited to join MarketMind AI"
    html_content = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 8px;">
        <h2 style="color: #ff4b4b;">Welcome to MarketMind AI</h2>
        <p>Hello,</p>
        <p>You have been invited to join a business account on MarketMind AI.</p>
        <p>Your unique invitation code is:</p>
        <div style="background-color: #f7f7f9; padding: 15px; border-radius: 6px; font-size: 20px; font-weight: bold; letter-spacing: 2px; text-align: center; color: #171f32; margin: 20px 0;">
            {code}
        </div>
        <p>This invitation code is single-use and valid for <strong>24 hours</strong>.</p>
        <p>To create your account, visit the link below and enter your email along with the invitation code:</p>
        <p style="text-align: center; margin: 30px 0;">
            <a href="{signup_url}" style="background-color: #ff4b4b; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">Create Your MarketMind AI Account</a>
        </p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;" />
        <p style="font-size: 12px; color: #888;">If you did not expect this invitation, you can safely ignore this email.</p>
    </div>
    """
    return send_email_via_resend(to_email, subject, html_content)

def send_otp_email(to_email: str, otp: str) -> bool:
    """Send 6-digit OTP verification code."""
    subject = "Your MarketMind AI verification code"
    html_content = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee; border-radius: 8px;">
        <h2 style="color: #ff4b4b;">Verify Your Email Address</h2>
        <p>Hello,</p>
        <p>Your MarketMind AI verification code is:</p>
        <div style="background-color: #f7f7f9; padding: 15px; border-radius: 6px; font-size: 24px; font-weight: bold; letter-spacing: 4px; text-align: center; color: #171f32; margin: 20px 0;">
            {otp}
        </div>
        <p>This verification code is valid for <strong>5 minutes</strong>.</p>
        <p>Do not share this verification code with anyone.</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;" />
        <p style="font-size: 12px; color: #888;">If you did not request this code, you can ignore this email.</p>
    </div>
    """
    return send_email_via_resend(to_email, subject, html_content)
