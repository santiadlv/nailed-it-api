from typing import Any, List
from uuid import uuid4
from bson.objectid import ObjectId
from pydantic import BaseModel, Field, validator
from .objectid_model import PyObjectId


class AvailabilityBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    service_id: str = Field(...)
    hours: List[dict[str, Any]]

    @validator('hours')
    def check_valid_hour(cls, v):
        for hours in v:
            for key in hours:
                if key != 'id':
                    assert hours[key] in range(0, 1440), 'Time value is not inside acceptable range (0 - 1440)'
        return v

    def set_hours_id(self):
        for dict in self.hours:
            new_uuid = str(uuid4())
            dict.update(hour_id=new_uuid)
        return self

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "service_id": "60860830041aa13d76554242",
                "hours": [{"timeStart": 660, "timeEnd": 750},
                          {"timeStart": 870, "timeEnd": 900},
                          {"timeStart": 960, "timeEnd": 990}]
            }
        }

class AvailabilityGet(BaseModel):
    service_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "service_id": "60860830041aa13d76554242",
            }
        }
