import datetime

import pytz
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.request import Request

from users.models import Token


class TokenAuthentication(BaseAuthentication):
    bearer_field = 'Bearer'

    def authenticate(self, request: Request):
        token = get_authorization_header(request)
        code = token.decode('utf-8').replace(f'{self.bearer_field} ', '')
        try:
            token = Token.objects.get(code=code)
        except Token.DoesNotExist:
            return None
        utc = pytz.UTC
        if token.expiration_time.replace(tzinfo=utc) < datetime.datetime.now(tz=utc):
            token.delete()
            return None
        return token.user, token
