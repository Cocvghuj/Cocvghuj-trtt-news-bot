import smtplib, traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

def send_transactional_email(subject, html_body):
    """
    Delivers responsive HTML emails with deliverability optimizations.
    """
    if not config.GMAIL_EMAIL or not config.GMAIL_APP_PASSWORD or not config.CUSTOMER_EMAILS:
        print("[EMAIL] Credentials missing. Skipping delivery.")
        return False

    recipients = [e.strip() for e in config.CUSTOMER_EMAILS.split(",") if e.strip()]
    if not recipients:
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"TRTT Travel Intelligence <{config.GMAIL_EMAIL}>"
        
        # Plain text fallback for spam score improvement
        text_fallback = "Please enable HTML viewing to access TRTT Travel Intelligence."
        msg.attach(MIMEText(text_fallback, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(config.GMAIL_EMAIL, config.GMAIL_APP_PASSWORD)
            for recipient in recipients:
                msg["To"] = recipient
                server.sendmail(config.GMAIL_EMAIL, recipient, msg.as_string())

        print(f"[EMAIL] Successfully dispatched to {len(recipients)} subscribers.")
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        traceback.print_exc()
        return False
