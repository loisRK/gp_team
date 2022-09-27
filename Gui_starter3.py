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

        # # 모델 실행
        model = Sentiment()
        review_sample = pd.DataFrame(review, columns=['review'])
        print(review_sample.head())
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

        # self.review_pre(review)   # 통합 리뷰 워드 클라우드
        self.menu_pre(menu)
        self.star_pre(star_opt)
        self.match_pie(star_t, output)
        self.star_compare(star_t, output)
        self.pos_neg_pie(output)

        # # 긍정/부정 워드클라우드
        review_sample['predict_star_t'] = output    # output list 결과를 다시 df 형식으로 변환
        # 긍정 = 4.0 이상, 부정 = 4.0 미만인 리뷰 분리
        postive_review = review_sample[review_sample['predict_star_t'] >= 4.0]
        negative_review = review_sample[review_sample['predict_star_t'] < 4.0]
        # 긍정/부정 워드클라우드 함수 실행
        self.postive_review_pre(list(postive_review['review']))
        self.negative_review_pre(list(negative_review['review']))

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

    def match_pie(self, star_t, pred):
        print('match pie')
        star = [len(s) for s in star_t]  # 별 개수 세서 리스트로 저장
        pred_trunc = list(map(math.trunc, pred))  # 예측 결과 소수점 이하 버림

        result = [s == p for s, p in zip(star, pred_trunc)]  # 일치 여부 비교
        ratio = [result.count(True), result.count(False)]  # 일치율, 불일치율 저장

        labels = ['일치율', '불일치율']
        ratio = ratio

        explode = [0.05 for i in range(len(labels))]

        # ui에 matplot 띄우기
        canvas = FigureCanvas()
        vbox = QVBoxLayout(self.graphicsView_9)
        vbox.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        colors = ['#f7ecb0', '#ffb3e6', '#99ff99', '#66b3ff', '#c7b3fb', '#ff6666', '#f9c3b7']
        self.ax.pie(ratio, labels=labels, autopct='%.1f%%', colors=colors, explode=explode, shadow=True)
        self.ax.figure.canvas.draw()

    def star_compare(self, stars, pred_review):
        print('star compare')
        stars = list(map(len, stars))
        # pred_review = list(map(round, pred_review))

        x = range(len(stars))
        plt.plot(x, stars, label='요기요')
        plt.plot(x, pred_review, label='모델')

        plt.xlabel('리뷰')
        plt.ylabel('평점')

        plt.fill_between(x=x, y1=stars, y2=0, alpha=0.2)
        plt.fill_between(x=x, y1=pred_review, y2=0, alpha=0.2)

        plt.ylim(0,6)
        plt.legend(loc="lower right")
        # plt 이미지 저장
        plt.savefig('pie.png')
        plt.clf()
        self.graphicsView_8.setStyleSheet("border-image:url(\'./pie.png');")

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

    def postive_review_pre(self, review):
        print('pos review pre')
        plt.clf()
        engine = Okt()
        all_nouns = engine.nouns(' '.join(review))
        nouns = [n for n in all_nouns if len(n) > 1]
        img = Image.open("./thumbs_up.jpg")
        print('image get')
        mask = np.array(img)
        count = Counter(nouns)
        tags = count.most_common(100)
        wc = WordCloud(font_path='malgun', mask=mask, background_color='white', colormap='cool', width=2500,
                       height=1500)
        cloud = wc.generate_from_frequencies(dict(tags))
        print('word cloud')
        # plt.imshow(cloud, interpolation='bilinear')
        # plt.axis('off')

        # ui에 matplot 띄우기
        canvas = FigureCanvas(Figure(figsize=(8,6)))
        vbox = QVBoxLayout(self.graphicsView_4)
        vbox.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        self.ax.imshow(cloud, interpolation='bilinear')
        self.ax.axis('off')
        self.ax.figure.canvas.draw()

        # return plt.show()

    def negative_review_pre(self, review):
        print('neg review pre')
        engine = Okt()
        all_nouns = engine.nouns(' '.join(review))
        nouns = [n for n in all_nouns if len(n) > 1]
        img = Image.open('./thumbs_down.jpg')
        mask = np.array(img)
        count = Counter(nouns)
        tags = count.most_common(100)
        wc = WordCloud(font_path='malgun', mask=mask, background_color='white', colormap='Accent', width=2500,
                       height=1500)
        cloud = wc.generate_from_frequencies(dict(tags))
        # plt.imshow(cloud, interpolation='bilinear')
        # plt.axis('off')

        # ui에 matplot 띄우기
        canvas = FigureCanvas(Figure(figsize=(8,6)))
        vbox = QVBoxLayout(self.graphicsView_11)
        vbox.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        self.ax.imshow(cloud, interpolation='bilinear')
        self.ax.axis('off')
        self.ax.figure.canvas.draw()
        # return plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = Main_Window()  # 첫 화면 class 명 입력
    main_dialog.show()
    QApplication.processEvents()
    app.exit(app.exec_())
