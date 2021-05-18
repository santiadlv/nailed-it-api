from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models.hours_model import AvailabilityBase, AvailabilityGet
from ..services.hours_service import HoursService

router = APIRouter(
    prefix="/hours",
    tags=["hours, availability"],
    responses={404: {"description": "Not found"}}
)

@router.post("/insert", status_code=status.HTTP_201_CREATED, response_description="Insert new service availability hours", response_model=AvailabilityBase)
async def insert_hours(request: Request, hours_in: AvailabilityBase) -> JSONResponse:
    hours_in = jsonable_encoder(hours_in)
    new_hours = await HoursService.insert_hours(request, hours_in)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "Availability hours inserted successfully", "data" : new_hours})

@router.post("/get", status_code=status.HTTP_200_OK, response_description="Get availability hours by service ID", response_model=AvailabilityBase)
async def get_hours_by_service_id(request: Request, hours_in: AvailabilityGet) -> JSONResponse:
    hours_in = jsonable_encoder(hours_in)
    retrieved_hours = await HoursService.get_availability_by_service_id(request, hours_in)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message" : "Availability hours retrieved successfully", "data" : retrieved_hours})

@router.post("/update", status_code=status.HTTP_200_OK, response_description="Update service's availability hours", response_model=AvailabilityBase)
async def update_service_hours(request: Request, hours_in: AvailabilityBase) -> JSONResponse:
    hours_in = jsonable_encoder(hours_in)
    updated_hours = await HoursService.update_availability_hours(request, hours_in)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message" : "Service's availability hours updated successfully", "data" : updated_hours})
