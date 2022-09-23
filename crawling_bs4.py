# (selenium)
from selenium import webdriver
import time
# (BeautifulSoup)
from bs4 import BeautifulSoup


class Find_Store2():
    global Star_Total
    global Comment_Total

    def __init__(self):
        super().__init__()
        self.Store_Name = ""
        self.Store_Address = ""
        self.Star_Total = ""
        self.Review_Count = ""
        self.Positive_Review = ""

    def play(self, sname):

        global review_list
        global star_list
        global menu_list

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


        # 가게 여부를 확인해주는 변수 check_store
        check_store = driver.find_element_by_xpath('//*[@id="content"]/div/div[7]').text == ''

        #test-----------------------------------------------------------------------------------------
        if check_store == False:
            print('가게가 없을 경우')
            driver.quit()
        elif check_store == True:
            print("가게가 있을 경우")
            # --------------------------------------------------------------------------------------------

            # 첫번째 가게 클릭
            driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div/div/div[1]/div/table/tbody/tr/td[2]/div/div[1]').click()
            time.sleep(3)

            # 클린댓글 클릭
            driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a').click()
            count = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span').text
            time.sleep(3)

            # 가게 정보 긁어오기
            self.Star_Total = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div[5]/div[1]/div/div/strong').text
            self.Comment_Total = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span').text

            # 더보기 클릭하여 댓글 30개 펼치기----------------------------------------------------------------------------------
            # if driver.find_element_by_xpath('//*[@id="review"]/li[12]/a').is_enabled():
            #     driver.find_element_by_xpath('//*[@id="review"]/li[12]/a').click()
            #     time.sleep(3)
            # else:       # 댓글이 10개 미만인 경우 에러가 발생하지 않도록 pass
            #     pass
            #
            # if driver.find_element_by_xpath('//*[@id="review"]/li[22]/a').is_enabled():
            #     driver.find_element_by_xpath('//*[@id="review"]/li[22]/a').click()
            #     time.sleep(3)
            # else:
            #     pass
            #
            # if driver.find_element_by_xpath('//*[@id="review"]/li[32]/a').is_enabled():
            #     driver.find_element_by_xpath('//*[@id="review"]/li[32]/a').click()
            #     time.sleep(3)
            # else:
            #     pass
            #--------------------------------------------------------------------------------------------------------------

            print("더보기란 클릭 시작")
            # 여기서 수정한 if문 넣기------------------------------------------------------------------------------------------
            # 댓글의 인덱싱은 xpath의 경로 중 li[]에서 [] 안에 있는 숫자로 결정됨
            # 시작 인덱싱은 2부터 시작
            # 한번에 보여줄 수 있는 댓글의 갯수는 10개이며 넘어갈 경우 더보기란 생성
            # 더보기를 누를 때마다 보여지는 댓글이 10개씩 추가됨
            # 댓글의 갯수가 x라는 변수로 지정하였을 때 더보기 버튼의 총 갯수는 x/10

            reviewtotal = int(self.Comment_Total)
            origin_more_click_count = reviewtotal / 10 - 1
            # 원하는 댓글의 수를 입력하면  그 갯수에 맞춰 더보기를 클릭할 수 있도록 설정하기(지금은 임의로 30개를 긁어올 수 있도록 2으로 설정)
            # 2 대신 넣어야 하는 것(입력값의 변수 = x)  =>  x/10 - 1
            more_click_count = 2

            if reviewtotal < 11:
                driver.quit()
                print("댓글이 없거나 너무 적습니다.")
            elif reviewtotal > 10:  # 이 때부터 더보기란 생성
                for i in range(1, more_click_count + 1):
                    driver.find_element_by_xpath(f'//*[@id="review"]/li[{i * 10 + 2}]/a').click()
                    time.sleep(3)
                    # return print("Success")   # for문에서 나올 때 오류가 발생하며 비정상종료됐지만 return 값이 생기니깐 비정상 종료는 안됨
                                                # return을 사용하면 종료가 되는 것이기 때문에 결국 원점
                    if i == more_click_count:
                        break                   # break로 해결됨
                # print('TEEEEEST')             # 하지만 이후 실행되야할 명령어들이 실행되지 않고 끝이 남
                    break
            print('더보기란 클릭 완료')
            #--------------------------------------------------------------------------------------------------------------

            # selenium 작업으로 더보기 펼친 후 html 긁어오기
            html = driver.page_source
            print('html 수집')

            soup = BeautifulSoup(html, 'html.parser')
            # id=review 인 ul 태그 가져오기
            review_tag = soup.select_one("ul.list-group.review-list")
            # print(review_tag)

            review_list = []
            star_list = []
            menu_list = []
            # ul tag 중 원하는 tag 가져오기
            for p in review_tag.select('p.review.comment'):
                review_list.append(p)
                print(review_list)
            # all_review_comment = review_tag.select('#review > li:nth-child(2) > p')
            # print(type(all_review_comment))
            # all_star_comment = review_tag.select('#review > li:nth-child(2) > div:nth-child(2)')
            # print(type(all_star_comment))
            # all_menu_comment = review_tag.select('#review > li:nth-child(2) > div.order-items.default.ng-binding')
            # print(all_menu_comment)


            # beautifulsoup_html 정보 분석
            # beautifulsoup_select_one() 함수
            # review_list = soup.findAll('span', class_='full ng-scope')

            # print(review_list)
            # print(star_list)
            # print(menu_list)

            driver.quit()

    def print_review(self):
        return review_list, star_list, menu_list