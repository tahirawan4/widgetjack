from django.contrib.auth.backends import ModelBackend
from widgets.models import User


class AuthBackend(ModelBackend):
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None, **kwargs):
        return (User.objects.filter(username__iexact=username) | User.objects.filter(email__iexact=username)).first()
