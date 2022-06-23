"""
본 modulingTest.py은 importing test를 한것이라 신경쓰지 않아도 됩니다.
타 파이썬 파일에서 사용하실때 본 내용 그대로 가져가시면 됩니다!
"""

from silence_tensorflow import silence_tensorflow
silence_tensorflow()
from korcen import korcen
import prediction as ssukzip


if __name__ == "__main__":
    review = input("Your Review : ")
    korcen = korcen.korcen()
    score = ssukzip.classifyReview("ssukzip_Model.h5", review, korcen)
    print(score)