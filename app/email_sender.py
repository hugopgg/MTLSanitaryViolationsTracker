# ============================================
# Auteur: Hugo Perreault Gravel 
# ============================================

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml

# ================
# Email Sending
# ================


class EmailSender:
    def __init__(self, config_file):
        self.config = self.load_email_config(config_file)

    def load_email_config(self, config_file):
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
        return config

    def send_email(self, subject, message):
        try:
            server = smtplib.SMTP(
                self.config["smtp_server"], self.config["smtp_port"]
            )
            server.ehlo()

            # Uncomment for real life context
            # (source: https://realpython.com/python-send-email/)
            # context = ssl.create_default_context()
            # server.starttls(context=context)
            # server.login(self.config["smtp_username"],
            #              self.config["smtp_password"])

            msg = f"Subject: {subject}\n\n{message}"

            server.sendmail(
                self.config["sender_email"],
                self.config["receiver_email"],
                msg.encode("utf-8"),
            )
            server.quit()
            print("Email successfully sent")
        except Exception as e:
            print(f"Error sending email: {e}")
