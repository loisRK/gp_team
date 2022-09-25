# bs4 crawling 실행 파일
# -- coding: utf-8 --
from PyQt5 import uic
from PyQt5.QtWidgets import *
# from Page_Gui_Test import Ui_MainWindow #앞의 파일명 동일 kinwriter_python 만 변경
from crawling_bs4 import Find_Store2
import os
import sys
from data_preprocessing import data_frame

# 파일 불러오는 함수 생성
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#################Page_Gui_Test.ui 가져오기#######################
form = resource_path('Page_Gui_Test.ui')
form_class = uic.loadUiType(form)[0]


class auto_w(QMainWindow,form_class): #class name 변경
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.show()

    # 실행에 필요한 모든 코드들은 전부 start() 함수에 모두 삽입
    def start(self):

        FS = Find_Store2()
        FS.play(self.Input_Store.text())

        # GUI : 빈칸 채우기 반환값
        self.Store_Name.setText(FS.Store_Name)    # GUI: 가게이름
        self.Review_Count_total.setText(FS.Comment_Total)   # GUI: Total Comment
        self.Star_Total.setText(FS.Star_Total)  # GUI: 총 평점

        review, menu, star_t, star_opt = FS.print_review()
        print(review)
        print(menu)
        print(star_t)
        print(star_opt)

        review = data_frame()
        # review.review_pre(review)
        # review.menu_pre(menu)
        review.star_pre(star_t)

        # review.make_csv(review, menu, star_t, star_opt)


app = QApplication([])
main_dialog = auto_w() #해당부분 위 class name과 동일하게 작성
QApplication.processEvents()
app.exit(app.exec_())