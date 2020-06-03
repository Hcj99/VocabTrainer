# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

#Functions that sends the mail
def send_certificate(rank, name, email):
    #Defining the mail
    message = Mail(
        #Filling mail with data
        from_email='hendrikjust@umail.ucsb.edu',
        to_emails= email,
        subject=f"VocabTrainer Certificate: {rank}",
        html_content=f"<b>Congratulations {name}!</b> <br></br> You have successfully completed the rank {rank}.")
    try:
        #Sending it out
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)