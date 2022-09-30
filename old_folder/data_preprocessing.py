import numpy as np
import pandas as pd
from PIL import Image

from matplotlib_font import font_setting
import re
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import math

font_setting()


class data_frame:
    def __init__(self):
        self.review = []
        self.star = []
        self.menu = []

    def make_csv(self, review, menu, star_t, star_opt):
        global store_df
        data = {'review': review, 'menu': menu, 'star_total': star_t, 'star_option': star_opt}
        store_df = pd.DataFrame(data)
        store_df.to_csv('C:/Users/Playdata/project/data.csv')
        return store_df

        def star_compare(self, stars, pred_review):
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
            plt.show()

    def pos_neg_pie(self, pred_review):
        pos_neg = ['pos' if rev >= 3.5 else 'neg' for rev in pred_review]
        ratio = [pos_neg.count('pos') / len(pos_neg), pos_neg.count('neg') / len(pos_neg)]
        labels = ['긍정', '부정']
        colors = ['#6b7ff0', '#f06b7f']
        explode = [0.05 for i in range(len(labels))]

        plt.pie(ratio, labels=labels, autopct='%.1f%%', colors=colors, explode=explode, shadow=True)
        plt.show()

    def review_pre(self, review):
        engine = Okt()
        all_nouns = engine.nouns(' '.join(review))
        nouns = [n for n in all_nouns if len(n) > 1]
        count = Counter(nouns)
        tags = count.most_common(100)
        wc = WordCloud(font_path='malgun', background_color='white', colormap='magma', width=2500,
                       height=1500)
        cloud = wc.generate_from_frequencies(dict(tags))
        plt.imshow(cloud, interpolation='bilinear')
        plt.axis('off')

        return plt.show()

    def star_pre(self, star):
        print('star')

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

        # top5가 아닌 메뉴 모두 기타 처리
        # labels.append('기타')
        # ratio.append(menu_sorted['count'].loc[menu_sorted.index > 5].sum())

        explode = [0.05 for i in range(len(labels))]

        colors = ['#f7ecb0', '#ffb3e6', '#99ff99', '#66b3ff', '#c7b3fb', '#ff6666', '#f9c3b7']
        plt.pie(ratio, labels=labels, autopct='%.1f%%', colors=colors, explode=explode, shadow=True)
        print(type(plt.show()))
        return plt.show()

    def math_pie(self, dataframe, pred):
        df = dataframe
        df['star'] = df['Total Star'].apply(len)
        df['pred'] = list(map(math.trunc, pred))  # 예측 결과 소수점 이하 버림

        df['T/F'] = [s == p for s, p in zip(df.star.tolist(), df.pred.tolist())]  # 일치 여부 비교
        df['distance'] = abs(df['star'] - df['pred'])  # 실제와 예측 차이 절댓값
        ratio = [len(df.loc[df['T/F'] == True]), len(df.loc[df['T/F'] == False])]  # 일치율, 불일치율 저장

        labels = ['일치율', '불일치율']
        ratio = ratio
        explode = [0.05 for i in range(len(labels))]
        colors = ['#f7ecb0', '#ffb3e6', '#99ff99', '#66b3ff', '#c7b3fb', '#ff6666', '#f9c3b7']
        plt.pie(ratio, labels=labels, autopct='%.1f%%', colors=colors, explode=explode, shadow=True)

        # 가장 차이 많이나는 댓글 3개
        df_sample = df.sort_values('distance', ascending=False)[:3]
        df_sample = df_sample[['review', 'star', 'pred']].reset_index(drop=True)
        df_sample.index = df_sample.index + 1
        # df_sample -> 댓글 3개 dataframe

        return plt.show()

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
        wc = WordCloud(font_path='malgun', mask=mask, background_color='white', colormap='YlGnBu', width=2500,
                       height=1500)
        cloud = wc.generate_from_frequencies(dict(tags))
        print('word cloud')
        plt.imshow(cloud, interpolation='bilinear')
        plt.axis('off')

        # ui에 matplot 띄우기
        # canvas = FigureCanvas(Figure(figsize=(4, 3)))
        # vbox = QVBoxLayout(self.graphicsView_4)
        # vbox.addWidget(canvas)
        # self.ax = canvas.figure.subplots()
        # self.ax.imshow(cloud, interpolation='bilinear')
        # self.ax.axis('off')
        # self.ax.figure.canvas.draw()

        return plt.show()

    def negative_review_pre(self, review):
        print('neg review pre')
        engine = Okt()
        all_nouns = engine.nouns(' '.join(review))
        nouns = [n for n in all_nouns if len(n) > 1]
        img = Image.open('./thumbs_down.jpg')
        mask = np.array(img)
        count = Counter(nouns)
        tags = count.most_common(100)
        wc = WordCloud(font_path='malgun', mask=mask, background_color='white', colormap='YlGnBu', width=2500,
                       height=1500)
        cloud = wc.generate_from_frequencies(dict(tags))
        plt.imshow(cloud, interpolation='bilinear')
        plt.axis('off')

        # ui에 matplot 띄우기
        # canvas = FigureCanvas(Figure(figsize=(4, 3)))
        # vbox = QVBoxLayout(self.graphicsView_11)
        # vbox.addWidget(canvas)
        # self.ax = canvas.figure.subplots()
        # self.ax.imshow(cloud, interpolation='bilinear')
        # self.ax.axis('off')
        # self.ax.figure.canvas.draw()
        return plt.show()
