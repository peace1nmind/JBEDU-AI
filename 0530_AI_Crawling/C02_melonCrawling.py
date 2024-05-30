"""
[ 멜론 곡 정보 크롤링 ]


"""
import os
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



#####

url = "https://www.melon.com"

##  옵션설정
opt = Options()
opt.add_experimental_option('detach', True)       # 브라우저 꺼짐 방지
# opt.add_argument('headless')        # 브라우저 안 뜨게 설정 (실행화면 안 보게)

##  검색어 입력
search = input('검색할 가수 입력 : ')
# search = '잔나비'

##  크롬 드라이브 개체 생성
driver = webdriver.Chrome(options=opt)
driver.get(url)



#####   작동

##  검색창에 잔나비 검색
searchBox = driver.find_element(By.ID,
                                'top_search')
searchBox.send_keys(f'{search}')
searchBox.send_keys(Keys.ENTER)
time.sleep(1)

##  앨범 클릭
driver.find_element(By.LINK_TEXT,
                    '앨범'
                    ).click()
time.sleep(1)


## 앨범 정보들 추출 (제목, 가사)
albums = driver.find_elements(By.CLASS_NAME, 'thumb')
print("albums=", len(albums))

# for album in albums:
#     print(album)

singer = []
album = []
release_date = []
genres = []
titles = []
lyrics = []

song_data = pd.DataFrame()

for n in range(len(albums)):
    time.sleep(3)
    if n <= 2:
        print()
        print(f"{n+1}번째 앨범 시작")
        albums[n].click()
        time.sleep(1)

        titleNum = driver.find_elements(By.TAG_NAME, 'tr')

        try:
            for i in range(1, len(titleNum)):
                print(f"{i}번째 노래 시작")
                # # 노래 제목
                # xp_t = f'//*[@id="frm"]/div/table/tbody/tr[{i}]/td[4]/div/div/div[1]/span/a'
                # song_title = driver.find_element(By.XPATH, xp_t).text
                # titles.append(song_title)

                # 노래 클릭
                xp_l = f'//*[@id="frm"]/div/table/tbody/tr[{i}]/td[3]/div/a'
                driver.find_element(By.XPATH, xp_l).click()
                time.sleep(1)

                # 노래 제목
                song_name = driver.find_element(By.CLASS_NAME,
                                                'song_name').text
                titles.append(song_name)

                # 노래 가수
                singer_name = driver.find_element(By.CLASS_NAME,
                                                  'artist').text
                singer.append(singer_name)

                # 앨범 이름
                album_name = driver.find_element(By.XPATH,
                                                 '//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[1]/a'
                                                 ).text
                album.append(album_name)

                # 발매일
                date = driver.find_element(By.XPATH,
                                           '//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[2]'
                                           ).text
                release_date.append(date)

                # 장르
                genre = driver.find_element(By.XPATH,
                                            '//*[@id="downloadfrm"]/div/div/div[2]/div[2]/dl/dd[3]'
                                            ).text
                genres.append(genre)

                # 노래 가사
                # 가사가 없는 경우 오류 수정 필요
                lyric = driver.find_element(By.ID,
                                            'd_video_summary'
                                            ).text.replace("\n", ". ")
                lyrics.append(lyric)

                print(f"{i}번째 노래 완료")

                # 뒤로가기
                driver.back()
                time.sleep(1)
            driver.back()
            time.sleep(1)

            print(f"{n+1}번째 앨범 완료")

        except:
            pass

    else:
        pass

song_data['가수'] = singer
song_data['앨범명'] = album
song_data['발매일'] = release_date
song_data['장르'] = genres
song_data['노래 제목'] = titles
song_data['노래 가사'] = lyrics

save_dir = "song"
os.makedirs(save_dir, exist_ok=True)

song_data.to_excel(f'./{save_dir}/{search}_노래.xlsx', engine='openpyxl')

print("저장 완료")

#  드라이버 종료
driver.quit()





