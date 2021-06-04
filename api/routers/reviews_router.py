from fastapi import APIRouter, Request, status, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import reviews_model
from ..services.reviews_service import ReviewService
from typing import List

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
    responses={404: {"description" : "Not found"}}
)

@router.post("/new", status_code=status.HTTP_201_CREATED, response_description="Added new review", response_model=reviews_model.ReviewBase)
async def create_review(request: Request, review_in: reviews_model.ReviewBase) -> JSONResponse:
    review_in = jsonable_encoder(review_in)
    new_review = await ReviewService.create(request, review_in)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "Review created successfully", "data" : new_review})

@router.get("/salon/{id}", status_code=status.HTTP_200_OK, response_description="List all reviews by salons", response_model=List[reviews_model.ReviewBase])
async def get_all_reviews_salons(request: Request, id: str = Path(..., title = "The ID of the salon")) -> JSONResponse:
    reviews_salons = await  ReviewService.get_all_reviews_by_salons(request, id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": reviews_salons})

@router.get("/service/{id}", status_code=status.HTTP_200_OK, response_description="List all reviews by service", response_model=reviews_model.ReviewBase)
async def get_all_reviews_service(request: Request, id: str = Path(..., title="The ID of the service")) -> JSONResponse:
    reviews_service = await  ReviewService.get_all_reviews_by_service(request, id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": reviews_service})
    