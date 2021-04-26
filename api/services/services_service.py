from fastapi import Request
from typing import Optional
from ..crud.service_crud import CRUDService
from ..models import service_model

class ServicesService():
    async def create(request: Request, service_in: service_model.ServiceBase) -> Optional[service_model.ServiceBase]:
        service = await CRUDService.create(request, service_in)
        return service
        