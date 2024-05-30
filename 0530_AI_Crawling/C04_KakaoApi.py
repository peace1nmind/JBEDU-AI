"""
[ 카카오 API ]

- 다음(daum)에 검색


"""


#####   라이브러리

##  내장
import json

##  외장
import requests



#####

## 다음(daum) 검색
url = 'https://dapi.kakao.com/v2/search/web'

rest_api_key = '96a951be0f4d53df6b4478628db3eecb'
my_header = {"Authorization": f"KakaoAK {rest_api_key}"}
# item = input("검색할 내용 : ")
item = '인공지능'
params = {'query': item,
          'sort': 'accuracy',
          'page': 1,
          'size': 10}

# url_get = 'https://dapi.kakao.com/v2/search/web?query=인공지능'
# requests.get(url_get, headers=my_header)

r = requests.get(url, params=params, headers=my_header)


##  요청 정상/오류 확인
if r.status_code == 200:
    print("요청 정상")
else:
    print("요청 오류")


##  json
result = r.json()

print(len(result['documents']))
for i in range(len(result['documents'])):
    print(i+1, result['documents'][i]['contents'])
