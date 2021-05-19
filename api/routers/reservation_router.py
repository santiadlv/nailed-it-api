from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import reservation_model
from ..services.reservation_service import ReservationService

router = APIRouter(
    prefix="/reservation",
    tags=["reservations"],
    responses={404: {"description" : "Not found"}}
)

@router.post("/new", status_code=status.HTTP_201_CREATED, response_description="Reservation created", response_model= reservation_model.ReservationBase)
async def create_salon(request: Request, reservation_in: reservation_model.ReservationBase) -> JSONResponse:
    reservation_in = jsonable_encoder(reservation_in)
    new_reservation = await ReservationService.create(request, reservation_in)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "Reservation added successfully", "data" : new_reservation})
