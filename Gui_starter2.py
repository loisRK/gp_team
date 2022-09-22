# bs4 crawling 실행 파일
# -- coding: utf-8 --

from PyQt5.QtWidgets import *
from Page_Gui_Test import Ui_MainWindow #앞의 파일명 동일 kinwriter_python 만 변경
from crawling_bs4 import Find_Store2
from data_preprocessing import data_frame


class auto_w(QMainWindow,Ui_MainWindow): #class name 변경
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



        # review_l, review_s, review_m = FS.print_review()

        # review = data_frame()
        # review.review_pre(review_l)
        # review.star_pre(review_s)
        # review.menu_pre(review_m)
        # review.make_csv(review_l, review_s, review_m)


app = QApplication([])
main_dialog = auto_w() #해당부분 위 class name과 동일하게 작성
QApplication.processEvents()
app.exit(app.exec_())