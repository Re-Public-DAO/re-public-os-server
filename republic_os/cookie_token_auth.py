from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from republic_os.devices.models import Device


# We're using this because we can't use the default SessionAuthentication
# and we need the token here to be an HttpOnly cookie
class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # print('CookieTokenAuthentication')
        token_key = request.COOKIES.get('auth_token')

        qr_code_key = request.GET.get('qr_code_key')

        if qr_code_key:
            device = Device.objects.filter(qr_code_key=qr_code_key).first()
            if not device:
                return None

            return device.user, device.user.auth_token

        # print(f'token_key: {token_key}')

        if not token_key:
            print('No token key')
            return None

        token = Token.objects.filter(key=token_key).first()

        if token and token.user.is_active:
            return token.user, token

        return None
