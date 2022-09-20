# -- coding: utf-8 --

import sys

from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Page_Gui_Test import Ui_MainWindow #앞의 파일명 동일 kinwriter_python 만 변경
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver
import time
import pyperclip
from bs4 import BeautifulSoup
import pyautogui
from Crawling_Store import Find_Store

class auto_w(QMainWindow,Ui_MainWindow): #class name 변경
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.show()

    # 실행에 필요한 모든 코드들은 전부 start() 함수에 모두 삽입
    def start(self):

        FS = Find_Store()
        FS.play(self.Input_Store.text())



app =QApplication([])
main_dialog = auto_w() #해당부분 위 class name과 동일하게 작성
QApplication.processEvents()
app.exit(app.exec_())