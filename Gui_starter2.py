# main 실행 파일
from PyQt5 import uic
from PyQt5.QtWidgets import *
from crawling_bs4 import Find_Store2
import os
import sys
from data_preprocessing import data_frame

from sentiment_model import Sentiment
import pandas as pd


# 파일 불러오는 함수 생성
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


#################main.ui 가져오기#######################
form = resource_path('main.ui')
form_class1 = uic.loadUiType(form)[0]
#################Page_Gui_Test.ui 가져오기##############
form2 = resource_path('content.ui')
form_class2 = uic.loadUiType(form2)[0]


class Main_Window(QMainWindow, form_class1):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Input_Store.setText('음식점 이름을 입력하세요.')
        self.Find_Store_Btn.clicked.connect(self.get_store)
        self.Find_Store_Btn.clicked.connect(self.display)

    def get_store(self):
        global store_name
        store_name = self.Input_Store.text()

    def display(self):
        self.hide()  # 메인 윈도우 숨김
        self.second = Second_Window(store_name)
        self.second.exec()  # 두 번째 창 닫을 때 까지 기다림
        self.show()


class Second_Window(QDialog, QWidget, form_class2):  # class name 변경
    def __init__(self, sname):
        super(Second_Window, self).__init__()
        self.setupUi(self)
        self.start_GP(sname)
        self.show()

    # 크롤링 정보 전달 -> 전처리 및 데이터 시각화, 모델링
    def start_GP(self, sname):
        FS = Find_Store2()
        FS.play(sname)

        # GUI : 빈칸 채우기 반환값
        self.Store_Name.setText(sname)  # GUI: 가게이름
        print('fs.storename:',sname)
        self.Review_Count_total.setText(FS.Comment_Total)  # GUI: Total Comment
        print('fs.comment_total', FS.Comment_Total)
        self.Star_Total.setText(FS.Star_Total)  # GUI: 총 평점
        print('fs.star_total', FS.Star_Total)

        review, menu, star_t, star_opt = FS.print_review()
        print('review:',review)
        print('menu:',menu)
        print('star_t:',star_t)
        print('star_opt:',star_opt)
        rv = data_frame()
        rv.review_pre(review)
        # rv.menu_pre(menu)
        # rv.star_pre(star_t)
        #
        # rv.make_csv(review, menu, star_t, star_opt)

        # 모델 실행
        model = Sentiment()
        review_sample = pd.DataFrame(review, columns=['review'])
        print("Model predicting...")
        output = model.get_score(review_sample)
        print("********** 모델 결과 ***********")
        print(output)
        print("*******************************")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = Main_Window()  # 첫 화면 class 명 입력
    main_dialog.show()
    QApplication.processEvents()
    app.exit(app.exec_())
