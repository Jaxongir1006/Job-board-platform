from django.db import models
from utils.models import TimeStampedModel
from .manager import ApplicationManager

class JobApplication(TimeStampedModel):
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
    )

    objects = ApplicationManager()

    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"

    @property
    def resume_url(self):
        return self.resume.url if self.resume else None