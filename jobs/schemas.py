from ninja import Schema, ModelSchema
from .models import Job, JobCategory


class JobSchema(ModelSchema):
    class Config:
        model = Job
        model_fields = ["title", "description", "salary", "image", "location", "company_name", "company_description", "status", 'slug']
        from_attributes = True

class JobCategorySchema(ModelSchema):
    class Config:
        model = JobCategory
        model_fields = ["title", "image", "description", 'slug']
        from_attributes = True

class CreateJobSchema(Schema):
    title: str
    description: str
    category: str
    salary: str
    image: str
    location: str
    company_name: str
    company_description: str