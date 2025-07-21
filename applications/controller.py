from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from .models import JobApplication
from .schemas import JobApplicationSchema,CreateJobApplicationSchema
from ninja_jwt.authentication import JWTAuth
from utils.permissions import IsAuthenticatedAndNotDeleted
from typing import List
from ninja.errors import HttpError
from jobs.models import Job
from django.shortcuts import get_object_or_404
from .tasks import send_application_email_to_company, send_result_to_seeker
import logging


logger = logging.getLogger("__name__")

@api_controller("", auth=JWTAuth(), permissions=[IsAuthenticatedAndNotDeleted])
class JobApplicationController:
    @http_get("job-applications/{job_slug}/", response=List[JobApplicationSchema])
    def list(self, job_slug: str, request):
        """
        List all job applications for a specific job.
        This endpoint retrieves all applications for a job identified by its slug.
        """
        user = request.user

        job = Job.objects.filter(slug=job_slug).first()
        if not job:
            return HttpError(400, "Job not found")
        
        job_applications = JobApplication.objects.filter(job=job, user=user)
        
        return job_applications
    
    @http_post("applications/{job_slug}/", response=JobApplicationSchema)
    def create(self, request, job_slug: str, data: CreateJobApplicationSchema):
        job = Job.objects.filter(slug=job_slug).first()
        if not job:
            return HttpError(400, "Job not found")
        job_application = JobApplication.objects.create(job=job, user=request.user, **data.model_dump())
        # Email yuborish
        logger.info(f"Job application created for job {job.title} by user {request.user.username}.")
        send_application_email_to_company.delay(job.user.email, job.title, job_application.user.username, job_application.id, job_application.resume.url)
        return job_application
    
@api_controller("", tags=["Job Application Management"])
class JobApplicationDetailController:
    @http_get("applications/{application_id}/accept/", response=dict)
    def accept_application(self, request, application_id: int): 
        app = get_object_or_404(JobApplication, id=application_id)
        if app.status != 'pending':
            return {"message": "Ariza allaqachon qabul qilingan yoki rad etilgan."}
        app.status = 'accepted'
        app.save()
        logger.info(f"Application {app.id} accepted for job {app.job.title} by user {request.user.username}.")
        
        # Job seekerni email orqali ogohlantirish
        send_result_to_seeker.delay(app.user.email, app.job.title, "QABUL QILINDI", app.job.contact)

        return {"message": "Ariza qabul qilindi."}  


    @http_get("applications/{application_id}/reject/", response=dict)
    def reject_application(self,request, application_id: int):
        app = get_object_or_404(JobApplication, id=application_id)
        if app.status != 'pending':
            return {"message": "Ariza allaqachon qabul qilingan yoki rad etilgan."}
        app.status = 'rejected'
        app.save()
        logger.info(f"Application {app.id} rejected for job {app.job.title} by user {request.user.username}.")  

        send_result_to_seeker.delay(app.user.email, app.job.title, "RAD ETILDI", app.job.contact)

        return {"message": "Ariza rad etildi."}
