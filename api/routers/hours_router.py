from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models.hours_model import AvailabilityAdd, AvailabilityBase, AvailabilityGet, AvailabilityRemove
from ..services.hours_service import HoursService


router = APIRouter(
    prefix="/hours",
    tags=["availability hours"],
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
    updated_hours = await HoursService.update_availability_hours(request, hours_in)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message" : "Service's availability hours updated successfully", "data" : updated_hours})

@router.post("/update/add", status_code=status.HTTP_200_OK, response_description="Add an entry to a service's availability hours", response_model=AvailabilityBase)
async def add_service_hour(request: Request, hours_in: AvailabilityAdd) -> JSONResponse:
    hours_in = jsonable_encoder(hours_in)
    updated_hours = await HoursService.add_availability_hour(request, hours_in)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message" : "Successfully added an hour to the service's availability", "data" : updated_hours})

@router.post("/update/remove", status_code=status.HTTP_202_ACCEPTED, response_description="Remove an entry from a service's availability hours", response_model=AvailabilityBase)
async def remove_service_hour(request: Request, hours_in: AvailabilityRemove) -> JSONResponse:
    hours_in = jsonable_encoder(hours_in)
    updated_hours = await HoursService.remove_availability_hour(request, hours_in)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message" : "Successfully removed an hour from the service's availability", "data" : updated_hours})
    