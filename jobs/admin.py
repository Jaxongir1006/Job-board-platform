from django.contrib import admin
from .models import Job, JobCategory


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ["title", 'id']
    list_filter = ["title"]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "id"]
    list_filter = ["category", "status"]
