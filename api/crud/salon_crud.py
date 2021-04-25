from typing import Optional, List
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..models import salon_model
from ..core import settings

class CRUDSalon():
    async def create(request: Request, obj_in: salon_model.SalonBase) -> Optional[salon_model.SalonBase]:
        new_salon = salon_model.SalonBase(
            name=obj_in['name'],
            openHour=obj_in['openHour'],
            closeHour=obj_in['closeHour'],
            imageUrl=obj_in['imageUrl'],
            appointment=obj_in['appointment'],
            rating=obj_in['rating'],
            available=obj_in['available']
        )
        serialized_salon = jsonable_encoder(new_salon)
        new_salon = await request.app.mongodb[settings.MONGODB_COLLECTION_SALONS].insert_one(serialized_salon)
        return serialized_salon

    async def get_salons(request: Request) -> List[salon_model.SalonBase]:
        
        students = await request.app.mongodb[settings.MONGODB_COLLECTION_SALONS].find().to_list(1000)
        return students
