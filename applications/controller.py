from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from .models import JobApplication
from .schemas import JobApplicationSchema,CreateJobApplicationSchema
from ninja_jwt.authentication import JWTAuth
from utils.permissions import IsAuthenticatedAndNotDeleted
from typing import List
from ninja.errors import HttpError
from jobs.models import Job

@api_controller("", auth=JWTAuth(), permissions=[IsAuthenticatedAndNotDeleted])
class JobApplicationController:
    @http_get("job-applications/{job_slug}/", response=List[JobApplicationSchema])
    def list(self, job_slug: str, request):

        user = request.user

        job = Job.objects.filter(slug=job_slug).first()
        if not job:
            return HttpError(400, "Job not found")
        
        job_applications = JobApplication.objects.filter(job=job, user=user)
        
        return job_applications
    
    @http_post("job-applications/{job_slug}/", response=JobApplicationSchema)
    def create(self, request, job_slug: str, data: CreateJobApplicationSchema):
        job = Job.objects.filter(slug=job_slug).first()
        if not job:
            return HttpError(400, "Job not found")
        job_application = JobApplication.objects.create(job=job, user=request.user, **data.model_dump())
        return job_application