import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib_font

matplotlib_font.font_setting()

class data_frame:
    def __init__(self):
        self.review = []
        self.star = []
        self.menu = []

    def make_csv(self, review, star, menu):
        global store_df
        data = {'review' : review, 'star' : star, 'menu' : menu}
        store_df = pd.DataFrame(data)
        print(store_df.head())

    def review_pre(self, review):
        print('review')
        print(review)

    def star_pre(self, star):
        print('star')
        print(star)

    def menu_pre(self, menu):
        print('menu')
        print(menu)
        menu_list = []
        count_list = []
        for m1 in menu:
            if len(m1.split(',')) == 1:
                menu_list.append(m1.split('/')[0].strip())
                num = re.findall('\d+', m1.split('/')[1])
                count_list.append(int(num[0]))
            else:
                for m2 in (m1.split(',')):
                    menu_list.append(m2.split('/')[0])
                    num = re.findall('\d+', m2.split('/')[1])
                    count_list.append(int(num[0]))

        menu_df = pd.DataFrame({'menu': menu_list, 'count': count_list}, index=None)
        menu_sorted = pd.DataFrame(data=menu_df.groupby('menu').sum().sort_values(by='count', ascending=False), index=None)
        menu_sorted['rank'] = menu_sorted['count'].rank(method='max', ascending=False)
        menu_sorted.reset_index(inplace=True)
        labels = menu_sorted.loc[menu_sorted['rank'] < 5]['menu'].tolist()
        ratio = menu_sorted.loc[menu_sorted['rank'] < 5]['count'].tolist()

        # 순위가 5위 미만인 메뉴는 모두 기타로 처리
        labels.append('기타')
        ratio.append(menu_sorted['count'].loc[menu_sorted['rank'] > 5].sum())

        # 메뉴 주문 순위 Top5 파이차트 시각화
        plt.pie(ratio, labels=labels, autopct='%.1f%%')
        return plt.show()


