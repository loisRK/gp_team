# main 실행 파일
import re
from PyQt5 import uic
from PyQt5.QtWidgets import *
import os
import sys
from Crawling_for_CSV import Find_Store
from matplotlib_font import font_setting


font_setting()

# 파일 불러오는 함수 생성
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


################# main.ui 가져오기 #######################
form = resource_path('main.ui')
form_class1 = uic.loadUiType(form)[0]


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
        self.start_GP(store_name)

    def display(self):
        self.show()

    def start_GP(self, sname):
        FS = Find_Store()
        FS.play(sname)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = Main_Window()  # 첫 화면 class 명 입력
    main_dialog.show()
    QApplication.processEvents()
    app.exit(app.exec_())