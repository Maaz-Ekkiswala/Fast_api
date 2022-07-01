from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette import status

from app.user import schemas, crud
from app.user.crud import verify_password
from app.user.models import User
from app.user.schemas import UserOut, UserAuth, TokenSchema
from db.depandency import get_db


user_router = APIRouter(tags=["Login"])
denylist = set()


@user_router.post('/signup/', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth, db_user: Session = Depends(get_db)):
    # querying database to check if user already exist
    user = db_user.query(User).filter(User.email == data.email, User.username == data.username).first()
    print(user)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email OR username already exist"
        )

    return crud.create_user(db=db_user, user=data)


@user_router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(login_u: schemas.Login, authorize: AuthJWT = Depends(), db_user: Session = Depends(get_db)):
    user = db_user.query(User).filter(User.username == login_u.username).first()
    print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username"
        )
    access_token = authorize.create_access_token(subject=user.id, fresh=True)
    refresh_token = authorize.create_refresh_token(subject=user.id)
    hashed_pass = user.password
    if not verify_password(login_u.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": access_token, "refresh_token": refresh_token
    }


@user_router.post('/refresh')
def refresh(authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    print(current_user)
    new_access_token = authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@user_router.delete('/access-revoke')
def access_revoke(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    jti = authorize.get_raw_jwt()['jti']
    print(authorize.get_raw_jwt())
    denylist.add(jti)
    return {"detail": "Access token has been revoke"}
