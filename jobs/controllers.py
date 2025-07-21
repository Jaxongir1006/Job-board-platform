from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from .models import Job, JobCategory
from .schemas import JobSchema, JobCategorySchema, CreateJobSchema, UpdateJobSchema, JobSearchSchema
from ninja_jwt.authentication import JWTAuth
from utils.permissions import IsAuthenticatedAndNotDeleted
from typing import List
from ninja.errors import HttpError
from .documents import JobDocument
import logging

logger = logging.getLogger("__name__")

@api_controller(
    "", tags=["Jobs"], auth=JWTAuth(), permissions=[IsAuthenticatedAndNotDeleted]
)
class JobsController:
    @http_get("categories/", response=List[JobCategorySchema])
    def get_categories(self):
        """
        Get all job categories.
        This endpoint retrieves all available job categories.
        """
        return JobCategory.objects.all()

    @http_get("jobs/{category_slug}/", response=List[JobSchema])
    def get_jobs(self, category_slug: str):
        """
        Get all jobs in a specific category.
        This endpoint retrieves all jobs that belong to the specified category.
        """
        return Job.objects.filter(category__slug=category_slug, status="open")

    @http_get("job/{job_slug}/", response=JobSchema)
    def get_job(self, job_slug: str):
        """
        Get a specific job by its slug.
        This endpoint retrieves a job based on its unique slug identifier.    
        """
        try:
            job = Job.objects.get(slug=job_slug)
            print(JobSchema.from_orm(job).dict())
        except Job.DoesNotExist:
            raise HttpError(404, "Job not found")
        return job

    @http_post("create-job/", response=dict)
    def create_job(self, request, data: CreateJobSchema):
        """
        Create a new job.
        This endpoint allows authenticated users to create a new job listing.
        """
        user = request.user
        data = data.model_dump()
        category = JobCategory.objects.filter(slug=data["category"]).first()
        if not category:
            return {"message": "Job category not found"}
        data["category"] = category
        job = Job.objects.create(**data, user=user)
        logger.info(f"Job {job.title} created by {user.username}.")
        return {
            "message": "Job created successfully",
            "slug": job.slug,
            "category": job.category.title,
            "title": job.title,
        }

    @http_put("update-job/{job_slug}/", response=JobSchema)
    def update_job(self, job_slug: str, request, data: UpdateJobSchema):
        user = request.user
        data = data.model_dump(exclude_unset=True)
        job = Job.objects.filter(slug=job_slug, user=user).first()
        if not job:
            return HttpError(400, "Job not found")
        for field, value in data.items():
            setattr(job, field, value)
        job.save()
        logger.info(f"Job {job.title} updated by {user.username}.")
        return JobSchema.from_orm(job)


    @http_delete("delete-job/{job_slug}/", response=dict)
    def disactivate_job(self, job_slug: str, request):
        user = request.user
        job = Job.objects.filter(slug=job_slug, user=user).first()
        if not job:
            return {"message": "Job not found"}
        job.status = 'closed'
        job.save()
        logger.info(f"Job {job.title} deactivated by {user.username}.")
        return {"message": "Job deleted successfully"}
    

    @http_put('reactivate-job/{job_slug}/', response=dict)
    def reactivate_job(self, job_slug: str, request):
        user = request.user
        job = Job.objects.filter(slug=job_slug, user=user).first()
        if not job:
            return {"message": "Job not found"}
        job.status = 'open'
        job.save()
        logger.info(f"Job {job.title} reactivated by {user.username}.")
        return {"message": "Job reactivated successfully"}
    

@api_controller("search/", tags=["Search"], auth=JWTAuth(), permissions=[IsAuthenticatedAndNotDeleted])
class SearchController:
    @http_get("/", response=List[JobSearchSchema])
    def search_jobs(self, request, query: str):
        if not query:
            return []
        results = JobDocument.search().query("multi_match", query=query, fields=['title', 'description', 'location', 'company_name', 'status'])
        if not results:
            return HttpError(404, "No jobs found") 
        return [hit.to_dict() for hit in results]
    