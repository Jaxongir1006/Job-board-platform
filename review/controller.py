from ninja_extra import api_controller, http_post, http_get, http_delete
from .models import Review
from .schemas import ReviewSchema, CreateReviewSchema
from utils.permissions import IsAuthenticatedAndNotDeleted
from ninja_jwt.authentication import JWTAuth
from jobs.models import Job
from typing import List
from django.db.models import Avg

@api_controller(tags=["Reviews"], auth=JWTAuth(), permissions=[IsAuthenticatedAndNotDeleted])
class ReviewController:
    @http_post("create-review/{job_slug}/", response=ReviewSchema)
    def create(self, job_slug, request, data: CreateReviewSchema):
        data = data.model_dump()
        data["user"] = request.user
        job = Job.objects.filter(slug=job_slug).first()
        if data['rating'] < 1 or data['rating'] > 5:
            return {"message": "Rating must be between 1 and 5"}
        if not job:
            return {"message": "Job not found"}
        data["job"] = job
        review = Review.objects.create(**data)
        return review

    @http_get("reviews/{job_slug}/", response=List[ReviewSchema])
    def list_reviews(self, job_slug: str):
        """
        List all reviews for a specific job.
        This endpoint retrieves all reviews associated with a job identified by its slug.
        """
        job = Job.objects.filter(slug=job_slug).first()
        if not job:
            return {"message": "Job not found"}
        
        reviews = Review.objects.filter(job=job)
        return reviews
    

    @http_delete("reviews/{job_slug}/", response=dict)
    def delete_review(self, job_slug: str, request):
        """
        Delete a review for a specific job.
        This endpoint allows users to delete their own reviews for a job identified by its slug.
        """
        user = request.user
        job = Job.objects.filter(slug=job_slug).first()
        if not job:
            return {"message": "Job not found"}
        
        review = Review.objects.filter(job=job, user=user).first()
        if not review:
            return {"message": "Review not found"}
        
        review.delete()
        return {"message": "Review deleted successfully"}
    
    @http_get("reviews/{job_slug}/average-rating/", response=dict)
    def average_rating(self, job_slug: str):
        """
        Get the average rating for a specific job.
        This endpoint calculates and returns the average rating of all reviews for a job identified by its slug.
        """
        job = Job.objects.filter(slug=job_slug).first()
        if not job:
            return {"message": "Job not found"}
        
        reviews = Review.objects.filter(job=job)
        if not reviews:
            return {"average_rating": 0}
        
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        return {"average_rating": average_rating or 0}