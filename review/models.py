from django.db import models
from utils.models import TimeStampedModel
from django.db.models import Avg


class Review(TimeStampedModel):
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='User'
    )
    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Job'
    )
    rating = models.PositiveIntegerField(
        verbose_name='Rating',
        help_text='Rating out of 5'
    )
    comment = models.TextField(
        verbose_name='Comment',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ('user', 'job')

    def __str__(self):
        return f'Review by {self.user.username} for {self.job.title}'
