from django.contrib import admin
from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "user_type", 'id']
    list_filter = ["user_type"]
    

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user__username', 'user__user_type', 'user__id']
    list_filter = ["user__user_type"]