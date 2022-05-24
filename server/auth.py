from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from starlette.config import Config
from requests.structures import CaseInsensitiveDict
from jwt import encode, decode
from urllib import parse
import models, schemas
import database, requests

config = Config('.env')
#구글 토큰 얻어오기
def get_google_token(code:str):
    print(config)
    url = "https://oauth2.googleapis.com/token"
    data={
    'code': code,
    'client_id':config('GOOGLE_CLIENT_ID', default=None),
    'client_secret': config('GOOGLE_CLIENT_SECRET', default=None),
    'redirect_uri':'http://localhost:8000/auth',
    'grant_type':'authorization_code'
    }

    resp = requests.post(url, data=data)
    token_info = resp.json()
    return token_info

#카카오 토큰 얻어오기
def get_kakao_token(code:str):
    code = parse.urlparse(code)
    print(code.path)
    url = "https://kauth.kakao.com/oauth/token"
    data={
    'code': code.path,
    'client_id':config('KAKAO_CLIENT_ID', default=None),
    'redirect_uri':'http://localhost:8000/auth/kakao',
    'grant_type':'authorization_code'
    }

    resp = requests.post(url, data=data)
    token_info = resp.json()

    return token_info


# 토큰으로 유저 정보 얻어오기
def get_user_info_by_token(url:str, access_token:str):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + access_token
    resp = requests.get(url, headers=headers)
    profile = resp.json()
    print("google api 프로필 정보 호출")
    return profile


def generate_token(user_email :str):
    email = user_email
    now = datetime.now()

    token = {
        'exp': now + timedelta(days=14),
        'iat': now,
        'token_type': 'access',
        'user_email': email
    }
    print("jwt 토큰 생성 완료")
    return{
        'access_token': encode(token,'secrett')
    }

def verify_jwttoken(token:str):
    try:
        token_info = decode(token, key='secrett', algorithms='HS256')

        now = int(datetime.now().timestamp())
        print(token_info['exp'])
        if(token_info['exp'] < now):
            print('로그아웃 되었습니다.')
            return False;
        else:
            return token_info['user_email']
    except Exception as e:
        return False;