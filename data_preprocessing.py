import pandas as pd
import numpy as np
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib
import matplotlib.pyplot as plt
from matplotlib_font import font_setting
from math import pi

font_setting()
class data_frame:
    def __init__(self):
        self.review = []
        self.star = []
        self.menu = []

    def make_csv(self, review, menu, star_t, star_opt):
        global store_df
        data = {'review' : review, 'menu' : menu, 'star_total' : star_t, 'star_option' : star_opt}
        store_df = pd.DataFrame(data)
        store_df.to_csv('C:/Users/Playdata/project/data.csv')
        return store_df

    def review_pre(self, review):
        engine = Okt()
        all_nouns = engine.nouns(''.join(review))
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
        print(1)
        df = pd.Series(star)
        print(2)
        df = pd.DataFrame(df, columns=['star'])
        print(3)
        data = df.star.str.split('\n')
        print(4)
        df['taste'] = data.str.get(3).astype('float64')
        print(5)
        df['amount'] = data.str.get(6).astype('float64')
        print(6)
        df['delivery'] = data.str.get(9).astype('float64')
        print(7)

        var = ['맛', '양', '배달']
        var1 = [*var, var[0]]
        var_data = [df['taste'].mean(), df['amount'].mean(), df['delivery'].mean()]
        var_data1 = [*var_data, var_data[0]]

        lobel_loc = np.linspace(start=0, stop=2 * np.pi, num=len(var_data1))

        ax = plt.subplot(polar=True)
        ax.set_theta_offset(pi / 2)  ## 시작점
        ax.tick_params(axis='x', which='major', pad=15)
        plt.xticks(lobel_loc, labels=var1, color='gray', size=10)
        ax.plot(lobel_loc, var_data1, linestyle='solid', color='green')
        ax.fill(lobel_loc, var_data1, 'green', alpha=0.3)
        return plt.show()
    def menu_pre(self, menu):
        print('menu')
        print(menu)

