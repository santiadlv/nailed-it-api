from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from .objectid_model import PyObjectId

class ReviewBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    title: str = Field(...)
    date: str = Field(...)
    reviewDescription: str = Field(...)
    salon_id: str = Field(...)
    user_id: str = Field(...)
    service_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Excellent Service",
                "date": "1998-09-05",
                "reviewDescription": "Excellent service. Loved my shellac and the color.",
                "salon_id": "6085d9afd9827ab0f5273e3b",
                "user_id": "605cd9ca1ec4bf19fe3f9581",
                "service_id": "60860830041aa13d76554242"
            }
        }