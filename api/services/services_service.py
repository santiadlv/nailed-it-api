from fastapi import Request, HTTPException, status
from typing import Optional, List

from starlette.status import HTTP_404_NOT_FOUND
from ..crud.service_crud import CRUDService
from ..models import service_model, salon_model

class ServicesService():
    async def create(request: Request, service_in: service_model.ServiceBase) -> Optional[service_model.ServiceBase]:
        service = await CRUDService.create(request, service_in)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Service could not be created"
            )
        return service

    async def get_services(request: Request, salon: salon_model.SalonServices) -> Optional[List[service_model.ServiceBase]]:
        retrieved_services = await CRUDService.get_services_by_salon_id(request, salon)
        if not retrieved_services:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Services for specified salon not found"
            )
        return retrieved_services

    async def get_service_price(request: Request, service: service_model.ServiceIdentifier) -> Optional[str]:
        service_price = await CRUDService.get_service_price(request, service)
        if not service_price:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Price for selected service not found"
            )
        return service_price
