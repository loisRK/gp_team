# -- coding: utf-8 --

from PyQt5.QtWidgets import *
from Page_Gui_Test import Ui_MainWindow #앞의 파일명 동일 kinwriter_python 만 변경
from Crawling_Store import Find_Store
from data_preprocessing import data_frame
from sentiment_model import Sentiment
import pandas as pd

class auto_w(QMainWindow,Ui_MainWindow): #class name 변경
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.show()

    # 실행에 필요한 모든 코드들은 전부 start() 함수에 모두 삽입
    def start(self):

        FS = Find_Store()
        FS.play(self.Input_Store.text())
        review_l, review_s, review_m = FS.print_review()

        review = data_frame()
        review.review_pre(review_l)
        review.star_pre(review_s)
        review.menu_pre(review_m)
        review.make_csv(review_l, review_s, review_m)

        # 모델 실행
        model = Sentiment()
        review_sample = pd.DataFrame(review_l, columns=['review'])
        print("Model predicting...")
        output = model.get_score(review_sample)
        print("********** 모델 결과 ***********")
        print(output)
        print("*******************************")

app = QApplication([])
main_dialog = auto_w() #해당부분 위 class name과 동일하게 작성
QApplication.processEvents()
app.exit(app.exec_())
