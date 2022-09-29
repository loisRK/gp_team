# 데이터 전처리 코드 메인 통합 버전
# main 실행 파일
import math
import os
import sys

from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *

# 데이터 전처리, 모델 학습 관련
import pandas as pd
import numpy as np
from math import pi
from matplotlib_font import font_setting
import re
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sentiment_model import Sentiment


# 크롤링 모듈
from crawling_bs4 import Find_Store2

font_setting()


# 파일 불러오는 함수 생성
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


#################main.ui 가져오기#######################
form = resource_path('main.ui')
form_class1 = uic.loadUiType(form)[0]
#################content.ui 가져오기##############
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
        self.second = Second_Window()
        self.second.exec()  # 두 번째 창 닫을 때 까지 기다림
        self.show()     # 두 번째 창이 닫히면 다시 메인 창이 열림


class Second_Window(QDialog, QWidget, form_class2):  # class name 변경
    def __init__(self):
        super(Second_Window, self).__init__()
        self.setupUi(self)
        self.start_GP()
        self.show()

    # 크롤링 정보 전달 -> 전처리 및 데이터 시각화, 모델링
    def start_GP(self):
        # FS = Find_Store2()
        # FS.play(sname)

        # GUI : 빈칸 채우기 반환값
        self.Store_Name.setText('지코바')  # GUI: 가게이름
        # print('fs.storename:',sname)
        self.Review_Count_total.setText('1000')  # GUI: Total Comment
        # print('fs.comment_total', FS.Comment_Total)
        self.Star_Total.setText('4.9')  # GUI: 총 평점
        # print('fs.star_total', FS.Star_Total)

        # 실시간 크롤링 시 데이터 변수
        # review, menu, star_t, star_opt = FS.print_review()
        # print('review:', review)
        # print('menu:', menu)
        # print('star_t:', star_t)
        # print('star_opt:', star_opt)

        # 1000개 댓글 크롤링 후 생성한 csv 파일 사용 시 데이터 변수
        # pd.set_option('display.max_columns', None)
        df = pd.read_csv('store_csv/DF_푸라닭.csv', index_col=0)
        print(df.info())
        review = list(df['review'])
        menu = list(df['Menu'].dropna(axis=0))
        star_t = list(df['Total Star'])
        star_opt = list(df['Star_opt'])
        output = list(df['Output'])
        print('review:', review)
        print('menu:', menu)
        print('star_t:', star_t)
        print('star_opt:', star_opt)

        # # 모델 실행
        # model = Sentiment()
        review_sample = pd.DataFrame(review, columns=['review'])
        # 구모델 모델링 값
        # output = [4.8, 4.59, 5.0, 5.0, 4.8, 4.6, 4.8, 4.8, 4.8, 4.8, 4.8, 5.0, 4.8, 4.79, 4.6, 3.79, 4.6, 5.0, 5.0, 4.0, 4.8, 5.0, 4.8, 4.8, 4.81, 4.0, 4.4, 4.6, 5.0, 5.0, 4.8, 4.81, 5.0, 4.79, 4.6, 4.79, 5.0, 5.0, 4.42, 5.0, 4.8, 4.8, 4.8, 5.0, 4.63, 4.8, 4.59, 4.8, 4.81, 5.0, 4.8, 5.0, 5.0, 4.8, 4.8, 1.6, 4.42, 4.23, 4.81, 5.0, 5.0, 4.8, 4.8, 1.2, 3.27, 2.41, 4.79, 4.8, 3.25, 4.79, 5.0, 3.04, 5.0, 4.8, 3.17, 4.79, 4.78, 1.22, 4.81, 4.81, 5.0, 5.0, 5.0, 4.61, 4.8, 1.4, 5.0, 4.8, 5.0, 4.8, 4.8, 4.2, 5.0, 4.81, 5.0, 2.41, 4.81, 4.61, 4.8, 4.61, 5.0, 4.61, 3.96, 5.0, 5.0, 3.82, 5.0, 5.0, 1.2, 4.6, 2.22, 4.8, 4.4, 4.13, 5.0, 5.0, 5.0, 4.8, 5.0, 4.18, 4.4, 3.39, 4.81, 4.81, 4.59, 4.8, 4.8, 5.0, 4.6, 5.0, 4.59, 4.4, 4.2, 4.62, 4.41, 4.81, 5.0, 4.8, 4.8, 4.8, 4.8, 4.8, 3.37, 4.0, 4.41, 4.8, 4.81, 4.6, 4.81, 5.0, 5.0, 3.21, 4.8, 4.02, 4.8, 4.8, 5.0, 5.0, 5.0, 5.0, 4.03, 4.21, 5.0, 4.4, 4.8, 3.0, 4.8, 5.0, 4.8, 4.43, 1.4, 4.8, 4.8, 3.78, 4.79, 4.81, 4.39, 4.58, 3.96, 4.8, 4.8, 5.0, 3.22, 4.78, 4.8, 4.6, 1.2, 4.22, 4.8, 3.99, 5.0, 5.0, 3.8, 4.8, 4.8, 4.59, 5.0, 4.8, 4.6, 1.78, 4.8, 1.0, 5.0, 4.61, 4.62, 4.8, 4.41, 4.6, 4.8, 4.6, 5.0, 4.8, 3.2, 4.82, 5.0, 5.0, 2.81, 4.81, 4.8, 4.8, 4.8, 4.0, 3.78, 5.0, 4.8, 4.82, 5.0, 4.61, 5.0, 4.8, 4.8, 4.8, 4.8, 4.01, 4.8, 5.0, 4.8, 4.8, 4.79, 4.8, 4.6, 4.79, 4.8, 4.8, 4.21, 4.6, 3.42, 4.62, 5.0, 5.0, 4.6, 5.0, 2.2, 4.8, 5.0, 4.8, 4.81, 2.18, 4.8, 4.6, 4.8, 5.0, 3.19, 4.8, 3.21, 3.61, 4.8, 5.0, 2.61, 5.0, 2.98, 4.22, 3.61, 4.8, 4.01, 4.8, 4.8, 4.39, 2.78, 4.8, 4.8, 4.8, 5.0, 4.8, 4.6, 4.8, 4.6, 2.24, 1.39, 5.0, 4.8, 4.6, 4.0, 4.2, 5.0, 4.6, 4.39, 4.79, 4.8, 2.39, 4.79, 4.8, 4.8, 4.6, 5.0, 4.8, 4.41, 4.8, 1.83, 4.8, 5.0, 4.8, 5.0, 4.8, 5.0, 4.8, 3.25, 4.8, 5.0, 5.0, 4.6, 4.8, 2.38, 3.21, 4.19, 5.0, 4.8, 4.8, 5.0, 4.4, 4.59, 4.8, 5.0, 3.67, 5.0, 4.6, 5.0, 4.79, 4.8, 4.8, 4.8, 4.8, 4.8, 4.61, 4.8, 1.2, 5.0, 3.78, 4.8, 4.8, 4.8, 4.4, 4.61, 4.8, 4.81, 4.6, 4.59, 4.8, 4.0, 4.6, 5.0, 4.8, 5.0, 4.8, 4.8, 3.58, 4.79, 4.8, 4.6, 4.61, 4.8, 4.8, 5.0, 5.0, 4.8, 5.0, 1.83, 4.6, 4.8, 5.0, 4.8, 4.8, 4.6, 4.39, 4.81, 4.6, 4.8, 3.99, 4.6, 4.8, 4.8, 4.59, 5.0, 4.6, 1.59, 5.0, 4.6, 5.0, 4.8, 4.8, 4.79, 4.81, 4.6, 4.8, 2.99, 4.39, 3.16, 4.19, 4.8, 3.78, 4.21, 5.0, 2.19, 4.41, 4.81, 4.6, 4.8, 4.8, 4.6, 1.79, 5.0, 4.8, 3.2, 4.8, 5.0, 4.8, 4.8, 3.41, 4.8, 4.8, 4.8, 4.6, 4.8, 4.39, 3.58, 4.79, 3.22, 1.78, 5.0, 4.8, 4.8, 4.8, 5.0, 4.8, 4.81, 3.83, 4.6, 5.0, 4.8, 4.81, 5.0, 4.4, 5.0, 4.6, 4.8, 5.0, 3.45, 5.0, 1.81, 4.8, 4.8, 3.58, 5.0, 1.81, 4.79, 4.8, 4.2, 4.6, 4.79, 4.8, 5.0, 2.59, 4.6, 4.8, 4.58, 5.0, 3.62, 4.8, 4.59, 1.61, 5.0, 4.6, 2.21, 4.8, 4.8, 4.81, 4.79, 4.4, 5.0, 5.0, 4.8, 4.59, 4.81, 4.4, 4.6, 4.8, 1.0, 4.8, 5.0, 5.0, 4.2, 4.8, 4.8, 4.6, 4.14, 4.6, 5.0, 4.8, 5.0, 4.8, 5.0, 5.0, 4.8, 4.8, 4.8, 5.0, 4.8, 5.0, 3.99, 5.0, 4.61, 4.8, 4.81, 4.8, 5.0, 5.0, 5.0, 4.79, 5.0, 4.8, 4.8, 4.8, 4.8, 4.81, 5.0, 3.6, 4.81, 4.8, 4.8, 4.8, 5.0, 3.0, 5.0, 5.0, 3.0, 4.4, 4.79, 5.0, 5.0, 4.4, 4.62, 4.8, 5.0, 4.8, 4.81, 5.0, 4.79, 4.8, 4.8, 3.58, 4.8, 2.04, 5.0, 4.8, 4.0, 4.8, 4.8, 4.8, 5.0, 4.8, 4.6, 5.0, 4.8, 5.0, 5.0, 4.6, 4.59, 4.0, 4.81, 4.8, 4.8, 4.8, 4.39, 4.6, 4.6, 4.8, 4.6, 5.0, 5.0, 4.6, 4.8, 1.81, 5.0, 4.8, 4.8, 4.8, 5.0, 5.0, 1.82, 4.78, 5.0, 4.8, 4.8, 4.8, 4.01, 5.0, 4.6, 4.78, 4.4, 4.8, 4.81, 5.0, 1.4, 4.8, 4.8, 5.0, 4.0, 5.0, 4.8, 3.86, 4.79, 4.6, 4.8, 4.6, 5.0, 4.6, 4.4, 5.0, 4.6, 4.8, 2.2, 4.79, 5.0, 4.41, 5.0, 4.79, 1.61, 5.0, 5.0, 4.8, 4.6, 5.0, 5.0, 4.81, 4.79, 2.18, 4.4, 4.8, 5.0, 4.81, 4.8, 4.8, 4.39, 5.0, 5.0, 4.0, 3.8, 5.0, 4.8, 4.6, 4.8, 1.63, 4.8, 4.76, 3.79, 1.4, 2.39, 4.8, 3.79, 4.8, 1.39, 5.0, 4.8, 4.8, 5.0, 4.6, 5.0, 4.8, 5.0, 4.8, 4.6, 5.0, 4.8, 4.8, 3.58, 5.0, 4.38, 5.0, 4.39, 4.8, 4.41, 1.0, 4.8, 4.41, 1.0, 4.81, 5.0, 4.61, 4.6, 2.77, 4.2, 5.0, 4.8, 4.43, 5.0, 4.8, 5.0, 5.0, 5.0, 5.0, 4.79, 2.59, 4.6, 4.79, 4.8, 4.6, 4.8, 4.6, 4.8, 4.8, 2.24, 5.0, 4.8, 4.42, 1.59, 2.4, 4.8, 2.58, 5.0, 2.0, 4.8, 4.8, 4.8, 5.0, 4.8, 4.39, 2.8, 4.8, 2.63, 4.8, 4.19, 4.79, 5.0, 4.8, 5.0, 2.66, 4.21, 4.8, 4.8, 2.21, 5.0, 3.39, 4.39, 5.0, 5.0, 5.0, 5.0, 5.0, 4.79, 5.0, 4.8, 5.0, 4.8, 4.6, 5.0, 5.0, 3.6, 1.6, 4.8, 4.59, 4.39, 4.8, 3.82, 4.79, 1.2, 4.38, 4.8, 3.63, 4.4, 5.0, 5.0, 4.6, 4.8, 5.0, 4.8, 3.81, 4.8, 4.0, 4.8, 4.0, 3.81, 4.8, 4.8, 4.8, 4.21, 4.61, 4.8, 4.81, 4.79, 4.8, 3.6, 4.8, 4.6, 4.81, 4.8, 3.98, 5.0, 4.8, 2.44, 5.0, 4.79, 4.8, 5.0, 3.8, 5.0, 4.8, 4.8, 4.8, 2.0, 1.39, 4.41, 2.2, 4.61, 2.61, 4.8, 4.58, 1.2, 2.0, 2.2, 4.8, 5.0, 4.8, 4.8, 4.8, 4.8, 4.61, 5.0, 5.0, 2.39, 2.39, 4.6, 4.8, 4.79, 4.81, 5.0, 5.0, 4.8, 3.43, 4.8, 1.6, 5.0, 4.39, 4.38, 5.0, 5.0, 2.83, 5.0, 4.8, 2.62, 4.8, 5.0, 4.8, 4.6, 4.2, 4.6, 5.0, 5.0, 4.8, 5.0, 1.6, 5.0, 5.0, 4.8, 4.42, 5.0, 4.8, 3.81, 1.59, 1.79, 5.0, 5.0, 2.21, 4.8, 3.99, 1.59, 4.6, 4.23, 4.8, 5.0, 4.2, 5.0, 5.0, 4.2, 2.39, 5.0, 4.23, 4.6, 1.59, 5.0, 4.8, 4.8, 4.8, 4.8, 5.0, 4.8, 4.8, 5.0, 4.6, 2.63, 4.8, 4.6, 4.8, 1.6, 4.8, 4.6, 4.8, 5.0, 5.0, 5.0, 5.0, 4.6, 5.0, 4.38, 1.59, 4.8, 4.81, 5.0, 4.8, 3.15, 5.0, 5.0, 5.0, 4.4, 4.81, 5.0, 4.01, 5.0, 4.81, 4.8, 5.0, 4.8, 4.8, 5.0, 4.6, 4.2, 4.4, 4.8, 3.8, 5.0, 5.0, 5.0, 4.8, 1.4, 4.6, 4.8, 5.0, 4.61, 5.0, 4.8, 4.8, 4.81, 2.99, 4.62, 2.76, 4.0, 4.59, 4.8, 4.6, 5.0, 4.8, 5.0, 3.18, 4.8, 3.43, 4.6, 4.8, 4.2, 4.61, 4.8, 5.0, 5.0, 5.0, 2.76, 4.8, 5.0, 4.8, 1.81, 4.79, 3.38, 4.81, 4.8, 4.6, 4.8, 4.8, 2.78, 4.61, 5.0, 4.8, 4.81, 3.83]
        # 신모델 모델링 값
        # output = [4.81, 4.59, 5.0, 5.0, 4.8, 4.6, 4.8, 4.8, 4.8, 4.61, 4.8, 5.0, 5.0, 4.8, 4.6, 3.79, 4.6, 5.0, 5.0, 4.0, 4.8, 5.0, 4.8, 4.61, 5.0, 4.2, 4.4, 4.6, 5.0, 5.0, 4.6, 5.0, 5.0, 4.79, 4.21, 4.59, 5.0, 5.0, 5.0, 5.0, 5.0, 4.8, 4.8, 5.0, 4.82, 4.8, 4.6, 4.8, 4.81, 5.0, 4.81, 5.0, 4.8, 4.8, 5.0, 1.61, 4.42, 4.23, 5.0, 5.0, 5.0, 5.0, 4.8, 1.0, 3.23, 2.36, 4.79, 4.8, 3.27, 4.6, 5.0, 3.04, 5.0, 4.8, 2.59, 4.79, 3.99, 1.22, 5.0, 4.62, 5.0, 5.0, 5.0, 4.62, 5.0, 1.4, 5.0, 4.8, 5.0, 4.8, 4.8, 4.2, 5.0, 4.81, 5.0, 2.21, 5.0, 4.61, 5.0, 4.8, 5.0, 5.0, 3.96, 5.0, 5.0, 4.01, 5.0, 5.0, 1.2, 4.6, 2.21, 5.0, 4.2, 3.94, 5.0, 5.0, 5.0, 4.8, 5.0, 4.8, 4.6, 3.01, 5.0, 5.0, 4.59, 4.8, 4.8, 5.0, 4.79, 5.0, 4.59, 4.4, 4.6, 4.62, 4.41, 5.0, 5.0, 4.8, 4.8, 4.6, 4.8, 5.0, 3.94, 3.41, 4.41, 5.0, 4.81, 4.6, 4.81, 4.8, 5.0, 4.0, 4.8, 4.22, 5.0, 4.81, 5.0, 4.8, 5.0, 5.0, 4.61, 4.21, 5.0, 4.4, 4.6, 3.21, 4.8, 5.0, 4.8, 5.0, 1.4, 4.8, 4.8, 4.37, 4.79, 4.81, 4.19, 4.59, 3.39, 4.8, 4.8, 5.0, 3.82, 4.79, 4.8, 4.59, 1.99, 5.0, 4.8, 4.19, 5.0, 5.0, 3.8, 4.61, 4.8, 4.2, 5.0, 4.8, 4.59, 1.78, 4.8, 1.0, 5.0, 4.61, 5.0, 4.6, 4.6, 4.6, 5.0, 4.59, 5.0, 4.8, 3.19, 5.0, 5.0, 5.0, 2.81, 4.81, 5.0, 5.0, 4.78, 4.2, 3.79, 5.0, 4.6, 4.8, 4.8, 4.41, 5.0, 4.8, 5.0, 4.8, 4.8, 3.21, 4.6, 4.41, 4.8, 4.8, 4.79, 5.0, 4.6, 4.6, 4.8, 5.0, 4.8, 4.6, 3.42, 4.62, 5.0, 5.0, 4.8, 5.0, 3.4, 4.8, 5.0, 5.0, 5.0, 2.76, 4.6, 4.4, 4.61, 5.0, 2.4, 4.8, 3.99, 3.8, 4.8, 5.0, 2.61, 5.0, 2.8, 4.23, 4.4, 4.8, 4.6, 4.6, 4.8, 4.39, 2.79, 4.8, 4.8, 5.0, 5.0, 4.8, 4.6, 5.0, 4.59, 3.4, 1.39, 5.0, 5.0, 4.6, 4.4, 4.39, 5.0, 4.6, 4.8, 4.79, 5.0, 1.8, 4.79, 4.8, 4.8, 4.59, 5.0, 5.0, 4.61, 4.61, 1.83, 4.8, 5.0, 5.0, 5.0, 4.6, 5.0, 4.8, 3.25, 4.8, 5.0, 5.0, 4.6, 5.0, 2.4, 3.2, 3.61, 5.0, 4.61, 4.8, 5.0, 4.4, 4.59, 5.0, 5.0, 2.98, 5.0, 4.6, 5.0, 4.79, 4.8, 5.0, 4.8, 4.8, 5.0, 4.61, 4.8, 1.2, 5.0, 3.78, 5.0, 4.6, 4.8, 4.59, 4.61, 5.0, 4.62, 4.6, 4.59, 4.61, 4.21, 4.6, 5.0, 4.8, 5.0, 4.8, 5.0, 2.8, 4.79, 4.8, 4.6, 4.81, 5.0, 5.0, 4.4, 5.0, 4.8, 5.0, 1.82, 4.61, 5.0, 5.0, 5.0, 5.0, 4.4, 4.59, 4.81, 4.8, 5.0, 3.99, 4.6, 4.8, 4.8, 4.6, 5.0, 4.59, 1.58, 5.0, 4.8, 5.0, 4.8, 4.81, 4.79, 4.81, 4.8, 4.8, 3.59, 4.2, 3.16, 4.39, 5.0, 3.78, 4.21, 5.0, 2.03, 4.41, 4.81, 4.8, 4.8, 4.6, 4.61, 1.59, 5.0, 5.0, 3.4, 4.8, 5.0, 4.81, 4.8, 2.8, 4.8, 4.8, 4.8, 4.6, 5.0, 4.39, 2.99, 4.59, 4.6, 2.18, 5.0, 4.8, 4.8, 5.0, 4.8, 5.0, 4.81, 3.83, 4.2, 5.0, 5.0, 4.62, 5.0, 4.6, 5.0, 4.4, 4.8, 5.0, 4.22, 5.0, 1.6, 4.8, 4.8, 3.58, 5.0, 1.81, 4.79, 4.8, 4.2, 4.4, 4.8, 4.8, 5.0, 2.0, 4.8, 4.8, 4.58, 5.0, 3.22, 5.0, 4.59, 2.01, 4.79, 4.8, 1.79, 4.8, 4.8, 4.81, 4.79, 4.4, 5.0, 5.0, 4.61, 4.4, 4.81, 4.4, 4.8, 4.8, 1.0, 4.8, 5.0, 5.0, 4.21, 5.0, 4.8, 4.6, 4.14, 4.6, 5.0, 4.8, 5.0, 4.8, 5.0, 5.0, 4.8, 4.8, 4.8, 5.0, 4.8, 5.0, 3.99, 5.0, 4.81, 4.8, 4.81, 4.8, 5.0, 5.0, 5.0, 4.8, 5.0, 4.8, 4.8, 4.8, 4.8, 4.81, 5.0, 4.0, 4.62, 4.8, 4.8, 4.8, 5.0, 3.44, 5.0, 5.0, 3.0, 4.4, 4.79, 5.0, 5.0, 4.6, 4.81, 5.0, 5.0, 4.8, 4.81, 5.0, 4.6, 4.8, 5.0, 3.58, 5.0, 1.83, 5.0, 5.0, 4.01, 5.0, 4.8, 4.8, 4.8, 5.0, 4.4, 5.0, 4.8, 4.8, 5.0, 4.61, 4.59, 4.0, 4.81, 4.8, 5.0, 4.8, 4.6, 4.6, 4.6, 4.6, 4.8, 4.8, 5.0, 4.8, 5.0, 1.8, 5.0, 4.8, 4.8, 4.8, 5.0, 4.81, 2.41, 4.59, 5.0, 4.8, 4.8, 4.6, 4.8, 5.0, 4.6, 4.78, 4.4, 4.8, 4.81, 5.0, 2.86, 4.8, 4.6, 5.0, 4.0, 5.0, 4.8, 3.86, 4.79, 4.6, 5.0, 4.8, 5.0, 4.6, 4.4, 5.0, 4.6, 5.0, 3.4, 4.8, 5.0, 4.41, 5.0, 4.79, 1.6, 5.0, 5.0, 4.8, 4.6, 5.0, 5.0, 5.0, 4.79, 2.18, 4.6, 5.0, 5.0, 4.81, 4.6, 4.81, 4.58, 5.0, 5.0, 4.0, 3.81, 5.0, 4.8, 4.59, 4.8, 2.4, 4.8, 4.6, 4.17, 1.4, 2.39, 4.8, 3.81, 5.0, 1.39, 5.0, 4.8, 4.8, 4.8, 4.8, 5.0, 4.6, 5.0, 5.0, 4.59, 4.81, 5.0, 4.8, 3.58, 5.0, 4.19, 5.0, 4.19, 4.8, 4.41, 1.0, 4.8, 4.41, 1.0, 4.81, 4.8, 4.61, 4.4, 2.79, 3.2, 5.0, 5.0, 4.43, 5.0, 4.8, 4.8, 5.0, 5.0, 5.0, 4.8, 2.59, 4.6, 4.79, 4.8, 4.6, 4.6, 4.6, 4.8, 5.0, 2.04, 5.0, 5.0, 3.43, 1.39, 2.4, 5.0, 2.58, 5.0, 2.0, 5.0, 4.8, 4.8, 5.0, 4.8, 3.99, 2.8, 4.59, 2.62, 4.8, 4.21, 4.8, 5.0, 4.8, 5.0, 3.42, 4.79, 4.8, 5.0, 2.21, 5.0, 2.79, 4.58, 5.0, 5.0, 5.0, 5.0, 5.0, 4.8, 5.0, 4.8, 5.0, 4.8, 4.8, 5.0, 5.0, 3.6, 1.6, 4.8, 4.6, 4.2, 4.8, 3.83, 4.8, 2.6, 4.38, 5.0, 3.67, 4.4, 5.0, 5.0, 4.8, 4.21, 5.0, 4.8, 3.81, 5.0, 3.8, 4.8, 4.6, 4.6, 5.0, 4.8, 4.61, 5.0, 5.0, 4.8, 5.0, 4.61, 4.8, 3.4, 4.6, 4.6, 5.0, 5.0, 3.98, 5.0, 4.8, 3.4, 5.0, 4.79, 5.0, 5.0, 3.8, 5.0, 4.6, 5.0, 5.0, 1.79, 1.0, 4.39, 2.2, 4.61, 1.99, 4.8, 4.58, 3.6, 1.81, 2.0, 4.8, 5.0, 4.8, 4.8, 4.8, 4.8, 4.6, 5.0, 5.0, 2.0, 2.0, 4.8, 4.8, 4.79, 5.0, 5.0, 5.0, 4.6, 4.21, 4.6, 1.59, 5.0, 4.39, 4.38, 4.81, 5.0, 3.42, 5.0, 4.8, 2.42, 4.8, 5.0, 4.8, 4.6, 4.21, 4.6, 5.0, 5.0, 4.6, 5.0, 1.6, 5.0, 5.0, 4.8, 4.42, 5.0, 4.8, 3.01, 1.19, 1.4, 5.0, 5.0, 1.62, 4.8, 4.18, 1.59, 4.6, 4.23, 5.0, 5.0, 4.2, 5.0, 5.0, 4.4, 1.79, 5.0, 4.23, 4.6, 1.21, 5.0, 5.0, 4.8, 5.0, 5.0, 4.81, 5.0, 4.8, 5.0, 4.6, 2.63, 4.8, 4.6, 4.8, 1.79, 4.8, 4.8, 4.6, 5.0, 5.0, 5.0, 5.0, 4.39, 5.0, 4.38, 1.39, 4.6, 5.0, 5.0, 5.0, 3.15, 5.0, 5.0, 5.0, 4.59, 5.0, 5.0, 4.21, 4.8, 4.81, 4.6, 5.0, 5.0, 4.8, 5.0, 4.59, 4.2, 4.2, 4.59, 3.8, 5.0, 5.0, 5.0, 5.0, 1.99, 4.6, 4.6, 5.0, 5.0, 5.0, 4.8, 4.8, 4.81, 3.18, 4.81, 1.97, 4.2, 4.59, 5.0, 4.6, 5.0, 5.0, 5.0, 3.76, 5.0, 3.04, 4.6, 5.0, 4.59, 4.81, 4.8, 5.0, 5.0, 5.0, 2.99, 5.0, 5.0, 4.8, 1.61, 4.79, 4.18, 4.81, 4.8, 4.4, 5.0, 4.8, 1.99, 4.61, 5.0, 4.8, 4.81, 4.02]
        # print(review_sample.head())
        # print("Model predicting...")
        # output = model.get_score(review_sample)
        # print("********** 모델 결과 ***********")
        # print(output)
        # print("*******************************")
        # # 학습 평점 입력
        # print(type(output[0]))
        avg = round(np.mean(output),1)
        # print(avg)
        # print(type(avg))
        self.Star_Total_2.setText(str(avg))

        # self.review_pre(review)   # 통합 리뷰 워드 클라우드
        self.menu_pre(menu)     # menu top 5 시각화(pie chart)
        self.star_pre(star_opt)     # 항목별 별점 레이더 차트
        self.match_pie(df, output)      # 불일치 댓글 예시
        self.star_compare(star_t, output)       # 별점/학습 별점 차이 라인 그래프
        self.pos_neg_pie(output)        # 긍정/부정 파이차트
        self.bar_chart(star_t, output)      # 일치/불일치 비율 바 그래프

        # logo 이미지 띄워주는 코드
        self.graphicsView.setStyleSheet("border-image:url(\'./store_image/gcova.png');")

        # # 긍정/부정 워드클라우드
        review_sample['predict_star_t'] = output    # output list 결과를 다시 df 형식으로 변환
        # 긍정 = 4.0 이상, 부정 = 4.0 미만인 리뷰 분리
        postive_review = review_sample[review_sample['predict_star_t'] >= 4.0]
        negative_review = review_sample[review_sample['predict_star_t'] < 4.0]
        # 긍정/부정 워드클라우드 함수 실행
        self.postive_review_pre(list(postive_review['review']))     # 긍정 워드 클라우드
        self.negative_review_pre(list(negative_review['review']))       # 부정 워드 클라우드

    ### 데이터 전처리 및 시각화 함수 모음 ###
    # 워드클라우드 시각화(통합)
    def review_pre(self, review):
        engine = Okt()
        all_nouns = engine.nouns(' '.join(review))
        nouns = [n for n in all_nouns if len(n) > 1]
        count = Counter(nouns)
        tags = count.most_common(100)
        wc = WordCloud(font_path='malgun', background_color='white', colormap='magma', width=2500,
                       height=1500)
        cloud = wc.generate_from_frequencies(dict(tags))

        # ui에 matplot 띄우기
        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.graphicsView_4)
        vbox.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        self.ax.imshow(cloud, interpolation='bilinear')
        self.ax.axis('off')
        self.ax.figure.canvas.draw()

    # 항목 별 레이더 그래프 시각화
    def star_pre(self, star_opt):
        df = pd.Series(star_opt)
        df = pd.DataFrame(df, columns=['star'])
        data = df.star.str.split('\n')
        df['taste'] = data.str.get(3).astype('float')
        df['amount'] = data.str.get(6).astype('float')
        df['delivery'] = data.str.get(9).astype('float')

        var = ['맛', '양', '배달']
        var1 = [*var, var[0]]
        var_data = [df['taste'].mean(), df['amount'].mean(), df['delivery'].mean()]
        var_data1 = [*var_data, var_data[0]]
        plt.figure(figsize=(10, 10))
        lobel_loc = np.linspace(start=0, stop=2 * np.pi, num=len(var_data1))
        ax = plt.subplot(polar=True)
        ax.set_theta_offset(pi / 2)  ## 시작점
        # ax.set_theta_direction(1)
        ax.tick_params(axis='x', which='major', pad=15)
        plt.xticks(lobel_loc, labels=var1, color='gray', size=10, fontsize=20)
        ax.plot(lobel_loc, var_data1, linestyle='solid', color='green')
        ax.fill(lobel_loc, var_data1, 'green', alpha=0.3)
        plt.savefig('radar.png')
        plt.clf()
        self.graphicsView_13.setStyleSheet("border-image:url(\'./radar.png');")

    # menu top 5 시각화(pie chart)
    def menu_pre(self, menu):
        print('menu')
        pattern = r"\（.*\）|\(.*\)|\s-|s.*"
        menu_list = []
        count_list = []

        for m1 in menu:
            if m1 == '\n':
                continue
            m1 = m1.replace('\n', '').strip()
            if len(m1.split(',')) == 1:
                menu_list.append(re.sub(pattern=pattern, repl='', string=m1.split('/')[0]))
                num = re.findall('\d+', m1.split('/')[1])
                count_list.append(int(num[0]))
            else:
                for m2 in (m1.split(',')):
                    if '/' not in m2:
                        continue
                    menu_list.append(re.sub(pattern=pattern, repl='', string=m2.split('/')[0]))
                    num = re.findall('\d+', m2.split('/')[1])
                    count_list.append(int(num[0]))

        menu_df = pd.DataFrame({'menu': menu_list, 'count': count_list}, index=None)
        print(menu_df.head())
        menu_sorted = pd.DataFrame(data=menu_df.groupby('menu').sum().sort_values(by='count', ascending=False),
                                   index=None)
        menu_sorted['rank'] = menu_sorted['count'].rank(method='min', ascending=False)
        menu_sorted.reset_index(inplace=True)

        labels = menu_sorted.loc[menu_sorted.index < 5]['menu'].tolist()
        ratio = menu_sorted.loc[menu_sorted.index < 5]['count'].tolist()

        # 기타 항목 추가 되는 부분
        # labels.append('기타')
        # ratio.append(menu_sorted['count'].loc[menu_sorted.index > 5].sum())

        explode = [0.05 for i in range(len(labels))]

        # ui에 matplot 띄우기
        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.graphicsView_6)
        vbox.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        colors = ['#f7ecb0', '#ffb3e6', '#99ff99', '#66b3ff', '#c7b3fb', '#ff6666', '#f9c3b7']
        self.ax.pie(ratio, labels=labels, autopct='%.1f%%', colors=colors, explode=explode, shadow=True)
        self.ax.figure.canvas.draw()

    # 불일치 댓글 예시
    def match_pie(self, dataframe, pred):
        df = dataframe
        df['star'] = df['Total Star'].apply(len)
        df['pred'] = list(map(math.trunc, pred))  # 예측 결과 소수점 이하 버림

        df['T/F'] = [s == p for s, p in zip(df.star.tolist(), df.pred.tolist())]  # 일치 여부 비교
        df['distance'] = abs(df['star'] - df['pred'])  # 실제와 예측 차이 절댓값
        ratio = [len(df.loc[df['T/F'] == True]), len(df.loc[df['T/F'] == False])]  # 일치율, 불일치율 저장

        labels = ['일치율', '불일치율']
        ratio = ratio
        explode = [0.05 for i in range(len(labels))]

        # # ui에 matplot 띄우기
        # canvas = FigureCanvas()
        # vbox = QVBoxLayout(self.graphicsView_9)
        # vbox.addWidget(canvas)
        # self.ax = canvas.figure.subplots()
        # colors = ['#f7ecb0', '#ffb3e6', '#99ff99', '#66b3ff', '#c7b3fb', '#ff6666', '#f9c3b7']
        # self.ax.pie(ratio, labels=labels, autopct='%.1f%%', colors=colors, explode=explode, shadow=True)
        # self.ax.figure.canvas.draw()

        # 가장 차이 많이나는 댓글 3개
        df_sample = df.sort_values('distance', ascending=False)[:4]
        df_sample = df_sample[['review', 'star', 'pred']].reset_index(drop=True)
        df_sample.index = df_sample.index + 1
        # df_sample -> 댓글 3개 dataframe
        print('iloc',df_sample.iloc[0][0])
        print('iloc', df_sample.iloc[0][1])
        print('iloc', df_sample.iloc[0][2])
        print('info',df_sample.info)
        print('head',df_sample.head)

        self.tableWidget.setColumnWidth(0, 500)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 100)
        for i in range(4):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(df_sample.iloc[i][0]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(df_sample.iloc[i][1])))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(df_sample.iloc[i][2])))

    # 별점/학습별점 비교 라인 그래프
    def star_compare(self, stars, pred_review):
        print('star compare')
        stars = list(map(len, stars))
        # pred_review = list(map(round, pred_review))

        diff = [stars[i] - pred_review[i] for i in range(len(pred_review))]
        df = pd.DataFrame({'stars': stars, 'pred_review': pred_review, 'diff': diff})
        df.sort_values(by=['diff', 'stars', 'pred_review'], inplace=True)

        stars = round(df.stars)
        pred_review = round(df.pred_review)

        x = range(len(stars))
        plt.plot(x, stars, label='요기요')
        plt.plot(x, pred_review, label='모델')

        plt.xlabel('리뷰')
        plt.ylabel('평점')
        #
        # plt.fill_between(x=x, y1=stars, y2=0, alpha=0.2)
        # plt.fill_between(x=x, y1=pred_review, y2=0, alpha=0.2)

        plt.ylim(0,6)
        plt.legend(loc="lower right")
        # plt 이미지 저장
        plt.savefig('pie.png')
        plt.clf()
        self.graphicsView_8.setStyleSheet("border-image:url(\'./pie.png');")

    # 긍정/부정 댓글 파이 그래프
    def pos_neg_pie(self, pred_review):
        print('pos neg pie')
        pos_neg = ['pos' if rev >= 3.5 else 'neg' for rev in pred_review]
        ratio = [pos_neg.count('pos') / len(pos_neg), pos_neg.count('neg') / len(pos_neg)]
        labels = ['긍정', '부정']
        colors = ['#6b7ff0', '#f06b7f']
        explode = [0.05 for i in range(len(labels))]

        # ui에 matplot 띄우기
        canvas = FigureCanvas()
        vbox = QVBoxLayout(self.graphicsView_5)
        vbox.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        self.ax.pie(ratio, labels=labels, autopct='%.1f%%', colors=colors, explode=explode, shadow=True)
        self.ax.figure.canvas.draw()

    # 긍정 워드 클라우드
    def postive_review_pre(self, review):
        print('pos review pre')
        plt.clf()
        engine = Okt()
        all_nouns = engine.nouns(' '.join(review))
        nouns = [n for n in all_nouns if len(n) > 1]
        img = Image.open("thumbs_up.jpg")
        print('image get')
        mask = np.array(img)
        count = Counter(nouns)
        tags = count.most_common(100)
        wc = WordCloud(font_path='malgun', mask=mask, background_color='white', colormap='Accent', width=2500,
                       height=1500)
        cloud = wc.generate_from_frequencies(dict(tags))
        print('word cloud')
        # plt.imshow(cloud, interpolation='bilinear')
        # plt.axis('off')

        # ui에 matplot 띄우기
        canvas = FigureCanvas(Figure(figsize=(10,10)))
        vbox = QVBoxLayout(self.graphicsView_4)
        vbox.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        self.ax.imshow(cloud, interpolation='bilinear')
        self.ax.axis('off')
        self.ax.figure.canvas.draw()

        # return plt.show()

    # 부정 워드 클라우드
    def negative_review_pre(self, review):
        print('neg review pre')
        engine = Okt()
        all_nouns = engine.nouns(' '.join(review))
        nouns = [n for n in all_nouns if len(n) > 1]
        img = Image.open('thumbs_down.jpg')
        mask = np.array(img)
        count = Counter(nouns)
        tags = count.most_common(100)
        wc = WordCloud(font_path='malgun', mask=mask, background_color='white', colormap='Accent', width=5000,
                       height=3000)
        cloud = wc.generate_from_frequencies(dict(tags))
        # plt.imshow(cloud, interpolation='bilinear')
        # plt.axis('off')

        # ui에 matplot 띄우기
        canvas = FigureCanvas(Figure(figsize=(20,20)))
        vbox = QVBoxLayout(self.graphicsView_11)
        vbox.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        self.ax.imshow(cloud, interpolation='bilinear')
        self.ax.axis('off')
        self.ax.figure.canvas.draw()
        # return plt.show()

    # 일치율/불일치율 바 그래프
    def bar_chart(self, star_t, output):
        star = [len(s) for s in star_t]
        result = [s == p for s, p in zip(star, output)]
        labels = ['일치율/불일치율']
        true = (result.count(True)) / len(result)  # 일치율
        false = (result.count(False)) / len(result)  # 불일치율
        plt.figure(figsize=(15, 4))
        plt.barh(labels, true, label='일치율', color='gold')
        plt.barh(labels, false, left=true, label='불일치율', color='silver')
        # plt.legend()
        plt.axis('off')

        # plt 이미지 저장
        plt.savefig('bar.png')
        plt.clf()
        self.graphicsView_9.setStyleSheet("border-image:url(\'./bar.png');")
        self.label_3.setText(f"일치율: {str(true*100)} %")
        self.label_6.setText(f"불일치율: {str(false*100)} %")
        # return plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = Main_Window()  # 첫 화면 class 명 입력
    main_dialog.show()
    QApplication.processEvents()
    app.exit(app.exec_())
