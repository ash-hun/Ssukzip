from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException,status, Response
from starlette.config import Config
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, sessionmaker
from requests.structures import CaseInsensitiveDict
from fastapi.security import OAuth2PasswordBearer

import jwt, requests, crud, auth, models, database, reviewcrud, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/review/create", status_code=200)
async def createReview(response: Response, review : schemas.Review, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    if(auth.verify_jwttoken(token)):
        email = auth.verify_jwttoken(token)
        print(email)
        user = crud.get_user_by_email(db=db, email = email)
        print(user)
        return reviewcrud.create_review(response=response, db=db, review = review, user_id = user.id, user_nickname=user.nickname)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"msg": "인증/재인증이 필요합니다."}

@router.get("/review/info/{market_id}", status_code=200)
async def getReview(response: Response, market_id : str, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    if(auth.verify_jwttoken(token)):
        return reviewcrud.get_review_by_marketid(response=response, db=db, market_id=market_id)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"msg" : "인증/재인증이 필요합니다."}

@router.get("/review/myinfo", status_code=200)
async def getReviewByMe(response: Response, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    if(auth.verify_jwttoken(token)):
        email = auth.verify_jwttoken(token)
        user = crud.get_user_by_email(db=db, email = email)
        print(user.nickname)
        return reviewcrud.get_review_by_userid(response=response, db=db, user_id=user.id)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"msg" : "인증/재인증이 필요합니다."}

@router.put("/review/update", status_code=200)
async def UpdateReview(response: Response, review : schemas.Review, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    if(auth.verify_jwttoken(token)):
        return reviewcrud.update_review(response=response, db=db, review=review)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"msg" : "인증/재인증이 필요합니다."}

@router.delete("/review/delete/{review_id}", status_code= 200)
async def deleteReview(response: Response, review_id : int, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    if(auth.verify_jwttoken(token)):
        return reviewcrud.delete_review(response=response, db=db, review_id=review_id)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"msg" : "인증/재인증이 필요합니다."}

@router.get("/review/recommend/{review_id}", status_code= 200)
async def recommendReview(response: Response, review_id : int, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    if(auth.verify_jwttoken(token)):
        return reviewcrud.recommend_review(response=response, db=db, review_id=review_id)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"msg" : "인증/재인증이 필요합니다."}