from ninja import Schema, ModelSchema
from .models import JobApplication


class JobApplicationSchema(ModelSchema):
    class Config:
        model = JobApplication
        model_fields = ["id", "cover_letter", "resume", "status", "created_at", "updated_at", "job", "user"]


class CreateJobApplicationSchema(Schema):
    cover_letter: str
    resume: str