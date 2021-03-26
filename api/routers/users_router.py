from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import user_model
from ..services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description" : "Not found"}}
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_description="Create new user", response_model=user_model.UserInDB)
async def create_user(request: Request, user_in: user_model.UserCreate) -> JSONResponse:
    user_in = jsonable_encoder(user_in)
    new_user = await UserService.create(request, user_in)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message" : "User added successfully", "data" : new_user})