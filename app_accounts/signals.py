import threading

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from Config.settings import EMAIL_HOST_USER
from app_accounts.models import UserModel, VerificationModel
from app_accounts.utils import get_random_verification_code


def send_verification_email(email):
    try:
        code = get_random_verification_code(email=email)
        VerificationModel.objects.create(code=code, user=UserModel.objects.get(email=email))
        send_mail(
            subject="Email Verification",
            message=f"Please verify your email address by clicking the link below:{code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
    except Exception as e:
        print(f"Failed to send verification email to {email}: {str(e)}")


@receiver(post_save, sender=UserModel)
def send_verification_email_after_signup(sender, instance=None, created=False, **kwargs):
    if created:
        email_thread = threading.Thread(target=send_verification_email, args=(instance.email,))
        email_thread.start()
