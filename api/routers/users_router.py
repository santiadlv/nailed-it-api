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
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"messsage" : "User added successfully", "data" : new_user})

@router.post("/reset", status_code=status.HTTP_202_ACCEPTED, response_description="Get reset password link")
async def get_reset_link(request: Request, user_in: user_model.UserBase) -> JSONResponse:
    user_in = jsonable_encoder(user_in)
    user_to_reset = await UserService.get_user_by_email(request, user_in)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
    content={"messsage" : "Token generated successfully", "token" : user_to_reset['_id']})

@router.post("/reset/token", status_code=status.HTTP_200_OK, response_description="Reset user password")
async def reset_password(request: Request, credentials: user_model.UserCredentials) -> JSONResponse:
    credentials = jsonable_encoder(credentials)
    reset_user = await UserService.update_password(request, credentials)
    return JSONResponse(status_code=status.HTTP_200_OK,
    content={"message" : "Resource updated successfully.", "data" : reset_user})

@router.post("/login", status_code=status.HTTP_200_OK, response_description="User Login")
async def validate_user(request: Request, user_login: user_model.UserLogin) -> JSONResponse:
    user_login = jsonable_encoder(user_login)
    validate_password = await UserService.login(request, user_login)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"messsage" : "Login Succesful", "data" : validate_password})
