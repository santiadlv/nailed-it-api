from uuid import uuid4
from fastapi import Request, HTTPException, status
from typing import Optional
from ..crud.hours_crud import CRUDHours
from ..models.hours_model import AvailabilityBase, AvailabilityGet, AvailabilityAdd, AvailabilityRemove


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
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"Availability hours for service with ID {hours_in['service_id']} could not be found"
            )
        elif not retrieved_hours['hours']:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There are no available hours for service with ID {hours_in['service_id']} as of right now"
            )
        return retrieved_hours

    async def update_availability_hours(request: Request, hours_in: AvailabilityBase) -> Optional[AvailabilityBase]:
        updated_hours = await CRUDHours.update(request, hours_in)
        if not updated_hours:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Availability hours for service with ID {hours_in.service_id} could not be updated"
            )
        return updated_hours

    async def add_availability_hour(request: Request, hours_in: AvailabilityAdd) -> Optional[AvailabilityBase]:
        existing_hours = await CRUDHours.retrieve_by_id(request, hours_in['service_id'])
        if not existing_hours:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"Availability hours for service with ID {hours_in['service_id']} could not be found"
            )

        new_hour = {"timeStart": hours_in['timeStart'], "timeEnd": hours_in['timeEnd'], 'hour_id': str(uuid4())}
        existing_hours['hours'].append(new_hour)
        updated_availability = AvailabilityBase(
            service_id=existing_hours['service_id'],
            hours=sorted(existing_hours['hours'], key=lambda i: i['timeStart'])
        )

        updated_hours = await CRUDHours.update(request, updated_availability)
        if not updated_hours:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Availability hours for service with ID {hours_in['service_id']} could not be updated"
            )
        return updated_hours

    async def remove_availability_hour(request: Request, hours_in: AvailabilityRemove) -> Optional[AvailabilityBase]:
        existing_hours = await CRUDHours.retrieve_by_id(request, hours_in['service_id'])
        if not existing_hours:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"Availability hours for service with ID {hours_in['service_id']} could not be found"
            )

        new_hours = [i for i in existing_hours['hours'] if not (i['hour_id'] == hours_in['hour_id'])]
        if new_hours == existing_hours['hours']:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"Hour with ID {hours_in['hour_id']} could not be found in service"
            )

        updated_availability = AvailabilityBase(
            service_id=existing_hours['service_id'],
            hours=sorted(new_hours, key=lambda i: i['timeStart'])
        )

        updated_hours = await CRUDHours.update(request, updated_availability)
        if not updated_hours:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Availability hours for service with ID {hours_in['service_id']} could not be updated"
            )
        return updated_hours
