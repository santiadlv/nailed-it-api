from fastapi import Request, HTTPException, status
from typing import Optional
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
