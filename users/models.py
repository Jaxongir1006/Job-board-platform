from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from utils.models import TimeStampedModel
from .manager import CustomUserManager
from django.utils.timezone import now


class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    class UserTypeEnum(models.TextChoices):
        JOB_SEEKER = "job_seeker"
        COMPANY = "company"
        ADMIN = "admin"

    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=11, choices=UserTypeEnum.choices, default=UserTypeEnum.JOB_SEEKER
    )
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username
    
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = now() 
        self.save()


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    cv = models.FileField(upload_to="cv/", null=True, blank=True)

    def __str__(self):
        return self.user.phone_number

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def imageURL(self):
        return self.profile_picture.url if self.profile_picture else ""
