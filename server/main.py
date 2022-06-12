from typing import List
from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session, sessionmaker
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm.session
import requests
import jwt
import json

import models, database, schemas, crud
from router import oauth,review,market


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(oauth.router)
app.include_router(review.router)
app.include_router(market.router)


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
