from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from .models import Job, JobCategory
from .schemas import JobSchema, JobCategorySchema, CreateJobSchema
from ninja_jwt.authentication import JWTAuth
from utils.permissions import IsAuthenticatedAndNotDeleted
from typing import List
from ninja.errors import HttpError


@api_controller(
    "", tags=["Jobs"], auth=JWTAuth(), permissions=[IsAuthenticatedAndNotDeleted]
)
class JobsController:
    @http_get("categories/", response=List[JobCategorySchema])
    def get_categories(self):
        return JobCategory.objects.all()

    @http_get("jobs/{category_slug}/", response=List[JobSchema])
    def get_jobs(self, category_slug: str):
        return Job.objects.filter(category__slug=category_slug)

    @http_get("job/{job_slug}/", response=JobSchema)
    def get_job(self, job_slug: str):
        try:
            job = Job.objects.get(slug=job_slug)
            print(JobSchema.from_orm(job).dict())
        except Job.DoesNotExist:
            raise HttpError(404, "Job not found")
        return job

    @http_post("create-job/", response=dict)
    def create_job(self, data: CreateJobSchema):
        data = data.model_dump()
        category = JobCategory.objects.filter(slug=data["category"]).first()
        if not category:
            return HttpError(400, "Category not found")
        data["category"] = category
        job = Job.objects.create(**data)
        return {
            "message": "Job created successfully",
            "slug": job.slug,
            "category": job.category.title,
            "title": job.title,
        }
