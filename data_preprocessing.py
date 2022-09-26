import pandas as pd
import numpy as np
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib_font import font_setting
import re
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
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

    def star_pre(self, star_opt):
        print(star_opt)
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
        plt.xticks(lobel_loc, labels=var1, color='gray', size=10,fontsize=20)
        ax.plot(lobel_loc, var_data1, linestyle='solid', color='green')
        ax.fill(lobel_loc, var_data1, 'green', alpha=0.3)
        return plt.show()

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
        menu_sorted = pd.DataFrame(data=menu_df.groupby('menu').sum().sort_values(by='count', ascending=False),index=None)
        menu_sorted['rank'] = menu_sorted['count'].rank(method='min', ascending=False)
        menu_sorted.reset_index(inplace=True)

        labels = menu_sorted.loc[menu_sorted.index < 5]['menu'].tolist()
        ratio = menu_sorted.loc[menu_sorted.index < 5]['count'].tolist()

        labels.append('기타')
        ratio.append(menu_sorted['count'].loc[menu_sorted.index > 5].sum())

        explode = [0.05 for i in range(len(labels))]

        colors = ['#f7ecb0', '#ffb3e6', '#99ff99', '#66b3ff', '#c7b3fb', '#ff6666', '#f9c3b7']
        plt.pie(ratio, labels=labels, autopct='%.1f%%', colors=colors, explode=explode, shadow=True)
        return plt.show()


