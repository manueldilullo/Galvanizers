import smtplib

class SMTP_util():
    def __init__(self):
        print('Initialized')
    
    def send_email(self, to_address):
        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        #     server.login(email, password)
        #     server.sendmail(email, email, message)
        return True