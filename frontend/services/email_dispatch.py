import os
import smtplib
import urllib.request
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger("EmailDispatch")


def resolve_mx_hosts(domain: str) -> list:
    """Resolve MX host servers using DNS over HTTPS with fallback to known providers."""
    domain = domain.strip().lower()
    mx_hosts = []
    try:
        req = urllib.request.Request(
            f"https://dns.google/resolve?name={domain}&type=MX",
            headers={"User-Agent": "MarketMind/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode())
            records = []
            for a in data.get("Answer", []):
                if a.get("type") == 15:
                    parts = a.get("data", "").split()
                    if len(parts) >= 2:
                        records.append((int(parts[0]), parts[1].rstrip(".")))
            records.sort(key=lambda x: x[0])
            mx_hosts = [r[1] for r in records]
    except Exception as e:
        logger.warning(f"DNS MX query failed for {domain}: {e}")

    if not mx_hosts:
        if domain == "gmail.com" or domain.endswith(".google.com"):
            mx_hosts = [
                "gmail-smtp-in.l.google.com",
                "alt1.gmail-smtp-in.l.google.com",
                "alt2.gmail-smtp-in.l.google.com"
            ]
        elif domain in ["outlook.com", "hotmail.com", "live.com"]:
            mx_hosts = ["outlook-com.olc.protection.outlook.com"]
        elif domain in ["yahoo.com", "ymail.com"]:
            mx_hosts = ["mta6.am0.yahoodns.net", "mta5.am0.yahoodns.net"]

    return mx_hosts


def dispatch_real_email(to_email: str, subject: str, html_body: str, text_body: str = "") -> bool:
    """Multi-tiered real email dispatching system:
    1. Configured SMTP (if environment credentials are provided)
    2. Resend REST API (if RESEND_API_KEY is provided)
    3. Direct MX Server Delivery (connects directly to recipient's email server)
    """
    to_email = to_email.strip()
    if not to_email or "@" not in to_email:
        return False

    if not text_body:
        text_body = html_body

    # 1. Check SMTP Credentials
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")

    if all([smtp_host, smtp_port, smtp_user, smtp_pass]):
        try:
            port = int(smtp_port)
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = smtp_user
            msg["To"] = to_email
            msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))

            server = smtplib.SMTP(smtp_host, port, timeout=10)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [to_email], msg.as_string())
            server.quit()
            logger.info(f"Successfully delivered email to {to_email} via configured SMTP.")
            return True
        except Exception as err:
            logger.warning(f"Configured SMTP failed for {to_email}: {err}")

    # 2. Check Resend REST API
    resend_key = os.getenv("RESEND_API_KEY")
    if resend_key:
        try:
            import httpx
            resp = httpx.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {resend_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "from": os.getenv("EMAIL_FROM", "MarketMind AI <onboarding@resend.dev>"),
                    "to": [to_email],
                    "subject": subject,
                    "html": html_body
                },
                timeout=10.0
            )
            if resp.status_code in [200, 201]:
                logger.info(f"Successfully sent email to {to_email} via Resend.")
                return True
            else:
                logger.warning(f"Resend returned status {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.warning(f"Resend dispatch error for {to_email}: {e}")

    # 3. Direct MX Delivery to recipient's mail exchange server
    domain = to_email.split("@")[-1].strip().lower()
    mx_hosts = resolve_mx_hosts(domain)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = "MarketMind AI <no-reply@marketmind.ai>"
    msg["To"] = to_email
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    for host in mx_hosts:
        try:
            server = smtplib.SMTP(host, 25, timeout=10)
            server.ehlo("marketmind.ai")
            if server.has_extn("STARTTLS"):
                server.starttls()
                server.ehlo("marketmind.ai")
            server.sendmail("no-reply@marketmind.ai", [to_email], msg.as_string())
            server.quit()
            logger.info(f"Successfully delivered email directly to {to_email} via MX server {host}.")
            return True
        except Exception as err:
            logger.warning(f"Direct MX delivery to {host} failed: {err}")
            continue

    return False


def send_password_reset_otp_email(to_email: str, otp: str) -> bool:
    """Send branded password reset OTP email to recipient."""
    subject = "MarketMind AI - Your Password Recovery Code"
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 560px; margin: auto; padding: 24px; border: 1px solid #e0e0e0; border-radius: 10px; background-color: #ffffff;">
        <h2 style="color: #ff4b4b; margin-top: 0;">MarketMind AI Security</h2>
        <p style="font-size: 15px; color: #333333;">Hello,</p>
        <p style="font-size: 15px; color: #333333;">You requested a password reset for your <strong>MarketMind AI</strong> account.</p>
        <p style="font-size: 15px; color: #333333;">Your One-Time Password (OTP) verification code is:</p>
        <div style="background-color: #f7f7f9; padding: 18px; border-radius: 8px; font-size: 32px; font-weight: bold; letter-spacing: 6px; text-align: center; color: #171f32; margin: 20px 0; border: 1px dashed #ff4b4b;">
            {otp}
        </div>
        <p style="font-size: 14px; color: #666666;">This verification code is valid for <strong>15 minutes</strong>. If you did not request a password reset, please ignore this email or contact support.</p>
        <hr style="border: none; border-top: 1px solid #eeeeee; margin: 24px 0;" />
        <p style="font-size: 12px; color: #999999; margin-bottom: 0;">&copy; MarketMind AI Platform. All rights reserved.</p>
    </div>
    """
    text_body = f"Hello,\n\nYour MarketMind AI password recovery OTP code is: {otp}\n\nThis code is valid for 15 minutes.\n\nBest regards,\nMarketMind AI Team"
    return dispatch_real_email(to_email, subject, html_body, text_body)
