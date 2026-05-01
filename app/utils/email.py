import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_settings

settings = get_settings()


async def send_contact_email(name: str, email: str, subject: str, message: str) -> bool:
    if not settings.SMTP_USER or not settings.CONTACT_RECEIVER_EMAIL:
        # SMTP not configured — skip silently (still save to DB)
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[Portfolio Contact] {subject}"
        msg["From"]    = settings.SMTP_USER
        msg["To"]      = settings.CONTACT_RECEIVER_EMAIL
        msg["Reply-To"] = email

        html_body = f"""
        <html><body style="font-family:sans-serif;color:#1e293b;max-width:600px;margin:auto">
          <div style="border-top:3px solid #c9a96e;padding:32px 0">
            <h2 style="margin:0 0 4px;font-size:22px">New Contact Message</h2>
            <p style="color:#64748b;margin:0 0 24px;font-size:13px">Via Portfolio Website</p>
            <table style="width:100%;border-collapse:collapse;font-size:14px">
              <tr>
                <td style="padding:10px 0;color:#64748b;width:90px">Name</td>
                <td style="padding:10px 0;font-weight:600">{name}</td>
              </tr>
              <tr>
                <td style="padding:10px 0;color:#64748b">Email</td>
                <td style="padding:10px 0"><a href="mailto:{email}" style="color:#c9a96e">{email}</a></td>
              </tr>
              <tr>
                <td style="padding:10px 0;color:#64748b">Subject</td>
                <td style="padding:10px 0">{subject}</td>
              </tr>
            </table>
            <div style="background:#f8f7f4;border-left:3px solid #c9a96e;padding:16px 20px;margin-top:20px;border-radius:0 6px 6px 0">
              <p style="margin:0;line-height:1.7;white-space:pre-wrap">{message}</p>
            </div>
          </div>
        </body></html>
        """

        msg.attach(MIMEText(html_body, "html"))

        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        return True

    except Exception as e:
        print(f"[Email Error] {e}")
        return False
