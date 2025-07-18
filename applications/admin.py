from django.contrib import admin
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ["user", "job", "status"]
    list_filter = ["status"]

    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"