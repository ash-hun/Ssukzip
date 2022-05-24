from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status
import models, schemas
import database

from sqlalchemy.orm import Session
import models, schemas
import database

def create_review(response: Response, db: Session, review = schemas.Review):
    try:
        db_review = models.Review(user_id = review.user_id, market_id = review.market_id, rate=review.rate, comment=review.comment, solution=review.solution)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return {'msg': "추가되었습니다."}
    except Exception as e:
        response.status_code = HTTP_409_CONFLICT
        return {'msg': "e"}

def update_review(response: Response, db: Session, review = schemas.Review):
    try:
        cur_review = db.query(models.Review).filter_by(id=review.id).first()
        if(review):
            cur_review.rate=review.rate
            cur_review.comment=review.comment
            cur_review.solution=review.solution
            db.add(cur_review)
            db.commit()
            db.refresh(cur_review)
            return {'msg': "수정되었습니다."}
        else:
            response.status_code = status.HTTP_204_NOCONTENT
            return {'msg': "해당 리뷰는 존재하지 않습니다."}
    except Exception as e:
        return {'msg': e}

def delete_review(response: Response, db: Session, review_id:int):
    try:
        review = db.query(models.Review).filter_by(id=review_id).first()
        if(review):
            db.delete(review)
            db.commit()
        else:
            response.status_code = status_code.HTTP_204_NOCONTENT
            return {'msg': "해당 리뷰는 존재하지 않습니다."}

        return {'msg': "삭제되었습니다."}
    except Exception as e:
        return {'msg': e}

def get_review(response: Response, db: Session, review_id: int):
    try:
        review = db.query(models.Review).filter(models.Review.id == review_id).first()
        if(review):
            return review
        else:
            return {'msg': "해당 리뷰는 존재하지 않습니다."}
    except Exception as e:
        response.status_code = status.HTTP_409_CONFLICT
        return {'msg': e}