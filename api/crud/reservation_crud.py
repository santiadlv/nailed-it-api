from typing import Optional
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..models import reservation_model
from ..core import settings

class CRUDReservation():
    async def create(request: Request, obj_in: reservation_model.ReservationBase) -> Optional[reservation_model.ReservationBase]:
        new_reservation = reservation_model.ReservationBase(
            user_id=obj_in['user_id'],
            service_id=obj_in['service_id'],
            time_start=obj_in['time_start'],
            time_end=obj_in['time_end'],
            hour_id=obj_in['hour_id']
        )
        serialized_reservation = jsonable_encoder(new_reservation)
        new_reservation = await request.app.mongodb[settings.MONGODB_COLLECTION_RESERVATIONS].insert_one(serialized_reservation)
        return serialized_reservation