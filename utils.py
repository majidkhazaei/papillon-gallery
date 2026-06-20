from kavenegar import KavenegarAPI
from django.contrib.auth.mixins import UserPassesTestMixin
from decouple import config


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI (config('apikey'))
        params = {'sender': '2000660110', 'receptor': phone_number, 'message': f'your code: {code}'}
        response = api.sms_send(params)
        print(response)
    except Exception as e:
        print(e)


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin

def send_reset_link_sms(phone_number, link):
    try:
        api = KavenegarAPI (config('apikey'))
        message = f'لینک بازیابی رمز عبور شما:\n{link}'
        params = {
            'sender': '2000660110',
            'receptor': phone_number,
            'message': message
        }
        response = api.sms_send(params)
        print(response)
    except Exception as e:
        print(e)