from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException
from starlette.config import Config
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, sessionmaker
from requests.structures import CaseInsensitiveDict
from fastapi.security import OAuth2PasswordBearer

import jwt, requests, crud, auth, models, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()
config = Config('.env')

@router.get("/auth")
async def signUpGoogle(code:str, db: Session = Depends(get_db)):
    token_info = auth.get_google_token(code)
    access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']

    #유저정보 가지고오기기
    url = "https://www.googleapis.com/oauth2/v1/userinfo"
    profile = auth.get_user_info_by_token(url, access_token)

    # db 생성
    user = models.User()
    user.email = profile['email']
    user.name = profile['name']
    user.nickname = profile['name']
    user.token = refresh_token
    user.img_url = profile['picture']

    if crud.get_user_by_email(db = db, email = profile['email']) :
        crud.update_user_token(db = db, email = user.email,token = refresh_token)

    else :
        crud.create_user(db=db, user=user)

    jwt_token = auth.generate_token(user.email)

    return JSONResponse(content=jwt_token)

@router.get("/auth/kakao")
async def signUpKakao(code:str, db: Session = Depends(get_db)):

    token_info = auth.get_kakao_token(code)
    access_token = token_info['access_token']
    refresh_token = token_info['refresh_token']
    print("토큰 발급 완료" + access_token)

    #유저 정보 가지고 오기
    url = 'https://kapi.kakao.com/v2/user/me'
    user_info = auth.get_user_info_by_token(url, access_token)['kakao_account']
    print(user_info)

    #회원 가입
    user = models.User()
    user.email = user_info['email']
    user.name = user_info['profile']['nickname']
    user.nickname = user_info['profile']['nickname']
    user.token = refresh_token
    user.img_url = user_info['profile']['profile_image_url']

    if crud.get_user_by_email(db = db, email = user.email) :
        crud.update_user_token(db = db, email = user.email, token = user.token)
    else :
        crud.create_user(db=db, user=user)

    jwt_token = auth.generate_token(user.email)

    auth.verify_jwttoken(jwt_token['access_token'])

    return JSONResponse(content=jwt_token)

# @router.get("/auth/kakao/logout")
# async def logoutKakao(token: str = Depends(oauth2_scheme)):
#     info_url = "https://kapi.kakao.com/v1/user/logout"
#     headers = CaseInsensitiveDict()
#     headers["Accept"] = "application/json"
#     headers["Authorization"] = "Bearer " + token
#     resp = requests.post(info_url, headers=headers)
#
# @router.get("/auth/google/logout")
# async def logoutGoogle(token: str = Depends(oauth2_scheme)):
#     info_url = "https://accounts.google.com/o/oauth2/revoke?token=" +token
#     resp = requests.post(info_url)
#     return JSONResponse(resp.json())


@router.get("/user/me")
async def getMyInfo(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    email = auth.verify_jwttoken(token)

    return crud.get_user_by_email(db= db, email = email)

@router.delete("/user/delete", status_code=201)
async def deleteUser(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    email = auth.verify_jwttoken(token)

    return JSONResponse(content= crud.delete_user(db = db, email = email))

@router.put("/user/update/nickname", status_code=201)
async def updateNickname(nickname:str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    email = auth.verify_jwttoken(token)
    result = crud.update_user_nickname(db = db, email = email, nickname = nickname)
    return result