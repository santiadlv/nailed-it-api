from fastapi import Request, HTTPException, status
from typing import Optional, List
from ..crud.reservation_crud import CRUDReservation
from ..models import reservation_model

class ReservationService():
    async def create(request: Request, reservation_in: reservation_model.ReservationBase) -> Optional[reservation_model.ReservationBase]:
        reservation = await CRUDReservation.create(request, reservation_in)
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reservation could not be created"
            )
        return reservation


    async def removeAvailabilityHour(request: Request, reservation_in: reservation_model.ReservationBase) -> Optional[reservation_model.ReservationConfirm]:
        reservation = await CRUDReservation.removeAvailability(request, reservation_in)
        return reservation

    async def get_all_reservations(request: Request, user_id) -> Optional[List[reservation_model.ReservationBase]]:
        retrieved_reservations = await CRUDReservation.get_reservations(request, user_id)
        if not retrieved_reservations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No Reservations Found For This User"
            )
        return retrieved_reservations

    async def get_reservations_by_id(request: Request, user_id: str, reservation_id: str) -> Optional[reservation_model.ReservationBase]:
        retrieved_reservation = await CRUDReservation.get_reservation_by_id(request, user_id, reservation_id)
        if not retrieved_reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User with ID {user_id} and reservation with ID {reservation_id} was not found"
            )
        return retrieved_reservation

