from django.db import models


class FavouriteJob(models.Model):
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('job', 'user')