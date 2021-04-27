from fastapi import Request, HTTPException, status
from typing import Optional, List
from ..crud.salon_crud import CRUDSalon
from ..models import salon_model

class SalonService():
    async def create(request: Request, salon_in: salon_model.SalonBase) -> Optional[salon_model.SalonBase]:
        salon = await CRUDSalon.create(request, salon_in)
        if not salon:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Salon could not be created"
            )
        return salon

    async def get_all_salons(request: Request) -> Optional[List[salon_model.SalonBase]]:
        retrieved_salons = await CRUDSalon.get_salons(request)
        if not retrieved_salons:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Salons not found"
            )
        return retrieved_salons

    async def get_salon_by_id(request: Request, id: str) -> Optional[salon_model.SalonBase]:
        retrieved_salon = await CRUDSalon.get_salon_by_id(request, id)
        if not retrieved_salon:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Salon with ID {id} not found"
            )
        return retrieved_salon
