from kavenegar import KavenegarAPI
from django.contrib.auth.mixins import UserPassesTestMixin
from decouple import config


def send_otp_code(phone_number, code):
    try:
        api = config('KavenegarAPI')
        params = {'sender': '2000660110', 'receptor': phone_number, 'message': f'your code: {code}'}
        response = api.sms_send(params)
        print(response)
    except Exception as e:
        print(e)


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin