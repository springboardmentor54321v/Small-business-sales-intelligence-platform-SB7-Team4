import os
import smtplib
import urllib.request
import json
import logging
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger("EmailDispatch")


def _load_env_files():
    """Auto-discover and load .env files from workspace, frontend, gateway, and parent dirs."""
    try:
        from dotenv import load_dotenv
        current_file = Path(__file__).resolve()
        possible_env_paths = [
            current_file.parent.parent.parent / ".env",          # Workspace root
            current_file.parent.parent / ".env",                 # Frontend root
            current_file.parent.parent.parent / "Security_APIGateway" / ".env",
            current_file.parent.parent.parent / "Backend_Database" / ".env",
            Path.cwd() / ".env",
        ]
        for env_path in possible_env_paths:
            if env_path.exists():
                load_dotenv(dotenv_path=str(env_path), override=False)
    except Exception as e:
        logger.debug(f"dotenv load skipped/failed: {e}")


# Initialize env loading on import
_load_env_files()


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


def _send_via_smtp(to_email: str, subject: str, html_body: str, text_body: str) -> tuple[bool, str]:
    """Attempt email dispatch via configured SMTP (Gmail SSL/TLS, Outlook, custom SMTP)."""
    _load_env_files()
    smtp_user = os.getenv("SMTP_USER", "").strip()
    smtp_pass = os.getenv("SMTP_PASSWORD", "").strip()
    smtp_host = os.getenv("SMTP_HOST", "").strip()
    smtp_port_raw = os.getenv("SMTP_PORT", "").strip()

    if not smtp_user or not smtp_pass:
        return False, "SMTP_USER or SMTP_PASSWORD not configured."

    # Auto-infer host and port if omitted
    if not smtp_host:
        if "@gmail.com" in smtp_user.lower():
            smtp_host = "smtp.gmail.com"
        elif any(domain in smtp_user.lower() for domain in ["@outlook.com", "@hotmail.com", "@live.com", "@office365.com"]):
            smtp_host = "smtp.office365.com"
        elif "@yahoo.com" in smtp_user.lower():
            smtp_host = "smtp.mail.yahoo.com"
        else:
            smtp_host = "smtp.gmail.com"

    port = 587
    if smtp_port_raw:
        try:
            port = int(smtp_port_raw)
        except ValueError:
            port = 587
    elif smtp_host in ["smtp.gmail.com", "smtp.mail.yahoo.com"]:
        port = 465

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_FROM", smtp_user)
    msg["To"] = to_email
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    errors = []
    # If port is 465 or default SSL
    if port == 465:
        try:
            with smtplib.SMTP_SSL(smtp_host, port, timeout=12) as server:
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, [to_email], msg.as_string())
            logger.info(f"Successfully delivered email to {to_email} via SMTP_SSL ({smtp_host}:{port}).")
            return True, f"SMTP_SSL ({smtp_host}:{port})"
        except Exception as e:
            errors.append(f"SSL 465 failed: {e}")
            # Fallback to STARTTLS on 587
            try:
                with smtplib.SMTP(smtp_host, 587, timeout=12) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_pass)
                    server.sendmail(smtp_user, [to_email], msg.as_string())
                logger.info(f"Successfully delivered email to {to_email} via SMTP STARTTLS ({smtp_host}:587).")
                return True, f"SMTP STARTTLS ({smtp_host}:587)"
            except Exception as e2:
                errors.append(f"STARTTLS 587 failed: {e2}")
    else:
        # Try STARTTLS on specified port
        try:
            with smtplib.SMTP(smtp_host, port, timeout=12) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, [to_email], msg.as_string())
            logger.info(f"Successfully delivered email to {to_email} via SMTP ({smtp_host}:{port}).")
            return True, f"SMTP ({smtp_host}:{port})"
        except Exception as e:
            errors.append(f"STARTTLS {port} failed: {e}")
            # Fallback to SSL 465 if host is Gmail/Yahoo
            if "gmail" in smtp_host or "yahoo" in smtp_host:
                try:
                    with smtplib.SMTP_SSL(smtp_host, 465, timeout=12) as server:
                        server.login(smtp_user, smtp_pass)
                        server.sendmail(smtp_user, [to_email], msg.as_string())
                    logger.info(f"Successfully delivered email to {to_email} via fallback SMTP_SSL ({smtp_host}:465).")
                    return True, f"SMTP_SSL ({smtp_host}:465)"
                except Exception as e2:
                    errors.append(f"Fallback SSL 465 failed: {e2}")

    return False, " | ".join(errors)


def _send_via_resend(to_email: str, subject: str, html_body: str) -> tuple[bool, str]:
    """Attempt email dispatch via Resend REST API."""
    _load_env_files()
    resend_key = os.getenv("RESEND_API_KEY", "").strip() or os.getenv("RESEND_KEY", "").strip()
    if not resend_key:
        return False, "RESEND_API_KEY not configured."

    try:
        import httpx
        from_email = os.getenv("EMAIL_FROM", "MarketMind AI <onboarding@resend.dev>")
        resp = httpx.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {resend_key}",
                "Content-Type": "application/json"
            },
            json={
                "from": from_email,
                "to": [to_email],
                "subject": subject,
                "html": html_body
            },
            timeout=10.0
        )
        if resp.status_code in [200, 201]:
            logger.info(f"Successfully sent email to {to_email} via Resend.")
            return True, "Resend API"
        else:
            return False, f"Resend HTTP {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, f"Resend exception: {e}"


def _send_via_brevo(to_email: str, subject: str, html_body: str, text_body: str) -> tuple[bool, str]:
    """Attempt email dispatch via Brevo / Sendinblue REST API."""
    _load_env_files()
    brevo_key = os.getenv("BREVO_API_KEY", "").strip() or os.getenv("SIB_API_KEY", "").strip() or os.getenv("SENDINBLUE_API_KEY", "").strip()
    if not brevo_key:
        return False, "BREVO_API_KEY not configured."

    try:
        import httpx
        sender_email = os.getenv("SMTP_USER", "").strip() or os.getenv("EMAIL_FROM_ADDRESS", "no-reply@marketmind.ai")
        sender_name = os.getenv("EMAIL_FROM_NAME", "MarketMind AI")
        resp = httpx.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "api-key": brevo_key,
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            json={
                "sender": {"name": sender_name, "email": sender_email},
                "to": [{"email": to_email}],
                "subject": subject,
                "htmlContent": html_body,
                "textContent": text_body
            },
            timeout=10.0
        )
        if resp.status_code in [200, 201, 202]:
            logger.info(f"Successfully sent email to {to_email} via Brevo API.")
            return True, "Brevo API"
        else:
            return False, f"Brevo HTTP {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, f"Brevo exception: {e}"


def _send_via_sendgrid(to_email: str, subject: str, html_body: str, text_body: str) -> tuple[bool, str]:
    """Attempt email dispatch via SendGrid REST API."""
    _load_env_files()
    sg_key = os.getenv("SENDGRID_API_KEY", "").strip()
    if not sg_key:
        return False, "SENDGRID_API_KEY not configured."

    try:
        import httpx
        from_email = os.getenv("EMAIL_FROM_ADDRESS", "no-reply@marketmind.ai")
        from_name = os.getenv("EMAIL_FROM_NAME", "MarketMind AI")
        resp = httpx.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {sg_key}",
                "Content-Type": "application/json"
            },
            json={
                "personalizations": [{"to": [{"email": to_email}]}],
                "from": {"email": from_email, "name": from_name},
                "subject": subject,
                "content": [
                    {"type": "text/plain", "value": text_body},
                    {"type": "text/html", "value": html_body}
                ]
            },
            timeout=10.0
        )
        if resp.status_code in [200, 202]:
            logger.info(f"Successfully sent email to {to_email} via SendGrid API.")
            return True, "SendGrid API"
        else:
            return False, f"SendGrid HTTP {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, f"SendGrid exception: {e}"


def _send_via_direct_mx(to_email: str, subject: str, html_body: str, text_body: str) -> tuple[bool, str]:
    """Last-ditch fallback: Direct MX delivery to recipient mail exchange server."""
    domain = to_email.split("@")[-1].strip().lower()
    mx_hosts = resolve_mx_hosts(domain)
    if not mx_hosts:
        return False, "No MX records resolved for recipient domain."

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = "MarketMind AI <no-reply@marketmind.ai>"
    msg["To"] = to_email
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    errors = []
    for host in mx_hosts:
        try:
            with smtplib.SMTP(host, 25, timeout=8) as server:
                server.ehlo("marketmind.ai")
                if server.has_extn("STARTTLS"):
                    server.starttls()
                    server.ehlo("marketmind.ai")
                server.sendmail("no-reply@marketmind.ai", [to_email], msg.as_string())
            logger.info(f"Successfully delivered email directly to {to_email} via MX server {host}.")
            return True, f"Direct MX ({host})"
        except Exception as err:
            errors.append(f"{host}: {err}")
            continue

    return False, "Direct MX failed: " + " | ".join(errors)


def dispatch_real_email_with_status(to_email: str, subject: str, html_body: str, text_body: str = "") -> dict:
    """Comprehensive multi-tiered email dispatcher returning status details."""
    to_email = to_email.strip()
    if not to_email or "@" not in to_email:
        return {
            "success": False,
            "provider": None,
            "error": "Invalid recipient email address format."
        }

    if not text_body:
        text_body = html_body

    # Attempt 1: Configured SMTP (Gmail, Outlook, Yahoo, Custom)
    ok, detail = _send_via_smtp(to_email, subject, html_body, text_body)
    if ok:
        return {"success": True, "provider": detail, "error": None}

    # Attempt 2: Resend REST API
    ok, detail = _send_via_resend(to_email, subject, html_body)
    if ok:
        return {"success": True, "provider": detail, "error": None}

    # Attempt 3: Brevo REST API
    ok, detail = _send_via_brevo(to_email, subject, html_body, text_body)
    if ok:
        return {"success": True, "provider": detail, "error": None}

    # Attempt 4: SendGrid REST API
    ok, detail = _send_via_sendgrid(to_email, subject, html_body, text_body)
    if ok:
        return {"success": True, "provider": detail, "error": None}

    # Attempt 5: Direct MX
    ok, detail = _send_via_direct_mx(to_email, subject, html_body, text_body)
    if ok:
        return {"success": True, "provider": detail, "error": None}

    return {
        "success": False,
        "provider": None,
        "error": "No email provider configured or active. Please configure SMTP credentials (e.g. Gmail App Password) or an API key (Resend/Brevo) in .env."
    }


def is_email_configured() -> tuple[bool, str]:
    """Check if any email provider is currently configured in environment."""
    _load_env_files()
    if os.getenv("SMTP_USER") and os.getenv("SMTP_PASSWORD"):
        return True, f"SMTP ({os.getenv('SMTP_USER')})"
    if os.getenv("RESEND_API_KEY") or os.getenv("RESEND_KEY"):
        return True, "Resend API"
    if os.getenv("BREVO_API_KEY") or os.getenv("SIB_API_KEY") or os.getenv("SENDINBLUE_API_KEY"):
        return True, "Brevo API"
    if os.getenv("SENDGRID_API_KEY"):
        return True, "SendGrid API"
    return False, "None"


def save_email_credentials(
    smtp_user: str = "",
    smtp_pass: str = "",
    smtp_host: str = "",
    smtp_port: str = "",
    resend_key: str = "",
    brevo_key: str = ""
) -> tuple[bool, str]:
    """Save email credentials to active runtime environment and .env configuration files."""
    updates = {}
    if smtp_user:
        updates["SMTP_USER"] = smtp_user.strip()
        os.environ["SMTP_USER"] = smtp_user.strip()
        os.environ["EMAIL_FROM"] = f"MarketMind AI <{smtp_user.strip()}>"
    if smtp_pass:
        updates["SMTP_PASSWORD"] = smtp_pass.strip()
        os.environ["SMTP_PASSWORD"] = smtp_pass.strip()
    if smtp_host:
        updates["SMTP_HOST"] = smtp_host.strip()
        os.environ["SMTP_HOST"] = smtp_host.strip()
    if smtp_port:
        updates["SMTP_PORT"] = smtp_port.strip()
        os.environ["SMTP_PORT"] = smtp_port.strip()
    if resend_key:
        updates["RESEND_API_KEY"] = resend_key.strip()
        os.environ["RESEND_API_KEY"] = resend_key.strip()
    if brevo_key:
        updates["BREVO_API_KEY"] = brevo_key.strip()
        os.environ["BREVO_API_KEY"] = brevo_key.strip()

    # Write to .env files
    current_file = Path(__file__).resolve()
    target_env_paths = [
        current_file.parent.parent.parent / ".env",
        current_file.parent.parent / ".env"
    ]

    for env_path in target_env_paths:
        try:
            existing_lines = []
            if env_path.exists():
                with open(env_path, "r", encoding="utf-8") as f:
                    existing_lines = f.readlines()

            # Process existing keys
            written_keys = set()
            new_lines = []
            for line in existing_lines:
                matched = False
                for k, v in updates.items():
                    if line.strip().startswith(f"{k}=") or line.strip().startswith(f"# {k}="):
                        new_lines.append(f"{k}={v}\n")
                        written_keys.add(k)
                        matched = True
                        break
                if not matched:
                    new_lines.append(line)

            # Append any unwritten keys
            for k, v in updates.items():
                if k not in written_keys:
                    new_lines.append(f"{k}={v}\n")

            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        except Exception as e:
            logger.warning(f"Failed to update {env_path}: {e}")

    return True, "Email credentials saved and activated successfully!"


def dispatch_real_email(to_email: str, subject: str, html_body: str, text_body: str = "") -> bool:
    """Legacy boolean wrapper around dispatch_real_email_with_status."""
    res = dispatch_real_email_with_status(to_email, subject, html_body, text_body)
    return res.get("success", False)


def send_password_reset_otp_email(to_email: str, otp: str) -> dict:
    """Send branded password reset OTP email to recipient and return dispatch status."""
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
    return dispatch_real_email_with_status(to_email, subject, html_body, text_body)
