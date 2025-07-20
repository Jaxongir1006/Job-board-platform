from django.db import models
from utils.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from .manager import JobManager,JobCategoryManager

class JobCategory(TimeStampedModel):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="job_categories/")
    description = models.TextField()
    slug = AutoSlugField(populate_from="title", unique=True)

    objects = JobCategoryManager()

    class Meta:
        verbose_name = "Job Category"
        verbose_name_plural = "Job Categories"

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        return self.image.url if self.image else ""


class Job(TimeStampedModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    category = models.ForeignKey(
        JobCategory, on_delete=models.CASCADE, related_name="jobs"
    )
    contact = models.CharField(max_length=20)
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    salary = models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to="jobs/", blank=True, null=True)
    location = models.CharField(max_length=100, null=True)
    company_name = models.CharField(max_length=100, null=True)
    company_description = models.TextField(null=True)
    status = models.CharField(
        max_length=20, default="open", choices=[("open", "Open"), ("closed", "Closed")]
    )
    slug = AutoSlugField(populate_from="title", unique=True)

    objects = JobManager()

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        return self.image.url if self.image else ""

    