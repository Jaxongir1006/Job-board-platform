from ninja import Schema, ModelSchema
from .models import Review
from typing import Optional



class ReviewSchema(ModelSchema):
    class Config:
        model = Review
        model_fields = ["id", "rating", "comment", "created_at", "updated_at", "job", "user"]
        from_attributes = True


class CreateReviewSchema(Schema):
    rating: int
    comment: Optional[str] = None