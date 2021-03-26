from fastapi import APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..models import user_model
from ..models import login_model
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
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"messsage" : "User added successfully", "data" : new_user})

@router.post("/login", status_code=status.HTTP_200_OK, response_description="User Login", response_model=login_model.UserLogin)
async def validate_user(request: Request, user_login: login_model.UserCheck) -> JSONResponse:
    user_login = jsonable_encoder(user_login)
    validate_password = await UserService.login(request, user_login)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"messsage" : "Login Succesful", "data" : validate_password})