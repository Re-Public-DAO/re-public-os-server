from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


# We're using this because we can't use the default SessionAuthentication
# and we need the token here to be an HttpOnly cookie
class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token_key = request.COOKIES.get('auth_token')

        if not token_key:
            return None

        token = Token.objects.filter(key=token_key).first()

        if token and token.user.is_active:
            return token.user, token

        return None
