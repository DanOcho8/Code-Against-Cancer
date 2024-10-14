import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
def send_sms_notification(to_phone, text_message):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']

    client = Client(account_sid, auth_token)


    try:
        message = client.messages.create(
        to = to_phone,
        from_= os.environ['MY_TWILIO_NUMBER'],
        body = text_message
)
        return{'status': 'success', 'message_sid': message.sid}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}