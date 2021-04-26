from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import salon_model
from ..services.salon_service import SalonService
from ..core import settings
from typing import List

router = APIRouter(
    prefix="/salons",
    tags=["salons"],
    responses={404: {"description" : "Not found"}}
)

@router.post("/new", status_code=status.HTTP_201_CREATED, response_description="Create new salon", response_model=salon_model.SalonBase)
async def create_salon(request: Request, salon_in: salon_model.SalonBase) -> JSONResponse:
    salon_in = jsonable_encoder(salon_in)
    new_salon = await SalonService.create(request, salon_in)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"messsage" : "Salon added successfully", "data" : new_salon})

@router.get("/", response_model=List[salon_model.SalonBase], response_description="Salons Information")
async def get_all_salons(request: Request) -> JSONResponse:
    salons_information = await  SalonService.get_all_salons(request)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": salons_information})
