from typing import Optional, List
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..models import service_model
from ..core import settings

class CRUDService():
    async def create(request: Request, obj_in: service_model.ServiceBase) -> Optional[service_model.ServiceBase]:
        new_service = service_model.ServiceBase(
            name=obj_in['name'],
            estimatedTimeLower=obj_in['estimatedTimeLower'],
            estimatedTimeHigher=obj_in['estimatedTimeHigher'],
            imageUrl=obj_in['imageUrl'],
            price=obj_in['price'],
            rating=obj_in['rating'],
            salon_id=obj_in['salon_id']
        )
        serialized_service = jsonable_encoder(new_service)
        new_service = await request.app.mongodb[settings.MONGODB_COLLECTION_SERVICES].insert_one(serialized_service)
        return serialized_service
