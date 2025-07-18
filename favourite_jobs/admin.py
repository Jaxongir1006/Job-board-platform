from django.contrib import admin
from .models import FavouriteJob


@admin.register(FavouriteJob)
class FavouriteJobAdmin(admin.ModelAdmin):
    list_display = ["job", "user"]
