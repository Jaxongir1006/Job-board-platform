from django.contrib import admin
from .models import Job, JobCategory
from django.utils.html import format_html

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />'.format(obj.image.url))

    image_preview.short_description = 'Image Preview'
    list_display = ["title", 'id', 'image_preview']
    list_filter = ["title"]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "id"]
    list_filter = ["category", "status"]
