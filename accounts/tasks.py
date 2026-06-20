from celery import shared_task
from utils import send_otp_code as _send_otp_code, send_reset_link_sms
from accounts.models import OtpCode
from datetime import timedelta
from django.utils import timezone

@shared_task
def send_otp_code(phone_number, code):
    _send_otp_code(phone_number, code)

@shared_task
def remove_expired_otp_codes():
    expired_time = timezone.now() - timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=expired_time).delete()


@shared_task
def send_reset_link_sms_task(phone_number, link):
    send_reset_link_sms(phone_number, link)