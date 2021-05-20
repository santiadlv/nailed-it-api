from typing import Optional, List
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..models import reservation_model
from ..core import settings
from ..routers import hours_router
import datetime

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
        info_reservation = await CRUDReservation.informationReservation(request, obj_in)
        return info_reservation

    async def informationReservation(request: Request, obj_in: reservation_model.ReservationInfo) -> Optional[reservation_model.ReservationInfo]:
        dateToday = datetime.datetime.now()
        service_info = await request.app.mongodb[settings.MONGODB_COLLECTION_SERVICES].find_one({'_id': obj_in['service_id']})
        salon_name = await request.app.mongodb[settings.MONGODB_COLLECTION_SALONS].find_one({'_id': service_info["salon_id"]})
        reservation_info = reservation_model.ReservationInfo(
            user_id=obj_in['user_id'],
            service_id=obj_in['service_id'],
            time_start=obj_in['time_start'],
            time_end=obj_in['time_end'],
            hour_id=obj_in['hour_id'],
            salon_name=salon_name["name"],
            service_name=service_info["name"],
            date=dateToday,
            price=service_info["price"]
        )
        serialized_reservation = jsonable_encoder(reservation_info)
        return serialized_reservation

    async def removeAvailability(request: Request, obj_in: reservation_model.ReservationConfirm) -> Optional[reservation_model.ReservationConfirm]:
        reservation_confirm = reservation_model.ReservationConfirm(
            service_id=obj_in['service_id'],
            hour_id=obj_in['hour_id']
        )
        serialized_reservation = jsonable_encoder(reservation_confirm)
        reservation_confirm = await hours_router.remove_service_hour(request, serialized_reservation)

    async def get_reservations(request: Request, user_id: str) -> Optional[List[reservation_model.ReservationBase]]:
        reservations = await request.app.mongodb[settings.MONGODB_COLLECTION_RESERVATIONS].find({"user_id": user_id}).to_list(1000)
        return reservations

    async def get_reservation_by_id(request: Request, user_id: str, reservation_id: str) -> Optional[reservation_model.ReservationBase]:
        if (reservation := await request.app.mongodb[settings.MONGODB_COLLECTION_RESERVATIONS].find_one({'_id': reservation_id, 'user_id': user_id})) is not None:
            return reservation
        else: return None

    async def addAvailability(request: Request, obj_in: reservation_model.ReservationCancel, reservation_id: str) -> Optional[reservation_model.ReservationCancel]:
        cancel_reservation = reservation_model.ReservationCancel(
            service_id=obj_in["service_id"],
            timeStart=obj_in['timeStart'],
            timeEnd=obj_in['timeEnd']
        )

        serialized_reservation = jsonable_encoder(cancel_reservation)
        cancel_reservation = await hours_router.add_service_hour(request, serialized_reservation)

        if (result := await request.app.mongodb[settings.MONGODB_COLLECTION_RESERVATIONS].find_one_and_delete({"_id": reservation_id})) is not None:
            serialized_user = jsonable_encoder(result)
            return serialized_user
        else: return None


        