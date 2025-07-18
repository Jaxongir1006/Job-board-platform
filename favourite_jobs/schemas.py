from ninja import Schema, ModelSchema
from .models import FavouriteJob
from jobs.models import Job

class JobSchema(ModelSchema):
    class Config:
        model = Job
        model_fields = ["title", "description", "salary", "image", "location", "company_name", "company_description", "status", 'slug', 'contact', 'category']
        from_attributes = True

class FavouriteJobSchema(ModelSchema):
    job: JobSchema  # nested schema
    class Config:
        model = FavouriteJob
        model_fields = ['job']
        from_attributes = True  