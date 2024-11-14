import random

from app_accounts.models import VerificationModel
from twilio.rest import Client
from django.conf import settings

def get_random_verification_code(email):
    code = random.randint(1000, 9999)
    while VerificationModel.objects.filter(user__email=email, code=code).exists():
        code = random.randint(1000, 9999)
    return code


from twilio.rest import Client
from django.conf import settings


def sms_sender(to_number, message_body):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    messaging_service_sid = settings.TWILIO_MESSAGING_SERVICE_SID

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            messaging_service_sid=messaging_service_sid,
            body=message_body,
            to=to_number
        )
        print(f"SMS sent successfully: {message.sid}")
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False

