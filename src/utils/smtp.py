import os
import json
import smtplib, ssl
from email.mime.text import MIMEText

class SMTP_util():
    def __init__(self):
        # load config file
        config_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config.json")
        with open(config_filepath) as f:
            config = json.load(f)

        self.username = config['smtp']['username']
        self.password = config['smtp']['password']
        self.sender = config['smtp']['sender']
        self.server = config['smtp']['server']
        self.port = config['smtp']['port']

    def send_email(self, receiver, message):
        try:
            msg = MIMEText(message)
            msg['Subject'] = "Your results from Galvanic Skin Response Tracker"
            msg['From'] = self.sender
            msg['To'] = receiver
            print(msg)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.server, 465, context=context) as server:
                server.login(self.username, self.password)
                server.sendmail(self.sender, receiver, msg.as_string())

            return True
        except Exception as e:
            print(e)
            return False