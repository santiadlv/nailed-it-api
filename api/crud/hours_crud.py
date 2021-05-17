from typing import Optional
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..models import hours_model
from ..core import settings

class CRUDHours():
    async def insert(request: Request, obj_in: hours_model.AvailabilityBase) -> Optional[hours_model.AvailabilityBase]:
        new_hours = hours_model.AvailabilityBase(
            service_id=obj_in['service_id'],
            hours=obj_in['hours']
        )

        serialized_hours = jsonable_encoder(new_hours)
        new_hours = await request.app.mongodb[settings.MONGODB_COLLECTION_HOURS].insert_one(serialized_hours)
        return serialized_hours

    async def retrieve(request: Request, obj_in: hours_model.AvailabilityGet) -> Optional[hours_model.AvailabilityBase]:
        hours = await request.app.mongodb[settings.MONGODB_COLLECTION_HOURS].find_one({'service_id': obj_in['service_id']})
        return hours

    async def update(request: Request, obj_in: hours_model.AvailabilityBase) -> Optional[hours_model.AvailabilityBase]:
        query = {"service_id" : obj_in['service_id']}
        update_values = { "$set" : {"hours" : obj_in['hours']}}

        await request.app.mongodb[settings.MONGODB_COLLECTION].find_one_and_update(query, update_values)
        updated_user = await request.app.mongodb[settings.MONGODB_COLLECTION].find_one({"service_id": obj_in['service_id']})
        return updated_user
