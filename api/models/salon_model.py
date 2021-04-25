from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from .objectid_model import PyObjectId

class SalonBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str = Field(...)
    openHour: int = Field(...)
    closeHour: int = Field(...)
    imageUrl: str = Field(...)
    appointment: bool  = Field(...)
    rating: str = Field(...)
    available: bool = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
              "name": "Beautify Salon",
              "openHour": 570,
              "closeHour": 1080,
              "imageUrl": "https://beuhairsalon.com/wp-content/uploads/2017/09/beuhair-interior-3-min-cropped.jpg",
              "appointment": True,
              "rating": "4.2",
              "available": True
            }
        }
        