# 필요한 모듈 호출
import sys
import requests
from bs4 import BeautifulSoup
from newspaper import Article
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
        self.Star_Tatal = ""
        self.Review_Count = ""
        self.Positive_Review = ""
        self.Negative_Review = ""

    def play(self):
        Navermap_link = "https://www.coupang.com/"
        driver = webdriver.Chrome("./../chromedriver.exe")
        driver.get(url=Navermap_link)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="headerSearchKeyword"]').send_keys(Input_Store)
