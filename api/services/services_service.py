from fastapi import Request, HTTPException
from typing import Optional, List
from ..crud.service_crud import CRUDService
from ..models import service_model, salon_model

class ServicesService():
    async def create(request: Request, service_in: service_model.ServiceBase) -> Optional[service_model.ServiceBase]:
        service = await CRUDService.create(request, service_in)
        return service

    async def get_services(request: Request, salon: salon_model.SalonServices) -> Optional[List[service_model.ServiceBase]]:
        retrieved_services = await CRUDService.get_services_by_salon_id(request, salon)
        if not retrieved_services:
            raise HTTPException(
                status_code=404, 
                detail="Services for specified salon not found"
            )
        return retrieved_services
