from sqlalchemy.orm import Session
import models, schemas
import database
from fastapi import FastAPI, Response, status


def create_user(db: Session, user: schemas.User):
    try:
        db_user = models.User(email=user.email, name=user.name, nickname= user.nickname, token = user.token, img_url = user.img_url)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {'msg': "추가되었습니다."}
    except Exception as e:
        return {'msg': e}

def get_user(db: Session, user_id: int):
   try:
        user = db.query(models.User).filter(models.User.id == User_id).first()
        if(user):
            return user
        return
   except Exception as e:
        return {'msg': e}


def get_user_by_email(db: Session, email: str):
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if(user):
            return user
        else:
            return {'msg': "해당 유저는 존재하지 않습니다."}
    except Exception as e:
        return {'msg': e}


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user_token(db: Session, email:str, token: str):
    try:
        user_update = db.query(models.User).filter_by(email = email).first()
        if(user_update):
            user_update.token = token
            db.add(user_update)
            db.commit()
        else:
            return
    except Exception as e:
        return {'msg': e}

def delete_user(response: Response, db: Session, email: str):
    try:
        user = db.query(models.User).filter_by(email=email).first()
        if(user):
            db.delete(user)
            db.commit()
        else:
            response.status_code = status_code.HTTP_204_NOCONTENT
            return {'msg': "해당 유저는 존재하지 않습니다."}

        return {'msg': "삭제되었습니다."}
    except Exception as e:
        response.status_code = status_code.HTTP_409_CONFLICT
        return {'msg': e}

def update_user_nickname(response: Response, db: Session, email: str, nickname: str):
    try:
        user = db.query(models.User).filter_by(email=email).first()
        if(user):
            user.nickname = nickname
            db.add(user)
            db.commit()
        else:
            response.status_code = status_code.HTTP_204_NOCONTENT
            return {'msg': "해당 유저는 존재하지 않습니다."}

        return {'msg': "수정되었습니다."}
    except Exception as e:
        response.status_code = status.HTTP_409_CONFLICT
        return {'msg': e}


