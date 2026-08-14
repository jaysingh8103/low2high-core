import os
import smtplib
from email.message import EmailMessage
import mimetypes

class AutoMailer:
    def __init__(self):
        self.server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.port = int(os.getenv("SMTP_PORT", 587))
        self.username = os.getenv("SMTP_USERNAME")
        self.password = os.getenv("SMTP_PASSWORD")

    def send_audit_email(self, recipient_email: str, subject: str, body_text: str, html_content: str = None, pdf_path: str = None) -> bool:
        if not self.username or not self.password or self.username == "your_email@gmail.com":
            print(f"[AutoMailer] SMTP Credentials not configured. Skipped sending email to {recipient_email}")
            return False

        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = recipient_email
            
            # Set the body of the email (plain text)
            msg.set_content(body_text)
            
            # Add HTML alternative if provided
            if html_content:
                msg.add_alternative(html_content, subtype='html')

            # Attach PDF if provided
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    pdf_data = f.read()
                    
                msg.add_attachment(
                    pdf_data, 
                    maintype='application', 
                    subtype='pdf', 
                    filename=os.path.basename(pdf_path)
                )

            # Connect to SMTP server and send
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                
            print(f"[AutoMailer] Successfully sent audit report to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"[AutoMailer] Failed to send email to {recipient_email}: {e}")
            return False
