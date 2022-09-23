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

#################main.ui 가져오기#######################
form = resource_path('main.ui')
form_class1 = uic.loadUiType(form)[0]
#################Page_Gui_Test.ui 가져오기#######################
form2 = resource_path('content.ui')
form_class2 = uic.loadUiType(form2)[0]

class auto_main(QMainWindow, form_class1):
    # global store_name
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.show()

        self.Input_Store.setText('음식점 이름을 입력하세요.')
        self.Find_Store_Btn.clicked.connect(self.get_store)
        self.Find_Store_Btn.clicked.connect(self.initUi)

    def get_store(self):
        global store_name
        store_name = self.Input_Store.text()

    def initUi(self):
        # 크롤링 코드에 입력 값 넣어줌
        FS = Find_Store2()
        FS.play(store_name)
        self.hide() # 메인 윈도우 숨김
        self.second = auto_w()
        self.second.exec()      # 두 번째 창 닫을 때 까지 기다림
        self.show()


class auto_w(QWidget,form_class2):      # class name 변경
    def __init__(self):
        super(auto_w, self).__init__()
        self.setupUi(self)
        self.show()
        self.start_GP()

    # 실행에 필요한 모든 코드들은 전부 start() 함수에 모두 삽입
    def start_GP(self):
        FS = Find_Store2()

        # GUI : 빈칸 채우기 반환값
        self.Store_Name.setText(FS.Store_Name)    # GUI: 가게이름
        self.Review_Count_total.setText(FS.Comment_Total)   # GUI: Total Comment
        self.Star_Total.setText(FS.Star_Total)  # GUI: 총 평점

        review, menu, star_t, star_opt = FS.print_review()
        # review = data_frame()
        # review.review_pre(review)
        # review.menu_pre(menu)
        # review.star_pre(star_t)
        #
        # review.make_csv(review, menu, star_t, star_opt)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = auto_main() #해당부분 위 class name과 동일하게 작성
    main_dialog.show()
    QApplication.processEvents()
    app.exit(app.exec_())