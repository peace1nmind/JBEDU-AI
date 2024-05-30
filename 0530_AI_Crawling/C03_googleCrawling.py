"""
[ 구글 이미지 크롤링 ]


"""


#####   라이브러리

## 내장
import time
import urllib.request
import os

## 외장
import requests
import pandas as pd
import openpyxl

## selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options   # 크롬 드라이버 옵션 설정하는 모듈
from selenium.webdriver.common.by import By     # find_element() 에서 사용하기 위한 모듈 (위치 조작)
from selenium.webdriver.common.keys import Keys     # send_keys() 에서 사용하기 위한 모듈 (행동 조작)



#####   selenium 기본 설정 (브라우저 설정 및 띄우기)

url = "https://www.google.com"

## 옵션설정
opt = Options()
opt.add_experimental_option('detach', True)       # 브라우저 꺼짐 방지
# opt.add_argument('headless')        # 브라우저 안 뜨게 설정 (실행화면 안 보게)

## 크롬 드라이브 개체 생성
driver = webdriver.Chrome(options=opt)
driver.get(url)



#####   작동

##  검색어 설정
# item = input("검색할 내용을 입력 : ")
item = '고양이'
search = f'{item} 무료 png'


##  내용 검색
searchBox = driver.find_element(By.ID,
                                'APjFqb')
searchBox.send_keys(search)
searchBox.submit()      # 엔터와 같은 기능


##  이미지 클릭
driver.find_element(By.LINK_TEXT,
                    '이미지'
                    ).click()


##  이미지 저장 폴더 생성
img_dir = "img"
os.makedirs(img_dir, exist_ok=True)        # exist_ok=True : 이미 존재하면 무시


##  이미지 검색 개수 및 다운로드
save_dir = img_dir+f"/{item}"
os.makedirs(save_dir, exist_ok=True)

imgs = driver.find_elements(By.CSS_SELECTOR, 'g-img.mNsIhb>img.YQ4gaf')

time.sleep(2)

for i in range(len(imgs)):
    img_url = imgs[i].get_attribute('src')
    if img_url is not None:
        urllib.request.urlretrieve(img_url,
                                   f"./{save_dir}/{item}_{i+1}.jpg")

print("저장 완료")


##  드라이브 종료
# driver.quit()
