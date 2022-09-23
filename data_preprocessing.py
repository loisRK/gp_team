import pandas as pd
import numpy as np

class data_frame:
    def __init__(self):
        self.review = []
        self.star = []
        self.menu = []

    def make_csv(self, review, menu, star_t, star_opt):
        global store_df
        data = {'review' : review, 'menu' : menu, 'star_total' : star_t, 'star_option' : star_opt}
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

