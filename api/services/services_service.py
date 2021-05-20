from fastapi import Request, HTTPException, status
from typing import Optional, List
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

    async def get_service_by_id(request: Request, service: service_model.ServiceIdentifier) -> Optional[service_model.ServiceBase]:
        service = await CRUDService.get_service_by_id(request, service)
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service with provided ID could not found"
            )
        return service
