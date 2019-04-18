import os
import boto3
from botocore.exceptions import ClientError

SES_CLIENT = boto3.client(
    'ses',
    aws_access_key_id=os.environ['AWS_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET'],
    region_name=os.environ['AWS_REGION_NAME']
)
EMAIL_SENDER = os.environ['EMAIL_SENDER']
EMAIL_CHARSET = os.environ.get('EMAIL_CHARSET', "UTF-8")

def vp_auto_success():
    to_email = EMAIL_SENDER
    subject = "VP Auto Run: Success"
    text = "The Virgin Pulse Automation script ran successfully"
    html = text
    send_ses_email(to_email, subject, text, html)

def vp_auto_failure(message_plaintext, message_html):
    to_email = EMAIL_SENDER
    subject = "VP Auto Run: Failure"
    text = "The Virgin Pulse Automation script failed to run to completion.\nError Message:\n{}".format(message_plaintext)
    html = "<p>The Virgin Pulse Automation script failed to run to completion.</p><p>Error Message:</p>{}".format(message_html)
    send_ses_email(to_email, subject, text, html)

def send_ses_email(email, subject, text, html):
    try:
        response = SES_CLIENT.send_email(
            Destination={
                'ToAddresses' : [email]
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': EMAIL_CHARSET,
                        'Data': html
                    },
                    'Text': {
                        'Charset': EMAIL_CHARSET,
                        'Data': text
                    }
                },
                'Subject': {
                    'Charset': EMAIL_CHARSET,
                    'Data': subject
                }
            },
            Source=EMAIL_SENDER
        )
    except ClientError as error:
        print('Email failed to send')
        print(error.response['Error'])
        raise error

    print('Email sent! Message ID: {}'.format(response['MessageId']))
    return True
