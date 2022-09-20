# 필요한 모듈 호출
import sys
import os
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import pyautogui
import pyperclip
from konlpy.tag import Okt
from collections import Counter
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
from selenium import webdriver
import time


class Find_Store():
    def __init__(self):
        super().__init__()
        self.Store_Name = ""
        self.Store_Address = ""
        self.Star_Total = ""
        self.Review_Count = ""
        self.Positive_Review = ""
        self.Negative_Review = ""

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
        count = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/ul/li[2]/a/span').text
        time.sleep(3)
        print(count)

        print('clicked')
        review_list = []

        if driver.find_element_by_xpath('//*[@id="review"]/li[12]/a').is_enabled():
            driver.find_element_by_xpath('//*[@id="review"]/li[12]/a').click()
            time.sleep(3)
        # print('if1')
        time.sleep(3)

        if driver.find_element_by_xpath('//*[@id="review"]/li[22]/a').is_enabled():
            driver.find_element_by_xpath('//*[@id="review"]/li[22]/a').click()
            time.sleep(3)
        # print('if2')
        time.sleep(3)

        if driver.find_element_by_xpath('//*[@id="review"]/li[32]/a').is_enabled():
            driver.find_element_by_xpath('//*[@id="review"]/li[32]/a').click()
            time.sleep(3)
        # print('if3')
        time.sleep(3)

        print(type(count))
        print(type(int(count)))
        c = int(count)

        if c > 33:
            for r in range(2, 33):
                review_list.append(driver.find_element_by_xpath(f'//*[@id="review"]/li[{r}]/p').text)
        elif c == 0:
            pass
        else:
            for r in range(2, c+2):
                review_list.append(driver.find_element_by_xpath(f'//*[@id="review"]/li[{r}]/p').text)

        print('for')

        print(review_list)

        driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').send_keys("비어킹")
        time.sleep(3)

