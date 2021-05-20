from typing import List
from fastapi import APIRouter, Request, status, Path, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import reservation_model
from ..services.reservation_service import ReservationService
import datetime

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
    responses={404: {"description" : "Not found"}}
)

@router.post("/new", status_code=status.HTTP_201_CREATED, response_description="Reservation created", response_model= reservation_model.ReservationBase)
async def create_reservation(request: Request, reservation_in: reservation_model.ReservationBase) -> JSONResponse:
    reservation_in = jsonable_encoder(reservation_in)
    removeServiceHour = await ReservationService.removeAvailabilityHour(request, reservation_in)
    new_reservation = await ReservationService.create(request, reservation_in)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "Reservation added successfully", "data" : new_reservation})

@router.get("/list/{user_id}", status_code=status.HTTP_200_OK, response_description="List all reservations by User", response_model=List[reservation_model.ReservationBase])
async def get_all_reservations(request: Request, user_id: str = Path(..., title="The ID of the user whose list of reservations to get")) -> JSONResponse:
    reservations_information = await  ReservationService.get_all_reservations(request, user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": reservations_information})

@router.get("/{user_id}/{reservation_id}", status_code=status.HTTP_200_OK, response_description="Reservation Information", response_model=reservation_model.ReservationBase)
async def get_reservation(request: Request, user_id: str = Path(..., title="The ID of the user to get reservations"), reservation_id: str = Path(..., title="The ID of the reservation")) -> JSONResponse:
    reservation_information = await  ReservationService.get_reservations_by_id(request, user_id, reservation_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": reservation_information})
    
