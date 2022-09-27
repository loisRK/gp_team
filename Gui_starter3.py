# 데이터 전처리 코드 메인 통합 버전
# main 실행 파일
import os
import sys
from PyQt5 import uic
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
        self.second = Second_Window(store_name)
        self.second.exec()  # 두 번째 창 닫을 때 까지 기다림
        self.show()     # 두 번째 창이 닫히면 다시 메인 창이 열림


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
        print('review:', review)
        print('menu:', menu)
        print('star_t:', star_t)
        print('star_opt:', star_opt)

        self.review_pre(review)
        self.menu_pre(menu)
        # self.star_pre(star_opt)

        # 모델 실행
        model = Sentiment()
        review_sample = pd.DataFrame(review, columns=['review'])
        print("Model predicting...")
        output = model.get_score(review_sample)
        print("********** 모델 결과 ***********")
        print(output)
        print("*******************************")
        # 학습 평점 입력
        print(type(output[0]))
        avg = round(np.mean(output),1)
        print(avg)
        print(type(avg))
        self.Star_Total_2.setText(str(avg))

    ### 데이터 전처리 및 시각화 함수 모음 ###
    # 워드클라우드 시각화
    def review_pre(self, review):
        engine = Okt()
        all_nouns = engine.nouns(' '.join(review))
        nouns = [n for n in all_nouns if len(n) > 1]
        count = Counter(nouns)
        tags = count.most_common(100)
        wc = WordCloud(font_path='malgun', background_color='rgb(255, 255, 127)', colormap='magma', width=2500,
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

        # ui에 matplot 띄우기
        lobel_loc = np.linspace(start=0, stop=2 * np.pi, num=len(var_data1))
        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        canvas.xticks(lobel_loc, labels=var1, color='gray', size=10, fontsize=20)
        vbox = QVBoxLayout(self.graphicsView_7)
        vbox.addWidget(canvas)

        self.ax = canvas.figure.subplots(polar=True)
        self.ax.set_theta_offset(pi / 2)  ## 시작점
        self.ax.tick_params(axis='x', which='major', pad=15)
        self.ax.plot(lobel_loc, var_data1, linestyle='solid', color='green')
        self.ax.fill(lobel_loc, var_data1, 'green', alpha=0.3)
        self.ax.figure.canvas.draw()

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
        menu_sorted = pd.DataFrame(data=menu_df.groupby('menu').sum().sort_values(by='count', ascending=False),
                                   index=None)
        menu_sorted['rank'] = menu_sorted['count'].rank(method='min', ascending=False)
        menu_sorted.reset_index(inplace=True)

        labels = menu_sorted.loc[menu_sorted.index < 5]['menu'].tolist()
        ratio = menu_sorted.loc[menu_sorted.index < 5]['count'].tolist()

        labels.append('기타')
        ratio.append(menu_sorted['count'].loc[menu_sorted.index > 5].sum())

        explode = [0.05 for i in range(len(labels))]

        # ui에 matplot 띄우기
        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.graphicsView_6)
        vbox.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        colors = ['#f7ecb0', '#ffb3e6', '#99ff99', '#66b3ff', '#c7b3fb', '#ff6666', '#f9c3b7']
        self.ax.pie(ratio, labels=labels, autopct='%.1f%%', colors=colors, explode=explode, shadow=True)
        self.ax.figure.canvas.draw()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = Main_Window()  # 첫 화면 class 명 입력
    main_dialog.show()
    QApplication.processEvents()
    app.exit(app.exec_())
