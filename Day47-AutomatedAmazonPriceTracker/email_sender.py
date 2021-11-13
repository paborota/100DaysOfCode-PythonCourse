from smtplib import SMTP

SMTP_SERVER = ""    # @TODO
EMAIL = ""          # @TODO
PASSWORD = ""       # @TODO


class EmailSender:

    def send_email_to_self(self, msg):

        self.send_email(to=EMAIL, msg=msg)

    def send_email(self, to, msg):

        with SMTP(host=SMTP_SERVER) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=to,
                msg=msg
            )
