from ninja_extra import api_controller, http_post, http_get,http_delete
from favourite_jobs.models import FavouriteJob
from utils.permissions import IsAuthenticatedAndNotDeleted
from ninja_jwt.authentication import JWTAuth
from ninja.errors import HttpError
from .schemas import FavouriteJobSchema
from typing import List
from jobs.models import Job


@api_controller(tags=["Favourite Jobs"], auth=JWTAuth(), permissions=[IsAuthenticatedAndNotDeleted])
class FavouriteJobsController:
    @http_post("favourite-jobs/{job_slug}/", response=FavouriteJobSchema)
    def favourite_job(self, request, job_slug: str):
        user = request.user

        try:
            job = Job.objects.get(slug=job_slug)
        except Job.DoesNotExist:
            raise HttpError(404, "Job not found")

        if FavouriteJob.objects.filter(job=job, user=user).exists():
            raise HttpError(400, "Job already favourited")

        favourite = FavouriteJob.objects.create(job=job, user=user)
        return favourite

    @http_get("favourite-jobs/", response=List[FavouriteJobSchema])
    def get_favourite_jobs(self, request):
        user = request.user
        return FavouriteJob.objects.select_related('job').filter(user=user)
    

    @http_delete("favourite-jobs/{job_slug}/", response=dict)
    def unfavourite_job(self, request, job_slug: str):
        user = request.user

        try:
            job = Job.objects.get(slug=job_slug)
        except Job.DoesNotExist:
            raise HttpError(404, "Job not found")

        if not FavouriteJob.objects.filter(job=job, user=user).exists():
            raise HttpError(400, "Job not favourited")

        FavouriteJob.objects.filter(job=job, user=user).delete()
        return {"message": "Job unfavourited successfully"}