import json
import logging
import os
import time
import datetime
import uuid

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

from email import encoders


# import Image


import boto3
from lambda_decorators import cors_headers

from Lambda.utils import send

dynamodb = boto3.resource('dynamodb')

@cors_headers
def create(event, context):
    data = json.loads(event['body'])
    response = {}
    print(data)
    if (data.get("name")==None or data.get("profile")==None):
        print("error")
        response = {
            "statusCode": 404,
            "body": json.dumps({})
        }
    else:
        print("start")
        timestamp = str(datetime.datetime.now())

        table = dynamodb.Table(os.environ['GOLDENMORN_PROFILE_TABLE'])
        email_user = os.environ['EMAIL_USER']
        email_password = os.environ['EMAIL_PASSWORD']

        profile = data["profile"]
        recipe_card = ""
        if (profile=="Mixed nuts"):
            recipe_card = "https://bit.ly/2BFLya7"
        elif(profile=="Fruits"):
          recipe_card = "https://bit.ly/2NagYKi"
        elif(profile=="Fruits and mixed nuts"):
          recipe_card = "https://bit.ly/2X86uiY"
        elif(profile=="Just add milk/Pure and simple"):
          recipe_card = "https://bit.ly/2EcRjxM"
        else:
          recipe_card = "there is no link"
        


        item = {
            'profile_id': str(uuid.uuid1()),
            'name': data['name'],
            # 'phone number': data['mobile'],
            # 'Email Address': data['email'],
            'createdAt': timestamp,
            'updatedAt': timestamp,
            'profile': profile,
            'question1': data['question1'],
            'question2': data['question2'],
            'question3': data['question3'],
            'question4': data['question4'],
            'question5': data['question5']
        }
        print("saving ............")
        # write the todo to the database
        table.put_item(Item=item)

        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(item)
        }
        # print("done saving.......")
        # print("sending SMS to user.......")
        # message = "Hello {0}. You deserve this yummy and nutritious recipe for a cereal that is truly Golden. Get it here {1}".format(data["name"],recipe_card)
        # send(data['mobile'],message)
        # print("done sending sms.....")
        # body = """<html><body>
        #                 Hello {0},<br /><br />
        #                 We’re delighted to present to you this yummy and nutritious recipe for a cereal that`s truly Golden. You’ve earned it.<br /><br />
        #                 <a href="{1}">Download</a> and enjoy!<br /> <br />
        #                 Remember to start your day with the right breakfast.<br />
        #                 Love, Golden Morn.
        #         </body></html>""".format(data['name'],recipe_card)
        # message_dict = { 'Data':
        #                   'From: ' + mail_sender + '\n'
        #                   'To: ' + mail_receivers_list + '\n'
        #                   'Subject: ' + mail_subject + '\n'
        #                   'MIME-Version: 1.0\n'
        #                   'Content-Type: text/html;\n\n' +
        #                   mail_content
        #                 }
        # msg = MIMEMultipart()
        # msg['From'] = 'dayo.akinbami@spongegroup.com.ng'
        # msg['To'] = data['email']
        # msg['Subject'] = 'Golden Morn'

        # msg.attach(MIMEText(body,'plain'))
        # text = msg.as_string()

        # filename = 'sponge.txt'
        # print(os.getcwd())
        # attachment = open("Golden-Morn-Nanaberry-Recipe.jpg", 'r')
        # part = MIMEBase('application', 'octet-stream')
        # part.set_payload((attachment).read())
        # encoders.encode_base64(part)
        # part.add_header('Content-Disposition', 'attachment; filename='+ filename)

        # msg.attach(part)

        # server = smtplib.SMTP('email-smtp.us-west-2.amazonaws.com',465)
        # server.starttls()
        # server.login(email_user, email_password)
        # server.sendMail('dayo.akinbami@spongegroup.com.ng', data['email'], text)
        # server.quit()


        # sendEmail(data['email'],body,body,"Golden Morn")
        # print("done sending email.....")

    # if 'name' not in data or 'phone' not in data:
    #     logging.error("Validation Failed")
    #     raise Exception("Couldn't create the phoenix profile item.")
    #     return

    
    return response

def sendEmail(send_to,email_body_html,email_body_text,subject):
    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name='us-west-2')

    # Try to send the email.
    
    
    response = client.send_email(
        Destination={
            'ToAddresses': [
                send_to,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': email_body_html,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': email_body_text,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': subject,
            },
        },
        Source='goldenmorncereal@gmail.com',
        # If you are not using a configuration set, comment or delete the
        # following line
        # ConfigurationSetName=CONFIGURATION_SET,
    )
    print("Email sent! Message ID:"),
    print(response)
