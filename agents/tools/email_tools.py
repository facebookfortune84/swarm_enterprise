import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from crewai.tools import tool

class EmailTools:
    @tool("send_outreach_email")
    def send_email(target_email: str, subject: str, body: str) -> str:
        """
        Physically sends an email using the company SMTP server.
        Used by the Outreach Supervisor to contact leads or send 'The Box' to buyers.
        """
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")

        if not all([smtp_server, smtp_user, smtp_pass]):
            return "ERROR: SMTP credentials missing in .env"

        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = target_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            return f"SUCCESS: Outreach email sent to {target_email}"
        except Exception as e:
            return f"ERROR: Failed to send email. {str(e)}"