from typing import Any, List
from uuid import uuid4
from bson.objectid import ObjectId
from pydantic import BaseModel, Field, validator
from .objectid_model import PyObjectId

def check_field_not_empty(value: str) -> str:
    assert value != "", 'Empty strings are not allowed'
    return value

def check_valid_hour(value: int) -> int:
    assert value in range(0, 1440), f'Time value {str(value)} is not inside acceptable range (0 - 1440)'
    return value

class AvailabilityBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    service_id: str = Field(...)
    hours: List[dict[str, Any]]

    service_id_validate = validator('service_id', allow_reuse=True)(check_field_not_empty)

    @validator('hours')
    def check_valid_hour_in_array(cls, v):
        for hours in v:
            for key in hours:
                if key != 'hour_id':
                    assert hours[key] in range(0, 1440), f'A time value in the array ({str(hours[key])}) \
                                                           is not inside the acceptable range (0 - 1440)'
        return v

    def set_hours_id(self):
        for dict in self.hours:
            if 'hour_id' not in dict:
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

    service_id_validate = validator('service_id', allow_reuse=True)(check_field_not_empty)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "service_id": "60860830041aa13d76554242",
            }
        }

class AvailabilityAdd(BaseModel):
    service_id: str = Field(...)
    timeStart: int = Field(...)
    timeEnd: int =  Field(...)

    service_id_validate = validator('service_id', allow_reuse=True)(check_field_not_empty)
    time_start_validate = validator('timeStart', allow_reuse=True)(check_valid_hour)
    time_end_validate = validator('timeEnd', allow_reuse=True)(check_valid_hour)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "service_id": "60860830041aa13d76554242",
                "timeStart": 480,
                "timeEnd": 510
            }
        }

class AvailabilityRemove(BaseModel):
    service_id: str = Field(...)
    hour_id: str = Field(...)
    
    service_id_validate = validator('service_id', allow_reuse=True)(check_field_not_empty)
    hour_id_validate = validator('hour_id', allow_reuse=True)(check_field_not_empty)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "service_id": "60860830041aa13d76554242",
                "hour_id": "395c7e3a-9c71-4e03-8d1c-c424f51716c7"
            }
        }
