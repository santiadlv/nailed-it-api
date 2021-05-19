from bson.objectid import ObjectId
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
    description: str = Field(...)
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
                "description": "A shellac manicure is the perfect version of a regular manicure.  It is a dry manicure that includes all of the basics of a regular manicure.   Your nails are cleaned up, the skin around your nails is pampered, and last of all a polish is applied to the nail with exactness.  However, the process of application is uniquely different. Instead of applying a nail polish that is bound to chip, scratch, or peel, a Shellac manicure is a polish/gel product that when cured under a UV lamp hardens and lasts.",
                "salon_id": "6085df4104159a9c9c81b968"
            }
        }
        