# (selenium)
import re

from selenium import webdriver
import time
# (BeautifulSoup)
from bs4 import BeautifulSoup
# (DataFrame)
import pandas as pd
from datetime import datetime

from sentiment_model import Sentiment


class Find_Store():

    def __init__(self):
        super().__init__()
        self.Positive_Review = None     # 모델학습결과 넣을 변수
        self.Negative_Review = None     # 모델학습결과 넣을 변수

    def play(self, sname):

        global store_total_list
        global star_total_list
        global review_total_list
        global review_list
        global star_list
        global menu_list
        global star_opt
        global Star_Total
        global Comment_Total
        global date_list

        # 크롤링 작업
        Store_link = "https://www.yogiyo.co.kr/mobile/#/"
        driver = webdriver.Chrome("chromedriver.exe")
        driver.get(url=Store_link)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="button_search_address"]/button[2]').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[1]/a').click()
        time.sleep(3)

        # 검색버튼 클릭 후 입력받은 가게명 검색창에 입력
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').send_keys(sname)

        # search 버튼 클릭
        driver.find_element_by_xpath('//*[@id="category_search_button"]').click()
        time.sleep(3)

        # 가게 여부를 확인해주는 변수 check_store
        check_store = driver.find_element_by_xpath('//*[@id="content"]/div/div[7]').text == ''

        # test-----------------------------------------------------------------------------------------
        if check_store == False:
            print('가게가 없을 경우')
            driver.quit()
        elif check_store == True:
            print("가게가 있을 경우")
            # --------------------------------------------------------------------------------------------

            # 첫번째 가게 클릭
            driver.find_element_by_xpath(
                '//*[@id="content"]/div/div[5]/div/div/div[1]/div/table/tbody/tr/td[2]/div/div[1]').click()
            # 푸라닭만 1000플 긁어오느라 추가한 코드
            # driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div[2]/div').click()
            time.sleep(3)

            # 클린댓글 클릭
            driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a').click()
            time.sleep(3)

            # 가게 정보 긁어오기
            self.Star_Total = driver.find_element_by_xpath(
                '//*[@id="content"]/div[2]/div[1]/div[5]/div[1]/div/div/strong').text
            self.Comment_Total = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span').text

            print("더보기란 클릭 시작")
            # 여기서 수정한 if문 넣기------------------------------------------------------------------------------------------
            # 댓글의 인덱싱은 xpath의 경로 중 li[]에서 [] 안에 있는 숫자로 결정됨
            # 시작 인덱싱은 2부터 시작
            # 한번에 보여줄 수 있는 댓글의 갯수는 10개이며 넘어갈 경우 더보기란 생성
            # 더보기를 누를 때마다 보여지는 댓글이 10개씩 추가됨
            # 댓글의 갯수가 x라는 변수로 지정하였을 때 더보기 버튼의 총 갯수는 x/10

            reviewtotal = int(self.Comment_Total)
            origin_more_click_count = (reviewtotal / 10) - 1
            # 원하는 댓글의 수를 입력하면  그 갯수에 맞춰 더보기를 클릭할 수 있도록 설정하기(지금은 임의로 30개를 긁어올 수 있도록 2으로 설정)
            # 2 대신 넣어야 하는 것(입력값의 변수 = x)  =>  x/10 - 1
            # more_click_count = 2
            # more_click_count = (1100 / 10) - 1    # 댓글 1000개로 고정
            more_click_count = origin_more_click_count

            if reviewtotal < 11:
                driver.quit()
                print("댓글이 없거나 너무 적습니다.")
            elif reviewtotal > 10:  # 이 때부터 더보기란 생성
                for i in range(1, int(more_click_count) + 1):
                    driver.find_element_by_xpath(f'//*[@id="review"]/li[{(i * 10) + 2}]/a').click()
                    time.sleep(2)
                    # return print("Success")   # for문에서 나올 때 오류가 발생하며 비정상종료됐지만 return 값이 생기니깐 비정상 종료는 안됨
                    # return을 사용하면 종료가 되는 것이기 때문에 결국 원점
                    if i == int(more_click_count):
                        break  # break로 해결됨
                    elif i < int(more_click_count):
                        continue
                    # print('TEEEEEST')             # 하지만 이후 실행되야할 명령어들이 실행되지 않고 끝이 남
                    break
            print('더보기란 클릭 완료')
            # --------------------------------------------------------------------------------------------------------------

        # html 긁어오기 전 충분히 로딩할 시간 부여
        time.sleep(60)

        # selenium 작업으로 더보기 펼친 후 html 긁어오기
        html = driver.page_source
        print('html')
        # print(html)

        time.sleep(3)
        soup = BeautifulSoup(html, 'html.parser')
        # id=review 인 ul 태그 가져오기
        time.sleep(3)
        review_tag = soup.select_one("ul.list-group.review-list")
        # print(review_tag)

        review_list = []
        menu_list = []
        star_list = []
        star_opt = []
        date_list = []

        time.sleep(3)

        # 리뷰 review
        # ul tag 중 원하는 tag 가져오기
        for p in review_tag.find_all("p", class_="ng-binding", attrs={"ng-show": "review.comment"}):
            review_list.append(p.get_text())
        print(len(review_list))
        print(review_list)

        time.sleep(3)

        # 리뷰 메뉴
        for div in review_tag.select('div.order-items.default.ng-binding'):
            menu_list.append(div.get_text())
        print(len(menu_list))
        print(menu_list)

        time.sleep(3)

        # 리뷰 total star
        for s in review_tag.select('div.star-point > span.total'):
            star = ""
            for st in s.select('span.full.ng-scope'):
                star += st.get_text()
            star_list.append(star)
        print(len(star_list))
        print(star_list)

        time.sleep(3)

        # 리뷰 품목별 star
        for s in review_tag.select('div.star-point > span.category'):
            star_opt.append(s.get_text())
        print(len(star_opt))
        print(star_opt)

        time.sleep(3)

        print('check')

        # 리뷰 날짜
        for s in review_tag.select('span.review-time.ng-binding'):
            s1 = s.get_text()
            s2 = s1.split(' ')
            if len(s2) == 3:
                s3 = s2[0] + ' ' + s2[1]
                date_list.append(s3)
        print(len(date_list))
        print(date_list)

        time.sleep(3)

# 크롤링 완---------------------------------------------------------------------------------------------------------

        global review_df
        global menu_df
        global star_df
        global staropt_df
        global date_df

        # review_df 만들기
        review_df = pd.DataFrame({"review":review_list}, index=None)
        print(review_df)
        print('review success')

        time.sleep(3)

        # menu_df 만들기
        menulist = []
        for m1 in menu_list:
            if m1 == '\n':
                continue
            m1 = m1.replace('\n', '').strip()
            menulist.append(m1)

        menu_df = pd.DataFrame({'Menu': menulist}, index=None)
        print(menu_df)
        print('menu success')

        time.sleep(3)

        # star_df 만들기
        star_df = pd.DataFrame({"Total Star":star_list}, index=None)
        print(star_df)
        print('star success')

        time.sleep(3)

        # staropt_df 만들기
        staropt_df = pd.DataFrame({'Star_opt':star_opt}, index=None)
        print(staropt_df)
        print('star_opt success')

        time.sleep(3)

        # date_df 만들기
        date_df = pd.DataFrame({'Date':date_list}, index=None)
        print('date success')

        time.sleep(3)


        # 데이터 프레임 합치기
        Review_info_df = pd.concat([review_df, star_df, menu_df, staropt_df, date_df], axis=1)
        print('Merge success')

        time.sleep(3)

        # 고객이 남긴 데이터들이 담겨있는 데이터프레임 원본을 csv파일로 변환
        Review_info_df.to_csv(f'Original_{sname}.csv')

        time.sleep(3)


        # 원하는 기간의 데이터 추출 ----------------------------------------------------------------------------------------
        # 원하는 기간을 최근 1년으로 정함
        # from datetime import datetime 필요
        d_list = []

        now_year = datetime.today().year
        now_month = datetime.today().month

        for d in range(now_month, 13):
            d_list.append(str(now_year - 1) + '년 ' + str(d) + '월')

        for d in range(1, now_month):
            d_list.append(str(now_year) + '년 ' + str(d) + '월')

        print(d_list)

        Before_Review_df = Review_info_df[Review_info_df['Date'].isin(d_list)]

        print('final success')

        time.sleep(3)
        # --------------------------------------------------------------------------------------------------------------

        # 이모지로만 된 댓글 삭제-------------------------------------------------------------------------------------------
        hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
        Before_Review_df["review"] = Before_Review_df["review"].apply(lambda x: hangul.sub('', x))

        time.sleep(3)
        Before_Review_df.drop(Before_Review_df[Before_Review_df['review'] == ''].index, inplace=True)

        time.sleep(3)
        # --------------------------------------------------------------------------------------------------------------

        # print(Before_Review_df)
        print('###INFO###')
        print(Before_Review_df.info())

        # 최근 1년간의 데이터들이 담긴 Review 데이터 프레임을 csv변환
        Before_Review_df.to_csv(f'Before_{sname}.csv')

        print(Before_Review_df.tail())


        # 예측 점수 컬럼이 포함된 최종 리뷰 데이터프레임 만들기------------------------------------------------------------------
        After_Review_df = Before_Review_df

        # 모델 실행
        from sentence_transformers import SentenceTransformer
        from keras.models import load_model
        import numpy as np

        model = SentenceTransformer('jhgan/ko-sroberta-multitask')
        df_em = pd.DataFrame({'word': After_Review_df["review"],
                              'embedding': pd.Series([] * len(After_Review_df["review"]))})
        df_em['embedding'] = df_em['word'].map(lambda x: list(model.encode(x)))

        model = load_model('./review_predict.h5')
        feature = np.vstack(df_em.embedding.values)
        print("Model predicting...")
        predict_score = model.predict(feature)
        output = [x + 1 for x in map(np.argmax, predict_score)]
        print("********** 모델 결과 ***********")
        print(output)
        print("*******************************")

        output_df = pd.DataFrame({'Output': output}, index=None)

        After_Review_df = pd.concat([After_Review_df, output_df], axis=1)
        After_Review_df = After_Review_df.dropna()
        print(After_Review_df.head)

        After_Review_df.to_csv(f'After_{sname}_total.csv')

        print('★☆Finish☆★')
