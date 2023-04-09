
from ssukzip_modelGenerator import predict_pos_neg
from konlpy.tag import Okt
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model
from korcen import korcen

def classifyReview(modelName, review, korcenModule):
    state = korcenModule.check(review)
    if not state:
        model = load_model(modelName)
        plot_model(model, to_file='./ssukzip_model_shapes.png', show_shapes=True)
        return predict_pos_neg(model, review)
    else:
        return "해당 리뷰는 비속어가 포함되어있습니다."

if __name__ == "__main__":
    review = input("Your Review : ")
    korcen = korcen.korcen()
    score = classifyReview("ssukzip_Model.h5", review, korcen)
    # print(score)
