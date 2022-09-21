import pandas as pd
import numpy as np

class data_frame:
    def __init__(self):
        self.review = []
        self.star = []
        self.menu = []

    def make_csv(self, review, star, menu):
        # data = {'review' : review, 'star' : star, 'menu' : menu}
        df = pd.DataFrame([review, star, menu], columns=['review', 'star', 'menu'])
        print(df)

    def review_pre(self, review):
        print('review')
        print(review)

    def star_pre(self, star):
        print('star')
        print(star)

    def menu_pre(self, menu):
        print('menu')
        print(menu)

