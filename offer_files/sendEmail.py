# Import the email modules we'll need
from email.message import EmailMessage
import smtplib
import logging


def sendEmail(txt, emailAddr, psf):
    gmail_user = 'ofer12@gmail.com'
    gmail_password: str = psf

    sent_from = gmail_user

    to = [emailAddr]

    print(sent_from, to)
    subject = 'Recovery Message'
    body = txt
    print(body)
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        print('hello')
        server.login(gmail_user, gmail_password)
        print('login')
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except Exception as e:
        logging.error('Failed to send email : ' + str(e))

        print('Something went wrong...')


if __name__ == "__main__":
    print("sending")
    psf = input("enter Password")
    sendEmail('12345', 'ofer12@gmail.com', psf)