import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from crewai.tools import tool

class EmailTools:
    @tool("send_outreach_email")
    def send_email(target_email: str, subject: str, body: str) -> str:
        """Physically sends an email via SMTP for sales and delivery."""
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
            return f"SUCCESS: Email delivered to {target_email}"
        except Exception as e:
            return f"ERROR: Delivery failed. {str(e)}"

# Export for the agents
comm_tools = EmailTools()
send_outreach_email = comm_tools.send_email