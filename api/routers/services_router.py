from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import service_model, salon_model
from ..services.services_service import ServicesService

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}}
)

@router.post("/new", status_code=status.HTTP_201_CREATED, response_description="Create new service", response_model=service_model.ServiceBase)
async def create_service(request: Request, service_in: service_model.ServiceBase) -> JSONResponse:
    service_in = jsonable_encoder(service_in)
    new_service = await ServicesService.create(request, service_in)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "Service added successfully", "data" : new_service})

@router.post("/get", status_code=status.HTTP_200_OK, response_description="Get services by salon ID", response_model=service_model.ServiceBase)
async def get_services_by_salon_id(request: Request, salon: salon_model.SalonServices) -> JSONResponse:
    salon = jsonable_encoder(salon)
    service_list = await ServicesService.get_services(request, salon)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message" : "List retrieved successfully", "data" : service_list})

@router.post("/get/id", status_code=status.HTTP_200_OK, response_description="Get service by ID")
async def get_service_by_id(request: Request, service: service_model.ServiceIdentifier) -> JSONResponse:
    service = jsonable_encoder(service)
    service_price = await ServicesService.get_service_by_id(request, service)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message" : "Service retrieved successfully", "data" : service_price})

@router.post("/filter", status_code=status.HTTP_200_OK, response_description="Get filtered services by one or more categories")
async def get_services_by_category(request: Request, categories: service_model.ServiceCategory) -> JSONResponse:
    categories = jsonable_encoder(categories)
    filtered_services = await ServicesService.get_filtered_services(request, categories)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "List of filtered services retrieved successfully", "data": filtered_services})
