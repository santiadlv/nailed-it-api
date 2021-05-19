from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from .objectid_model import PyObjectId

class ReservationBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: str = Field(...)
    service_id: str = Field(...)
    time_start: int = Field(...)
    time_end: int = Field(...)
    hour_id: str  = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
              "user_id": "605cd9ca1ec4bf19fe3f9581",
              "service_id": "60860830041aa13d76554242",
              "time_start": 870,
              "time_end": 900,
              "hour_id": "d7b9599a-28da-48c7-b6e6-e6eba7a502fa"
            }
        }
        