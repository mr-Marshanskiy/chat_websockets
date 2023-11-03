from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken


User = get_user_model()


def get_user_by_jwt(token):
    try:
        token = AccessToken(token)
        user = User.objects.get(id=token['user_id'])
        return user
    except Exception as e:
        return None
