from django.contrib.auth.models import BaseUserManager
from phonenumber_field.validators import validate_international_phonenumber
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError("The username field must be set")
        if not email:
            raise ValueError("The email field must be set")
        if not phone_number:
            raise ValueError("The phone number field must be set")

        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, phone_number=phone_number, **extra_fields
        )
        if password is None:
            raise ValueError("The password field must be set")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if password == username:
            raise ValueError("Password cannot be the same as username")
        if password.isnumeric():
            raise ValueError("Password cannot be numeric")
        if password.isalpha():
            raise ValueError("Password cannot be alphabetical")
        try:
            validate_international_phonenumber(phone_number)
        except ValidationError:
            raise ValidationError("Telefon raqam notogri formatda. Masalan: +998901234567")
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, username, email, phone_number, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, phone_number, password, **extra_fields)
