# 데이터 전처리 코드 메인 통합 버전
# main 실행 파일
import os
import sys
import math
from PIL import Image
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

# matplotlib_font 실행
font_setting()


# 파일 불러오는 함수 생성
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


#################main.ui 가져오기#######################
form = resource_path('MAIN_START.ui')
form_class1 = uic.loadUiType(form)[0]
##############Second_Choice_Page.ui 가져오기############
form2 = resource_path('content.ui')
form_class2 = uic.loadUiType(form2)[0]


class Main_Window(QMainWindow, form_class1):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.store_info()

    def store_info(self):
        # 음식점 데이터
        # 지코바
        global gcova_name
        global gcova_total_star
        global gcova_total_review
        global gcova_csv
        global gcova_logo_path

        gcova_name = '지코바-독산1호점'
        gcova_total_star = '4.9'
        gcova_total_review = '1000'
        gcova_csv = './store_csv/DF_지코바.csv'
        gcova_logo_path = "border-image:url(\'./store_image/gcova.png');"

        self.Store_name_1.setText(gcova_name)
        self.Store_total_star_1.setText(gcova_total_star)
        self.Store_total_review_1.setText(gcova_total_review)
        self.btn_store_picture_1.setStyleSheet(gcova_logo_path)


        # 굽네치킨
        global goobne_name
        global goobne_total_star
        global goobne_total_review
        global goobne_csv
        global goobne_logo_path

        goobne_name = 'BBQ'
        goobne_total_star = '4.3'
        goobne_total_review = '1000'
        goobne_csv = './store_csv/DF_bbq.csv'
        goobne_logo_path = "border-image:url(\'./store_image/bbq.png');"

        self.Store_name_2.setText(goobne_name)
        self.Store_total_star_2.setText(goobne_total_star)
        self.Store_total_review_2.setText(goobne_total_review)
        self.btn_store_picture_2.setStyleSheet(goobne_logo_path)

        # 푸라닭
        global puradak_name
        global puradak_total_star
        global puradak_total_review
        global puradak_csv
        global puradak_logo_path

        puradak_name = '푸라닭-미성점'
        puradak_total_star = '4.9'
        puradak_total_review = '1000'
        puradak_csv = './store_csv/DF_푸라닭.csv'
        puradak_logo_path = "border-image:url(\'./store_image/puradak.png');"

        self.Store_name_3.setText(puradak_name)
        self.Store_total_star_3.setText(puradak_total_star)
        self.Store_total_review_3.setText(puradak_total_review)
        self.btn_store_picture_3.setStyleSheet(puradak_logo_path)

        # 교촌치킨
        global gyochon_name
        global gyochon_total_star
        global gyochon_total_review
        global gyochon_csv
        global gyochon_logo_path

        gyochon_name = '교촌치킨-독산1호점'
        gyochon_total_star = '4.7'
        gyochon_total_review = '1000'
        gyochon_csv = './store_csv/DF_교촌.csv'
        gyochon_logo_path = "border-image:url(\'./store_image/kyochon.png');"

        self.Store_name_4.setText(gyochon_name)
        self.Store_total_star_4.setText(gyochon_total_star)
        self.Store_total_review_4.setText(gyochon_total_review)
        self.btn_store_picture_4.setStyleSheet(gyochon_logo_path)

        # 또래오래
        global ddorea_name
        global ddorea_total_star
        global ddorea_total_review
        global ddorea_csv
        global ddorea_logo_path

        ddorea_name = '또래오래-독산가산점'
        ddorea_total_star = '4.9'
        ddorea_total_review = '1000'
        ddorea_csv = './store_csv/DF_또래오래.csv'
        ddorea_logo_path = "border-image:url(\'./store_image/ddorea.png');"

        self.Store_name_5.setText(ddorea_name)
        self.Store_total_star_5.setText(ddorea_total_star)
        self.Store_total_review_5.setText(ddorea_total_review)
        self.btn_store_picture_5.setStyleSheet(ddorea_logo_path)

    def detail_1_store(self):
        global STORE_NAME
        global STORE_TOTAL_REVIEW
        global STORE_TOTAL_STAR
        global STORE_CSV
        global STORE_LOGO_PATH
        STORE_NAME = gcova_name
        STORE_TOTAL_REVIEW = gcova_total_review
        STORE_TOTAL_STAR =gcova_total_star
        STORE_CSV = gcova_csv
        STORE_LOGO_PATH = gcova_logo_path
        print(STORE_NAME)
        print(STORE_TOTAL_REVIEW)
        print(STORE_TOTAL_STAR)
        print(STORE_CSV)
        print(STORE_LOGO_PATH)

        self.main_display()

    def detail_2_store(self):
        global STORE_NAME
        global STORE_TOTAL_REVIEW
        global STORE_TOTAL_STAR
        global STORE_CSV
        global STORE_LOGO_PATH
        STORE_NAME = goobne_name
        STORE_TOTAL_REVIEW = goobne_total_review
        STORE_TOTAL_STAR = goobne_total_star
        STORE_CSV = goobne_csv
        STORE_LOGO_PATH = goobne_logo_path
        print(STORE_NAME)
        print(STORE_TOTAL_REVIEW)
        print(STORE_TOTAL_STAR)
        print(STORE_CSV)
        print(STORE_LOGO_PATH)

        self.main_display()

    def detail_3_store(self):
        global STORE_NAME
        global STORE_TOTAL_REVIEW
        global STORE_TOTAL_STAR
        global STORE_CSV
        global STORE_LOGO_PATH
        STORE_NAME = puradak_name
        STORE_TOTAL_REVIEW = ddorea_total_review
        STORE_TOTAL_STAR = puradak_total_star
        STORE_CSV = puradak_csv
        STORE_LOGO_PATH = puradak_logo_path
        print(STORE_NAME)
        print(STORE_TOTAL_REVIEW)
        print(STORE_TOTAL_STAR)
        print(STORE_CSV)
        print(STORE_LOGO_PATH)

        self.main_display()

    def detail_4_store(self):
        global STORE_NAME
        global STORE_TOTAL_REVIEW
        global STORE_TOTAL_STAR
        global STORE_CSV
        global STORE_LOGO_PATH
        STORE_NAME = gyochon_name
        STORE_TOTAL_REVIEW = gyochon_total_review
        STORE_TOTAL_STAR = gyochon_total_star
        STORE_CSV = gyochon_csv
        STORE_LOGO_PATH = gyochon_logo_path
        print(STORE_NAME)
        print(STORE_TOTAL_REVIEW)
        print(STORE_TOTAL_STAR)
        print(STORE_CSV)
        print(STORE_LOGO_PATH)

        self.main_display()

    def detail_5_store(self):
        global STORE_NAME
        global STORE_TOTAL_REVIEW
        global STORE_TOTAL_STAR
        global STORE_CSV
        global STORE_LOGO_PATH
        STORE_NAME = ddorea_name
        STORE_TOTAL_REVIEW = ddorea_total_review
        STORE_TOTAL_STAR =ddorea_total_star
        STORE_CSV = ddorea_csv
        STORE_LOGO_PATH = ddorea_logo_path
        print(STORE_NAME)
        print(STORE_TOTAL_REVIEW)
        print(STORE_TOTAL_STAR)
        print(STORE_CSV)
        print(STORE_LOGO_PATH)

        self.main_display()

    def quit_window(self):
        self.close()

    def main_display(self):
        self.hide()  # 메인 윈도우 숨김
        self.Second = Second_Window()
        self.Second.exec()  # 세 번째 창 닫을 때 까지 기다림
        self.show()     # 세 번째 창이 닫히면 다시 메인 창이 열림

class Second_Window(QDialog, QWidget, form_class2):  # class name 변경
    def __init__(self):
        super(Second_Window, self).__init__()
        self.setupUi(self)
        self.start_GP()
        self.show()
        self.back_home.clicked.connect(self.Second_close)

    def Second_close(self):
        print(STORE_NAME)
        print(STORE_TOTAL_REVIEW)
        print(STORE_TOTAL_STAR)
        print(STORE_CSV)
        print(STORE_LOGO_PATH)
        self.close()

    # 크롤링 정보 전달 -> 전처리 및 데이터 시각화, 모델링
    def start_GP(self):

        print('second window')
        # GUI : 빈칸 채우기 반환값
        self.Store_Name.setText(STORE_NAME)  # GUI: 가게이름
        # print('fs.storename:',sname)
        self.Review_Count_total.setText(STORE_TOTAL_REVIEW)  # GUI: Total Comment
        # print('fs.comment_total', FS.Comment_Total)
        self.Star_Total.setText(STORE_TOTAL_STAR)  # GUI: 총 평점
        # print('fs.star_total', FS.Star_Total)

        # logo 이미지 띄워주는 코드
        self.graphicsView.setStyleSheet(STORE_LOGO_PATH)

        # 실시간 크롤링 시 데이터 변수
        # review, menu, star_t, star_opt = FS.print_review()
        # print('review:', review)
        # print('menu:', menu)
        # print('star_t:', star_t)
        # print('star_opt:', star_opt)

        # 1000개 댓글 크롤링 후 생성한 csv 파일 사용 시 데이터 변수
        # pd.set_option('display.max_columns', None)
        df = pd.read_csv(STORE_CSV, index_col=0)
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
        print('Output:', output)

        review_sample = pd.DataFrame(review, columns=['review'])
        avg = round(np.mean(output), 1)
        self.Star_Total_2.setText(str(avg))

        # self.review_pre(review)   # 통합 리뷰 워드 클라우드
        self.menu_pre(menu)  # menu top 5 시각화(pie chart)
        self.star_pre(star_opt)  # 항목별 별점 레이더 차트
        self.match_pie(df, output)  # 불일치 댓글 예시
        self.star_compare(star_t, output)  # 별점/학습 별점 차이 라인 그래프
        self.pos_neg_pie(output)  # 긍정/부정 파이차트
        self.bar_chart(star_t, output)  # 일치/불일치 비율 바 그래프

        # # 긍정/부정 워드클라우드
        review_sample['predict_star_t'] = output  # output list 결과를 다시 df 형식으로 변환
        # 긍정 = 4.0 이상, 부정 = 4.0 미만인 리뷰 분리
        postive_review = review_sample[review_sample['predict_star_t'] >= 3.0]
        negative_review = review_sample[review_sample['predict_star_t'] < 3.0]
        # 긍정/부정 워드클라우드 함수 실행
        self.postive_review_pre(list(postive_review['review']))  # 긍정 워드 클라우드
        self.negative_review_pre(list(negative_review['review']))  # 부정 워드 클라우드

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
        print('star pre')
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
        ax.set_theta_direction(1)
        ax.tick_params(axis='x', which='major', pad=15)
        plt.xticks(lobel_loc, labels=var1, color='gray', size=10, fontsize=20)
        ax.plot(lobel_loc, var_data1, linestyle='solid', color='green')
        ax.fill(lobel_loc, var_data1, 'green', alpha=0.3)
        plt.savefig('radar.png')
        plt.clf()
        self.graphicsView_13.setStyleSheet("border-image:url(\'./radar.png');")
        print('star pre quit')

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

        explode = [0.05 for i in range(len(labels))]

        # ui에 matplot 띄우기
        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.graphicsView_6)
        vbox.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        colors = ['#f7ecb0', '#ffb3e6', '#99ff99', '#66b3ff', '#c7b3fb', '#ff6666', '#f9c3b7']
        self.ax.pie(ratio, labels=labels, autopct='%.1f%%', colors=colors, explode=explode, shadow=True)
        self.ax.figure.canvas.draw()
        print('menu draw')

    # 불일치 댓글 예시 테이블
    def match_pie(self, dataframe, pred):
        df = dataframe
        df['star'] = df['Total Star'].apply(len)
        df['pred'] = list(map(math.trunc, pred))  # 예측 결과 소수점 이하 버림

        df['T/F'] = [s == p for s, p in zip(df.star.tolist(), df.pred.tolist())]  # 일치 여부 비교
        df['distance'] = abs(df['star'] - df['pred'])  # 실제와 예측 차이 절댓값

        # 가장 차이 많이나는 댓글 3개
        df_sample = df.sort_values('distance', ascending=False)[:4]
        df_sample = df_sample[['review', 'star', 'pred']].reset_index(drop=True)
        df_sample.index = df_sample.index + 1
        # df_sample -> 댓글 3개 dataframe
        print('iloc', df_sample.iloc[0][0])
        print('iloc', df_sample.iloc[0][1])
        print('iloc', df_sample.iloc[0][2])
        print('info', df_sample.info)
        print('head', df_sample.head)

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
        plt.ylim(0, 6)
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
        n_nouns = []
        # 중의적 표현 삭제
        f_word = ['항상','오늘','역시','진짜','주신','먹음','나용','회사','해도',
                  '가요','주시','버세','이크','로서','요사','그것','라서','거나',
                  '이드','서요','요나','다라','레도','이서','이지','니드','더니',
                  '나니','대로','읍니','러신','솼습']
        for n in nouns:
            if n not in f_word:
                n_nouns.append(n)

        img = Image.open("./thumbs_up.jpg")
        print('image get')
        mask = np.array(img)
        count = Counter(n_nouns)
        tags = count.most_common(100)
        wc = WordCloud(font_path='malgun', mask=mask, background_color='white', colormap='winter', width=2500,
                       height=1500, random_state=199)
        cloud = wc.generate_from_frequencies(dict(tags))
        print('word cloud')

        # ui에 matplot 띄우기
        canvas = FigureCanvas(Figure(figsize=(10, 10)))
        vbox = QVBoxLayout(self.graphicsView_4)
        vbox.addWidget(canvas)
        self.ax = canvas.figure.subplots()
        self.ax.imshow(cloud, interpolation='bilinear')
        self.ax.axis('off')
        self.ax.figure.canvas.draw()

    # 부정 워드 클라우드
    def negative_review_pre(self, review):
        print('neg review pre')
        engine = Okt()
        all_nouns = engine.nouns(' '.join(review))
        nouns = [n for n in all_nouns if len(n) > 1]
        n_nouns = []
        # 중의적 표현 삭제
        f_word = ['항상', '오늘', '역시', '진짜', '주신', '먹음', '나용', '회사', '해도',
                  '가요', '주시', '버세', '이크', '로서', '요사', '그것', '라서', '거나',
                  '이드', '서요', '요나', '다라', '레도', '이서', '이지', '니드', '더니',
                  '나니', '대로', '읍니', '러신', '솼습']
        for n in nouns:
            if n not in f_word:
                n_nouns.append(n)

        img = Image.open('./thumbs_down.jpg')
        mask = np.array(img)
        count = Counter(n_nouns)
        tags = count.most_common(100)
        wc = WordCloud(font_path='malgun', mask=mask, background_color='white', colormap='gnuplot', width=2500,
                       height=1500, random_state=199)
        cloud = wc.generate_from_frequencies(dict(tags))
        # plt.imshow(cloud, interpolation='bilinear')
        # plt.axis('off')

        # ui에 matplot 띄우기
        canvas = FigureCanvas(Figure(figsize=(20, 20)))
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
        self.label_3.setText(f"일치율: {str(true * 100)} %")
        self.label_6.setText(f"불일치율: {str(false * 100)} %")
        # return plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_dialog = Main_Window()  # 첫 화면 class 명 입력
    main_dialog.show()
    QApplication.processEvents()
    app.exit(app.exec_())