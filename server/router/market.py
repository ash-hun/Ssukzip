from fastapi import APIRouter
from fastapi import Depends, FastAPI, HTTPException
from starlette.config import Config
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, sessionmaker
from requests.structures import CaseInsensitiveDict
from fastapi.security import OAuth2PasswordBearer

import jwt, requests, crud, auth, models, database, marketcrud, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/market/create")
async def createMarket(market : schemas.Market, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    return marketcrud.create_market(db=db, market=market)

@router.get("/market/info/{market_id}")
async def getMarket(market_id : int, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    return marketcrud.create_market(db=db, market_id=market_id)

@router.put("/market/update")
async def updateMarket(market : schemas.Market, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    return marketcrud.update_market(db=db, market=market)

@router.delete("/reivew/delete/{market_id}")
async def deleteMarket(market_id : int, token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    return marketcrud.delete_market(db=db, market_id=market_id)