from fastapi import APIRouter, status, Response
from ..models import user_model
from ..services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description" : "Not found"}}
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=user_model.UserGet)
async def create_user(user_in: user_model.UserCreate, response: Response):
    created_user = UserService.create(user_in=user_in)
    if not created_user:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return create_user