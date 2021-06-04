from typing import Optional, List
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..models import reviews_model
from ..core import settings

class CRUDReview():
    async def create(request: Request, obj_in: reviews_model.ReviewBase) -> Optional[reviews_model.ReviewBase]:
        new_review = reviews_model.ReviewBase(
            title=obj_in['title'],
            date=obj_in['date'],
            reviewDescription=obj_in['reviewDescription'],
            salon_id=obj_in['salon_id'],
            user_id=obj_in['user_id'],
            service_id=obj_in['service_id']
        )
        serialized_review = jsonable_encoder(new_review)
        new_review = await request.app.mongodb[settings.MONGODB_COLLECTION_REVIEWS].insert_one(serialized_review)
        return serialized_review

    async def get_reviews_by_salon(request: Request, id: str) -> Optional[List[reviews_model.ReviewBase]]:
        # reviews_salon = await request.app.mongodb[settings.MONGODB_COLLECTION_REVIEWS].find({'salon_id': id}).to_list(1000)
        if (reviews_salon := await request.app.mongodb[settings.MONGODB_COLLECTION_REVIEWS].find({"salon_id": id}).to_list(1000)) is not None:
            return reviews_salon
        else: return None

    async def get_reviews_by_service(request: Request, id: str) -> Optional[reviews_model.ReviewBase]:
        if (reviews_service := await request.app.mongodb[settings.MONGODB_COLLECTION_REVIEWS].find({"service_id": id}).to_list(1000)) is not None:
            return reviews_service
        else: return None
