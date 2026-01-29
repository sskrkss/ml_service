from fastapi import APIRouter, status, Depends

from database.database import get_session
from services.auth_service import AuthService

auth_route = APIRouter()


# TODO: токены сразу выдаем (в куке?)
# TODO: принимать request dto с валидацией длины, формата email
@auth_route.post(
    '/sign-up',
    status_code=status.HTTP_200_OK,
    summary="User registration"
)
async def sign_up(email: str, username: str, password: str, session=Depends(get_session)) -> None:
    auth_service = AuthService(session)
    auth_service.sign_up(email=email, username=username, password=password)

    pass


# TODO: токены сразу выдаем (в куке?)
@auth_route.post(
    '/sign-in',
    status_code=status.HTTP_200_OK,
    summary="User sign-in"
)
async def sign_in(emailOrUsername: str, password: str, session=Depends(get_session)) -> None:
    pass


# TODO: чистим куки или что там будет
@auth_route.post(
    '/sign-out',
    status_code=status.HTTP_200_OK,
    summary="User sign-out"
)
async def sign_out(session=Depends(get_session)):
    pass


# TODO: взять refresh_token из куки или что там будет
@auth_route.post(
    "/refresh-token",
    status_code=status.HTTP_200_OK,
    summary="Refresh user's access token"
)
async def refresh_token(session=Depends(get_session)) -> None:
    pass
