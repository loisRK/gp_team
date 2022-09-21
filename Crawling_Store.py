# 필요한 모듈 호출
import sys
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
        self.Store_Name = ""
        self.Store_Address = ""
        self.Star_Total = ""
        self.Review_Count = ""
        self.Positive_Review = ""
        self.Negative_Review = ""

    def play(self, Store_Name):

        # 크롤링 작업
        Store_link = "https://www.yogiyo.co.kr/mobile/#/"
        driver = webdriver.Chrome("./chromedriver.exe")
        driver.get(url=Store_link)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="button_search_address"]/button[2]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[1]/a').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').click()
        driver.find_element_by_xpath('//*[@id="category"]/ul/li[15]/form/div/input').send_keys(Store_Name)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="category_search_button"]').click()
        time.sleep(3)
