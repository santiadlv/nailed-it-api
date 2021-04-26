from typing import Optional, List
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..models import service_model, salon_model
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

    async def get_services_by_salon_id(request: Request, salon: salon_model.SalonServices) -> Optional[List[service_model.ServiceBase]]:
        print(salon)
        services = await request.app.mongodb[settings.MONGODB_COLLECTION_SERVICES].find({'salon_id': salon['id']}).to_list(1000)
        return services
