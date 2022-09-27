# main 실행 파일
from PyQt5 import uic
from PyQt5.QtWidgets import *
import pandas as pd
import os
import sys
import time
from selenium import webdriver
from Crawling_for_CSV import Find_Store
from Crawling import Make_DataFrame
from data_preprocessing import data_frame
from sentiment_model import Sentiment

# 파일 불러오는 함수 생성
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#################main.ui 가져오기#######################
form = resource_path('main.ui')
form_class1 = uic.loadUiType(form)[0]
#############Second_Choice_Page.ui 가져오기#############
form2 = resource_path('Second_Choice_Page.ui')
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

class Second_Window(QDialog, QWidget, form_class2):

    def __init__(self, sname):
        super(Second_Window, self).__init__()
        self.setupUi(self)
        self.start_GP(sname)
        self.show()
        self.make_df()

    def start_GP(self, sname):
        FS = Find_Store()
        FS.play(sname)

    def detail_1_store(self):
        print('1')

    def detail_2_store(self):
        print('2')

    def detail_3_store(self):
        print('3')

    def detail_4_store(self):
        print('4')

    def detail_5_store(self):
        print('5')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = Main_Window()  # 첫 화면 class 명 입력
    main_dialog.show()
    QApplication.processEvents()
    app.exit(app.exec_())