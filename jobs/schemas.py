from ninja import Schema, ModelSchema
from .models import Job, JobCategory
from typing import Optional
from pydantic import BaseModel

class JobSchema(ModelSchema):
    class Config:
        model = Job
        model_fields = ["title", "description", "salary", "image", "location", "company_name", "company_description", "status", 'slug', 'contact', 'category']
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
    contact: str    


class UpdateJobSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[str] = None
    image: Optional[str] = None
    location: Optional[str] = None
    company_name: Optional[str] = None
    company_description: Optional[str] = None
    contact: Optional[str] = None



class JobSearchSchema(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    company_name: Optional[str] = None
    status: Optional[str] = None
    salary: Optional[int] = None
    slug: Optional[str] = None
    category: Optional[str] = None