from typing import List
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session, sessionmaker

import sqlalchemy.orm.session
import requests
import jwt
import json

import models
import database
import schemas
import crud


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#oauth
@app.get('/auth/google')
async def google_auth(code: str):
    code = parse.urlparse(code)
    print(code.path)
    url = "https://oauth2.googleapis.com/token"
    data={
    'code': code.path,
    'client_id':'',
    'client_secret': '',
    'redirect_uri':'',
    'grant_type':''
    }

    resp = request.post(url, data=data)
    token = {'token' : resp.json()['id_token']}
    print(token)
#     profile = jwt.decode(token,options={"verify_signature": False})
    return JSONResponse(content=token)



"""
@app.post("/users",response_model=schemas.User)
def create_user2(user:schemas.UserCreate, db: Session = Depends(get_db)): # 무조건 typing을 해줘야 에러가 발생하지 않음
    db_user = crud.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/user/{user_email}", response_model=schemas.User)
def get_user(user_email: str, db: Session = Depends(get_db)):
    return crud.get_user_by_email(db=db,email=user_email) """
