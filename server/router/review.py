from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException
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

@router.post("/review/create")
async def createReview(review : schemas.Review, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    email = auth.verify_jwttoken(token)
    user_id = crud.get_user_by_email(db=db, email = email).id
    return reviewcrud.create_review(db=db, review = review)

@router.get("/review/info/{review_id}")
async def getReview(review_id : int, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    return reviewcrud.get_review(db=db, review_id=review_id)

@router.put("/review/update")
async def UpdateReview(review : schemas.Review, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    return reviewcrud.update_review(db=db, review=review)

@router.delete("/review/delete/{review_id}")
async def deleteReview(review_id : int, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    return reviewcrud.delete_review(db=db, review_id=review_id)