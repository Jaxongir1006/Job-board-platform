from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["job", "user", "rating", "created_at"]
    list_filter = ["job", "user", "rating"]
    search_fields = ["job__title", "user__username"]
    ordering = ["-created_at"]

    def has_add_permission(self, request):
        return False
    