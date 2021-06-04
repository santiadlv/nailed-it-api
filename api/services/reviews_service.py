from fastapi import Request, HTTPException, status
from typing import Optional, List
from ..crud.reviews_crud import CRUDReview
from ..models import reviews_model

class ReviewService():
    async def create(request: Request, review_in: reviews_model.ReviewBase) -> Optional[reviews_model.ReviewBase]:
        review = await CRUDReview.create(request, review_in)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Review could not be created, please try again later."
            )
        return review

    async def get_all_reviews_by_salons(request: Request, id: str) -> Optional[List[reviews_model.ReviewBase]]:
        retrieved_reviews = await CRUDReview.get_reviews_by_salon(request, id)
        if not retrieved_reviews:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Reviews not found"
            )
        return retrieved_reviews

    async def get_all_reviews_by_service(request: Request, id: str) -> Optional[reviews_model.ReviewBase]:
        retrieved_reviews = await CRUDReview.get_reviews_by_service(request, id)
        if not retrieved_reviews:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Reviews not found"
            )
        return retrieved_reviews

