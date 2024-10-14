import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def reminder_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        consent = request.POST.get('consent')

        if consent:
            # Ensure phone number starts with '+'
            if not phone_number.startswith('+'):
                phone_number = '+' + phone_number

            try:
                # Set the message text
                message_text = 'This is a reminder from CodeAgainstCancer.'

                # Call the updated function with phone number and message
                response = send_sms_notification(phone_number, message_text)

                if response['status'] == 'success':
                    messages.success(request, f"Reminder sent successfully! Message SID: {response['message_sid']}")
                else:
                    messages.error(request, f"Failed to send reminder: {response['message']}")

            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

            return redirect('reminder')

    return render(request, 'reminder.html')


def send_sms_notification(to_phone, text_message):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    from_phone= os.environ['MY_TWILIO_NUMBER']

    client = Client(account_sid, auth_token)


    try:
        message = client.messages.create(
        to = os.environ['MY_PHONE_NUMBER'],
        from_= os.environ['MY_TWILIO_NUMBER'],
        body = 'This is a text message from django project'
        #body = "This is a text message from django project"
        )
        return{'status': 'success', 'message_sid': message.sid}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

