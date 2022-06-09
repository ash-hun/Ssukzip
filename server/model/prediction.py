from silence_tensorflow import silence_tensorflow
silence_tensorflow()
from model import ssukzip_modelGenerator as mm
from konlpy.tag import Okt
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model
from korcen import korcen
import numpy as np
import json
import os
import nltk

def classifyReview(modelName, review, korcenModule):
    """
    This function roles to predict what sentence is positive or negative.
    In professsional parts, it calls "Sentiment-Analysis"

    :param review: When a customer write a review on our application, it goes through this function to check if it is a proper review.
    :return res: Returns the result of determining whether param is an appropriate review.
    """
    state = korcenModule.check(review)
    # print(f"=========================\nkorcen check : {state}\n=========================")
    if (not state):
        okt = Okt()
        model = load_model(modelName)
        train_data = mm.read_data('ratings_train.txt')
        test_data = mm.read_data('ratings_test.txt')

        token = ['/'.join(t) for t in okt.pos(review, norm=True, stem=True)]

        if os.path.isfile('train_docs.json'):
            with open('train_docs.json', encoding="utf-8") as f:
                train_docs = json.load(f)
            with open('test_docs.json', encoding="utf-8") as f:
                test_docs = json.load(f)
        else:
            train_docs = [(mm.tokenize(row[1]), row[2]) for row in train_data]
            test_docs = [(mm.tokenize(row[1]), row[2]) for row in test_data]
            # JSON 파일로 저장
            with open('train_docs.json', 'w', encoding="utf-8") as make_file:
                json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")
            with open('test_docs.json', 'w', encoding="utf-8") as make_file:
                json.dump(test_docs, make_file, ensure_ascii=False, indent="\t")
        # plot_model(model, to_file='./ssukzip_model_shapes.png', show_shapes=True)
        tokens = [t for d in train_docs for t in d[0]]
        text = nltk.Text(tokens, name='NMSC')

        # 시간이 꽤 걸립니다! 시간을 절약하고 싶으면 most_common의 매개변수를 줄여보세요.
        selected_words = [f[0] for f in text.vocab().most_common(10000)]

        tf = [token.count(word) for word in selected_words]
        data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)

        score = float(model.predict(data))

        if (score > 0.5):
            res = f"[{review}]는 {score * 100}% 확률로 긍정 리뷰이지 않을까 추측해봅니다.^^\n"
        else:
            res = f"[{review}]는 {(1 - score) * 100}% 확률로 부정 리뷰이지 않을까 추측해봅니다.^^\n"

        return res
    else:
        return "해당 리뷰는 비속어가 감지되었습니다!"

if __name__ == "__main__":
    review = input("Your Review : ")
    korcen = korcen.korcen()
    score = classifyReview("ssukzip_Model.h5", review, korcen)
    print(score)
