"""
[ selenium ]

- 동적 크롤링에 사용하는 라이브러리
- 업무 자동화용으로도 사용
- ver.4.06 이후부터는 드라이브 설정이 필요없다


▷ find_element(), find_elements() : 요소들을 찾는데 활용

    By.TAG_NAME
    By.ID
    By.CLASS_NAME
    By.CSS_SELECTOR
    By.XPATH
    By.NAME
    By.LINK_TEXT
    By.PARTIAL_LINK_TEXT

▷ .click() : 클릭
  .send_keys() : 키 입력

    Keys.ENTER, Keys.RETURN : 엔터
    Keys.SPACE : 스페이스바
    ...


"""


#####   라이브러리

## 내장
import time

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

url = "https://www.naver.com"

## 옵션설정
opt = Options()
# opt.add_experimental_option('detach', True)       # 브라우저 꺼짐 방지
opt.add_argument('headless')        # 브라우저 안 뜨게 설정 (실행화면 안 보게)

## 크롬 드라이브 개체 생성
driver = webdriver.Chrome(options=opt)
driver.get(url)



#####   selenium 조작

##  검색창에서 키워드 입력 후 엔터
searchBox = driver.find_element(By.ID, 'query')     # 검색창에 위치 조정
searchBox.send_keys("인공지능")     # 검색창에 행동 조작 ('인공지능' 글씨 넣기)
searchBox.send_keys(Keys.ENTER)     # 엔터 조작


##  뉴스탭 클릭
# 방법1. XPATH 활용
driver.find_element(By.XPATH,
                    '//*[@id="lnb"]/div[1]/div/div[1]/div/div[1]/div[3]/a'
                    ).click()

# # 방법2. LINK_TEXT 활용 (a 태그일 때 사용가능)
# driver.find_element(By.LINK_TEXT,
#                     '뉴스'
#                     ).click()


##  화면 스크롤
scroll = driver.find_element(By.TAG_NAME,
                             'body')        # 스크롤 할 영역 설정

num = 1
while True:
    scroll.send_keys(Keys.PAGE_DOWN)        # Page Down 조작
    time.sleep(0.2)


    ##  뉴스 제목 추출 (100개 추출 후 csv로 저장)
    news_titles = driver.find_elements(By.CLASS_NAME,
                                       'news_tit')

    for title in news_titles:
        if num <= 100:
            print(str(num) + "번 기사 저장중>>>>>")
            with open("news.csv", 'a', encoding='utf-8') as f:
                f.write(str(num) + ". " + title.text)
                f.write('\n')
            num += 1

    if num > 100:
        print("저장 완료")
        break


##  드라이버 종료
driver.quit()

