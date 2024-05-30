"""
[ 뉴스 크롤링 ]


"""


#####   라이브러리

## 외장
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import lxml
import openpyxl



#####   크롤링

##  네이버 뉴스 - 경제 - 금융
url = 'https://news.naver.com/breakingnews/section/101/259'
header = {'user-agent': 'Mozilla/5.0'}
r = requests.get(url, headers=header)
soup = BeautifulSoup(r.text, 'lxml')


##  뉴스 제목과 링크 주소 가져오기
# tag3 = soup.find('ul', {'class': 'sa_list'}).find_all('li', limit=3)
tag3 = soup.select_one('ul.sa_list').select('li', limit=3)

news_list = []

for li in tag3:
    news_info = {'title': li.select_one('strong.sa_text_strong').text.strip(),
                 'news_url': li.find('a')['href']}
    news_list.append(news_info)


##  뉴스 상세페이지로 이동
for news in news_list:
    de_url = news['news_url']
    de_r = requests.get(de_url, headers=header)
    de_soup = BeautifulSoup(de_r.text, 'lxml')

    body = de_soup.find('article', {'class': 'go_trans _article_content'})
    news_contents = body.text.replace("\n", " ").strip()
    news['news_contents'] = news_contents
    print(news_contents+"\n"*3)

news_df = pd.DataFrame(news_list)



#####   한줄 요약하기

# [내 애플리케이션] > [앱 키] 에서 확인한 REST API 키 값 입력
REST_API_KEY = '96a951be0f4d53df6b4478628db3eecb'

# KoGPT API 호출을 위한 메서드 선언
# 각 파라미터 기본값으로 설정
def kogpt_api(prompt, max_tokens = 1, temperature = 1.0, top_p = 1.0, n = 1):
    result = requests.post(
        'https://api.kakaobrain.com/v1/inference/kogpt/generation',
        json = {
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'n': n
        },
        headers = {
            'Authorization': 'KakaoAK ' + REST_API_KEY,
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(result.content)
    return response


# KoGPT에게 전달할 명령어 구성
# for i in range(len(news_df['news_contents'])):
i = 0
try:
    prompt = news_df['news_contents'].iloc[i]
    # print(prompt)
    response = kogpt_api(prompt, max_tokens=200, top_p=0.7)
    # print(response)
    summ = response['generations'][0]['text']
    print(summ)

except:
    print("e")
    summ = ""
    pass

news_df['summary'].iloc[i] = summ

print(news_df.info())

# # 파라미터를 전달해 kogpt_api()메서드 호출
# response = kogpt_api(
#     prompt = prompt,
#     max_tokens = 32,
#     temperature = 1.0,
#     top_p = 1.0,
#     n = 3
# )
#
# print(response)
