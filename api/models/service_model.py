from bson.objectid import ObjectId
from pydantic import BaseModel, Field, validator
from .objectid_model import PyObjectId

service_categories_list = ["Nails", "Haircutting, coloring and styling", "Tanning", "Massages", "Hair removal", "Makeup", "Skin care", "Cosmetic beauty", "Complementary care"]

class ServiceBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str = Field(...)
    estimatedTimeLower: int = Field(...)
    estimatedTimeHigher: int = Field(...)
    imageUrl: str = Field(...)
    price: str = Field(...)
    rating: str = Field(...)
    description: str = Field(...)
    category: str = Field(...)
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
                "category": "Nail treatments",
                "salon_id": "6085df4104159a9c9c81b968"
            }
        }

class ServiceIdentifier(BaseModel):
    id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "608608d7041aa13d76554244"
            }
        }

class ServiceCategory(BaseModel):
    categories: list = Field(...)

    @validator('categories')
    def check_valid_category(cls, v):
        for category in v:
            assert category in service_categories_list, f"Category '{category}' does not exist"
        return v

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "categories": service_categories_list
            }
        }
