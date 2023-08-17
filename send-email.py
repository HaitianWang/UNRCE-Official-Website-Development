import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(from_email="rce.uwa@gmail.com",
               to_emails='ryantakeda1@gmail.com',
               subject='First Test',
               plain_text_content='This is my first sendgrid email, hopefully this works',
               html_content='<strong>Testing html_content</strong>')

try:
    # sg = SendGridAPIClient('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')
    sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)