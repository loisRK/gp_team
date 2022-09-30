## 모델 학습 모듈
# 모듈 가져오기
import pandas as pd
import re
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None)

# sentiment_model.h5, embedding.csv 링크로 다운 받아서 경로 설정하기
working_directory = '.'

class Sentiment:
    def __init__(self):
        # 모델 로딩
        self.model = SentenceTransformer(f'{working_directory}/sentiment_model_re.h5')
        self.embedding_df = pd.read_csv(f'{working_directory}/embedding_re.csv', index_col=0)
        self.embedding_df.embedding = self.embedding_df.embedding.apply(lambda x: [float(i) for i in x[1:-1].split(', ')])

    def predict_score(self, sample_text):
        # 텍스트 벡터화
        embedding_text = list(self.model.encode(sample_text))

        # 학습 데이터의 임베딩과 유사도 비교
        self.embedding_df['distance'] = self.embedding_df['embedding'].map(
            lambda x: cosine_similarity([embedding_text], [x]).squeeze())

        # 유사도의 가중치 계산
        self.embedding_df['weight'] = (self.embedding_df['score'] + 3) * self.embedding_df['distance']
        df_dist_sorted = self.embedding_df.sort_values('distance', ascending=False)

        # 유사도 top 5로 평점 예측
        df_top5 = df_dist_sorted[:5]
        sum_top5 = df_top5['distance'].sum()
        df_top5['sum_weight'] = df_top5['distance'] / sum_top5

        df_top5['new_score'] = df_top5['sum_weight'] * (df_top5['score'] + 3)

        return df_top5.new_score.sum()

    def get_score(self, sample_df):
        # 한글만 남기기
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        sample_df["review"] = sample_df["review"].apply(lambda x: hangul.sub('', x))

        # 빈칸 지우기
        sample_df.drop(sample_df[sample_df['review'] == ''].index, inplace=True)

        # 리뷰 하나씩 모델로 평점 예측
        out_df = []
        for index, row in tqdm(sample_df.iterrows()):
            new_score = self.predict_score(row['review'])
            out_df.append(round(new_score, 2))
            # print('Score: ', new_score)

        return out_df
