##coding=utf8

"""
EagleForce EmailBot

Import Command
--------------
    from archives.emailbot import efa_client
"""

import smtplib
from email.mime.text import MIMEText

class Config():
    """Email Account Configuration Class
    """
    def __init__(self, smtpServer, port, acc, pwd):
        self.smtpServer = smtpServer
        self.port = port
        self.acc = acc
        self.pwd = pwd
        
class EmailClient():
    """Email Client Class
    """
    def __init__(self, config):
        self.config = config
        self.server = smtplib.SMTP()
        self.server.connect(host=self.config.smtpServer, port=self.config.port)
        self.server.login(self.config.acc, self.config.pwd)
        
    def send_text(self, toAddr, subject, content):
        """Send simple pure text email to multiple recipients. No attachments, text only.
        Arguments
        ---------
            toAddr: list of recipient's email address
            subject: text
            content: text
        """
        msg = MIMEText(content)
        msg["Subject"] = subject
        msg["From"] = self.config.acc
        msg["To"] = ", ".join(toAddr)
        self.server.sendmail(self.config.acc, toAddr, msg.as_string())
    
config = Config(
            smtpServer="smtpout.secureserver.net",
            port=3535,
            acc="sanhe.hu@theeagleforce.net",
            pwd="EagleForce2014",
            )
efa_client = EmailClient(config=config)

if __name__ == "__main__":
    efa_client.send_text(["sanhe.hu@theeagleforce.net"], "Greeting", "This is a test email. For testing my email bot.")
