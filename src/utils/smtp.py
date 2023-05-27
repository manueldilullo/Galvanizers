import os
import json
import smtplib, ssl

class SMTP_util():
    def __init__(self):
        # load config file
        config_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "config.json")
        with open(config_filepath) as f:
            config = json.load(f)

        self.username = config['smtp']['username']
        self.sender = f"Galvanizers' team member <{self.username}>"
        self.server = config['smtp']['server']
        self.port = config['smtp']['port']
        self.password = config['smtp']['password']

    def send_email(self, receiver, message):
        try:
            full_message = f"""
            Subject: Your results from Galvanic Skin Response Tracker
            To: {receiver}
            From: {self.sender}
            
            {message}
            """
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.server, 465, context=context) as server:
                server.login(self.username, self.password)
                server.sendmail(self.sender, receiver, full_message)

            return True
        except Exception as e:
            print(e)
            return False