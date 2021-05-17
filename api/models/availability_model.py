from typing import List
from bson.objectid import ObjectId
from pydantic import BaseModel, Field, validator
from .objectid_model import PyObjectId


class HoursBase(BaseModel):
    timeStart: int = Field(...)
    timeEnd: int = Field(...)

    @validator('timeStart', 'timeEnd')
    def check_valid_hour(cls, v, values, **kwargs):
        start = 'timeStart' in values
        end = 'timeEnd' in values
        assert (0 <= start <= 1440) and (0 <= end <= 1440), 'Time value is not inside acceptable range (0 - 1440)'
        return values

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "timeStart": 960,
                "timeEnd": 1020
            }
        }

class AvailabilityBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    service_id: str = Field(...)
    hours: List[HoursBase] = Field(...)

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
