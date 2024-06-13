"""
[ streamlit (text, DataFrame, plot)]

streamlit 텍스트, 데이터 프레임, 차트 표시


"""


#####   라이브러리

# 외부
import streamlit
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc



#####   streamlit

### 텍스트 요소
streamlit.title("인공지능 모델 배포")
streamlit.header("헤더")
streamlit.text("일반 텍스트")

streamlit.markdown("# 마크다운")
streamlit.markdown("스트림릿에서 **마크다운**")


### 데이터 요소

# 데이터 불러오기
kr_rain = pd.read_csv("0613_AI\data\korea_rain1.csv")

# 데이터 표시 (DataFarme)
# 다운로드, 정렬등 상호작용 가능
streamlit.subheader("streamlit 데이터 표시 - DataFrame")
streamlit.dataframe(kr_rain)

# 데이터 표시 (Table)
# 상호작용 불가, 데이터 표시만
streamlit.subheader("streamlit 데이터 표시 - Table")
streamlit.table(kr_rain)


### 차트 요소

# 한글 폰트 설정
plt.rc('font', family="Malgun Gothic")

# 데이터 불러오기
factory1 = pd.read_csv("0613_AI\data\공장별_생산현황.csv")
salesTeam = pd.read_excel("0613_AI\data\영업팀별_판매현황.xlsx", index_col='월')

# 차트 그리기 (꺾은 선)
plt_fac1 = factory1.plot()
plt_fac1.set_title("공장별 생산 현황", fontsize=20)
plt_fac1.set_xlabel("연도")
plt_fac1.set_ylabel("생산량")
fig_fac1 = plt_fac1.get_figure()

# 차트 그리기 (막대 그래프)
bar_salesTeam = salesTeam.plot.bar(grid=True, figsize=(12,5), rot=0)
fig_salesTeam = bar_salesTeam.get_figure()

# 차트 표시
streamlit.subheader("꺽은 선형 차트")
streamlit.pyplot(fig_fac1)

streamlit.subheader("막대형 차트")
streamlit.pyplot(fig_salesTeam)


