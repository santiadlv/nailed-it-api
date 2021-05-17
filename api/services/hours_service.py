from fastapi import Request, HTTPException, status
from typing import Optional
from ..crud.hours_crud import CRUDHours
from ..models.hours_model import AvailabilityBase, AvailabilityGet


class HoursService():
    async def insert_hours(request: Request, hours_in: AvailabilityBase) -> Optional[AvailabilityBase]:
        existing_hours = await CRUDHours.retrieve(request, hours_in)
        if existing_hours:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Availability hours for service with ID {hours_in['service_id']} already exist"
            )

        new_hours = await CRUDHours.insert(request, hours_in)
        if not new_hours:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Availability hours for service with ID {hours_in['service_id']} could not be inserted"
            )
        return new_hours

    async def get_availability_by_service_id(request: Request, hours_in: AvailabilityGet) -> Optional[AvailabilityBase]:
        retrieved_hours = await CRUDHours.retrieve(request, hours_in)
        if not retrieved_hours:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Availability hours for service with ID {hours_in['service_id']} could not be found"
            )
        return retrieved_hours

    async def update_availability_hours(request: Request, hours_in: AvailabilityBase) -> Optional[AvailabilityBase]:
        updated_hours = await CRUDHours.update(request, hours_in)
        if not updated_hours:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Availability hours for service with ID {hours_in['service_id']} could not be updated"
            )
        return updated_hours
