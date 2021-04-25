from fastapi import Request, HTTPException
from typing import Optional
from ..crud.salon_crud import CRUDSalon
from ..models import salon_model
from ..core import security

class SalonService():

    async def create(request: Request, salon_in: salon_model.SalonBase) -> Optional[salon_model.SalonBase]:
        salon = await CRUDSalon.create(request, salon_in)
        return salon


    async def get_all_salons(request: Request):
        retrieved_salons = await CRUDSalon.get_salons(request)
        if not retrieved_salons:
            raise HTTPException(
                status_code=404, 
                detail="Salons not found"
            )
        return retrieved_salons
