from email import message
import imp
from sys import exc_info
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from log import Log

class SendMail():
    def __init__(self) -> None:
        self.log = Log()

    def send_mail(self, smtp_params, content):
        if(content == None):
            self.log.info("No errors to sent to E-Mail")
            return None

        mail_sender = smtp_params["mail_sender"]
        mail_receivers = smtp_params["mail_receiver"]
        mail_server = smtp_params["mail_server"]
        mail_port = smtp_params["mail_port"]
        server_error = smtp_params["server_error"]

        text = f"""\
            There was a problem with archiving logs on the server: {server_error}
            Check the problem !
            
            {content}
            
            ----------------
            Powered by Majster
            """
        html = f"""\
            <div style="font-wehigh: bold; font-size: 20; font-famili: Comic Sans MS;">
                There was a problem with archiving logs on the server: {server_error}
                <div style="color: red;">
                    Check the problem !
                </div>
            </div>
            <br /><br />
            
            {content}
            
            <br />
            ----------------
            <br />
            Powered by <a href="mailto://rachuna.mikolaj@gmail.com" style="color: red; text-decoration: none; font-weight: bold">Majster</a>
            """

        message = MIMEMultipart("alternative")
        message["Subject"] = "!!! ERROR in archives logs !!!"
        message["From"] = mail_sender

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        try:
            server = SMTP(mail_server, mail_port)
            server.ehlo_or_helo_if_needed()
            print(server.ehlo())

            for mail_reciver in mail_receivers:
                message["To"] = mail_reciver
                server.sendmail(mail_sender, mail_reciver, message.as_string())
                mail_reciver = None

            server.close()
            self.log.info("Email sending with erros completed.")

        except:
            print(exc_info()[:-1])
            self.log.error(exc_info()[:-1])

    def __del__(self) -> None:
        del self.log