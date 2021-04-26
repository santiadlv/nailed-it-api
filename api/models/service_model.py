from bson.objectid import ObjectId
from decimal import Decimal
from pydantic import BaseModel, Field
from .objectid_model import PyObjectId

class ServiceBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str = Field(...)
    estimatedTimeLower: int = Field(...)
    estimatedTimeHigher: int = Field(...)
    imageUrl: str = Field(...)
    price: str = Field(...)
    rating: str = Field(...)
    salon_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Nail Cleaning and Shellac",
                "estimatedTimeLower": 15,
                "estimatedTimeHigher": 30,
                "imageUrl": "https://www.nenha.com/wp-content/uploads/2017/08/lateral-nail-art.png",
                "price": "200.00",
                "rating": "4.1",
                "salon_id": "6085df4104159a9c9c81b968"
            }
        }
        