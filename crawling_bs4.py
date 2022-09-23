# (selenium)
from selenium import webdriver
import time
# (BeautifulSoup)
from bs4 import BeautifulSoup


class Find_Store2():

    def __init__(self):
        super().__init__()
        self.Comment_Total = None
        self.Store_Name = None
        self.Star_Total = None
        self.review_list = None     # 데이터 전처리용 변수
        self.star_list = None       # 데이터 전처리용 변수
        self.menu_list = None       # 데이터 전처리용 변수
        self.star_opt = None        # 데이터 전처리용 변수
        self.Positive_Review = None     # 모델학습결과 넣을 변수
        self.Negative_Review = None     # 모델학습결과 넣을 변수

    def play(self, sname):

        # 크롤링 작업
        Store_link = "https://www.yogiyo.co.kr/mobile/#/"
        driver = webdriver.Chrome("./chromedriver.exe")
        driver.get(url=Store_link)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="button_search_address"]/button[2]').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[1]/a').click()
        time.sleep(3)

        # 검색버튼 클릭 후 입력받은 가게명 검색창에 입력
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').click()

        driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').send_keys(sname)
        time.sleep(3)

        # search 버튼 클릭
        driver.find_element_by_xpath('//*[@id="category_search_button"]').click()
        time.sleep(3)
        print('test')

        # 첫번째 가게 클릭
        driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div[1]/div/table/tbody/tr/td[2]/div/div[1]').click()
        time.sleep(3)

        # 클린댓글 클릭
        driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a').click()
        time.sleep(3)

        # 가게 정보 긁어오기
        self.Star_Total = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[5]/div[1]/div/div/strong').text
        self.Comment_Total = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span').text
        self.Store_Name = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[1]/div[1]/span').text
        print('test2')

        print(self.Comment_Total)

        # click 조건
        if int(self.Comment_Total) > 30:
            driver.find_element_by_xpath('//*[@id="review"]/li[12]/a').click()
            time.sleep(3)
            driver.find_element_by_xpath('//*[@id="review"]/li[22]/a').click()
            time.sleep(3)
            driver.find_element_by_xpath('//*[@id="review"]/li[32]/a').click()
        elif 31 > int(self.Comment_Total) > 20:
            driver.find_element_by_xpath('//*[@id="review"]/li[12]/a').click()
            time.sleep(3)
            driver.find_element_by_xpath('//*[@id="review"]/li[22]/a').click()
        elif 21 > int(self.Comment_Total) > 10:
            driver.find_element_by_xpath('//*[@id="review"]/li[12]/a').click()
        else:
            pass

        time.sleep(3)

        # selenium 작업으로 더보기 펼친 후 html 긁어오기
        html = driver.page_source
        print('html')
        print(html)

        soup = BeautifulSoup(html, 'html.parser')
        # id=review 인 ul 태그 가져오기
        review_tag = soup.select_one("ul.list-group.review-list")
        # print(review_tag)

        review_list = []
        menu_list = []
        star_list = []
        star_opt = []

        # ul tag 중 원하는 tag 가져오기
        for p in review_tag.find_all("p", class_="ng-binding", attrs={"ng-show":"review.comment"}):
            review_list.append(p.get_text())
        print(review_list)

        # 리뷰 메뉴
        for div in review_tag.select('div.order-items.default.ng-binding'):
            menu_list.append(div.get_text())
        print(menu_list)

        # 리뷰 total star
        for s in review_tag.select('div.star-point > span.total'):
            star = ""
            for st in s.select('span.full.ng-scope'):
                star += st.get_text()
            star_list.append(star)
        print(star_list)

        # 리뷰 품목별 star
        for s in review_tag.select('div.star-point > span.category'):
            star_opt.append(s.get_text())
        print(star_opt)

    def print_review(self):
        return self.review_list, self.menu_list, self.star_list, self.star_opt