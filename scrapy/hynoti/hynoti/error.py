import smtplib
from email.mime.text import MIMEText

def send_email(msg):
    email_address = 'rkdejrdud88@naver.com'
    email_password = 'duckyoung88!'

    server = smtplib.SMTP_SSL('smtp.naver.com', 465)
    server.login(email_address, email_password)
    
    email = MIMEText("PANIC: unexpected error at '{}'".format(msg))
    email['Subject'] = 'HYnoti'
    email['From'] = email_address
    email['To'] = email_address
    server.sendmail(email_address, email_address, email.as_string())
    server.quit()