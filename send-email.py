import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(from_email="rce.uwa@gmail.com",
               to_emails='tomr06072001@gmail.com',
               subject='Password Reset Confirmation',
               plain_text_content='This is my second sendgrid email',
               html_content='<h1>Password Reset</h1><p> Please click <a href="www.youtube.com.au">here</a> to reset your password</p><i> Please Note: This link will only stay valid for 24 hours.</i>')

try:
    sg = SendGridAPIClient('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')
    # sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)