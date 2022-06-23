from sqlalchemy.orm import Session
import models, schemas
import database

def create_market(db: Session, review = schemas.Market):
    try:
        db_market = models.Review(market_name = market.market_name, market_latitude = market.market_latitude, market_longitude=maket.market_longitude, phone=market.phone)
        db.add(db_market)
        db.commit()
        db.refresh(db_market)
        return {'msg': "추가되었습니다."}
    except Exception as e:
        return {'msg': e}

def update_market(db: Session, market = schemas.Market):
    try:
        cur_market = db.query(models.Market).filter_by(id=market.id).first()
        if(review):
            cur_market.market_name=market.market_name
            cur_market.market_latitude=market.market_latitude
            cur_market.market_longitude=market.market_longitude
            cur_market.phone=market.phone
            db.add(cur_market)
            db.commit()
            db.refresh(cur_market)
            return {'msg': "수정되었습니다."}
        else:
            return {'msg': "해당 가게는 존재하지 않습니다."}
    except Exception as e:
        return {'msg': e}

def delete_market(db: Session, market_id:int):
    try:
        market = db.query(models.Market).filter_by(id=market_id).first()
        if(market):
            db.delete(market)
            db.commit()
        else:
            return {'msg': "해당 가게는 존재하지 않습니다."}

        return {'msg': "삭제되었습니다."}
    except Exception as e:
        return {'msg': e}

def get_market(db: Session, market_id: int):
    try:
        review = db.query(models.Market).filter(models.Market.id == market_id).first()
        if(market):
            return market
        else:
            return {'msg': "해당 가게는 존재하지 않습니다."}
    except Exception as e:
        return {'msg': e}