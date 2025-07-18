from .models import CustomUser
from django.contrib.auth.backends import BaseBackend


class CustomUserBackend(BaseBackend):
    def authenticate(self, request, login_input, password=None, **kwargs):
        """
        Foydalanuvchini email, username yoki telefon raqam orqali topish
        """
        user = None
        try:
            user = CustomUser.objects.get(email=login_input) or \
            CustomUser.objects.get(username=login_input) or \
            CustomUser.objects.get(phone_number=login_input)
        except CustomUser.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None