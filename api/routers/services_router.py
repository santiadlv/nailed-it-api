from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import service_model
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
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"messsage" : "Service added successfully", "data" : new_service})
    