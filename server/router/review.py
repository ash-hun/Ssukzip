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
        user_id = crud.get_user_by_email(db=db, email = email).id
        return reviewcrud.create_review(response=response, db=db, review = review)
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"msg": "인증/재인증이 필요합니다."}

@router.get("/review/info/{review_id}", status_code=200)
async def getReview(response: Response, review_id : int, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    if(auth.verify_jwttoken(token)):
        return reviewcrud.get_review(response=response, db=db, review_id=review_id)
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
        response.status_code = status_code.HTTP_401_UNAUTHORIZED
        return {"msg" : "인증/재인증이 필요합니다."}