from typing import Optional
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..models.hours_model import AvailabilityBase, AvailabilityGet
from ..core import settings


class CRUDHours():
    async def insert(request: Request, obj_in: AvailabilityBase) -> Optional[AvailabilityBase]:
        new_hours = AvailabilityBase(
            service_id=obj_in['service_id'],
            hours=sorted(obj_in['hours'], key=lambda i: i['timeStart'])
        )

        new_hours = new_hours.set_hours_id()
        serialized_hours = jsonable_encoder(new_hours)
        new_hours = await request.app.mongodb[settings.MONGODB_COLLECTION_HOURS].insert_one(serialized_hours)
        return serialized_hours

    async def retrieve(request: Request, obj_in: AvailabilityGet) -> Optional[AvailabilityBase]:
        hours = await request.app.mongodb[settings.MONGODB_COLLECTION_HOURS].find_one({'service_id': obj_in['service_id']})
        return hours

    async def retrieve_by_id(request: Request, service_id: str) -> Optional[AvailabilityBase]:
        hours = await request.app.mongodb[settings.MONGODB_COLLECTION_HOURS].find_one({'service_id': service_id})
        return hours

    async def update(request: Request, obj_in: AvailabilityBase) -> Optional[AvailabilityBase]:
        obj_in = obj_in.set_hours_id()
        query = {"service_id" : obj_in.service_id}
        update_values = { "$set" : {"hours" : obj_in.hours}}

        await request.app.mongodb[settings.MONGODB_COLLECTION_HOURS].find_one_and_update(query, update_values)
        updated_user = await request.app.mongodb[settings.MONGODB_COLLECTION_HOURS].find_one({"service_id": obj_in.service_id})
        return updated_user
