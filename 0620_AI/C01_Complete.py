"""
[ Exchange Rate ]

크롤링 해와서 streamlit 에 표시


"""


#####   라이브러리

# !pip install html5lib
import pandas as pd
import re
import streamlit as st

import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

from io import BytesIO



def ex_rate():
    #####   화폐 종류 딕셔너리로 모으기
    list_url = "https://finance.naver.com/marketindex/exchangeList.naver"
    list_tbl = pd.read_html(list_url, encoding='cp949')

    # 화페 종류 딕셔너리 만드는 함수
    def c_code_dic():
        code_dic = {}
        c_code_df = pd.DataFrame()
        c_code_df = pd.concat([c_code_df, list_tbl[0]])
        text_list = c_code_df['통화명']['통화명']

        for text in text_list:
            kor = re.findall(r'[가-힣]+', text)
            kor = "".join(kor)
            eng = re.findall(r'[a-zA-Z]+', text)
            eng = "".join(eng)
            code_dic[kor] = eng

        return code_dic
        


    #####   환율 데이터 반환 함수

    def get_exchange(currency):
        # 화폐
        c_code = c_code_dic()[currency]

        # 페이지
        last_pageNum = 10

        # 설정한 화폐의 시장동향을 넣을 빈 데이터프레임
        tbl = pd.DataFrame()

        # 회폐 시장동향 뽑아와서 tbl에 넣기
        for pageNum in range(1, last_pageNum+1):
            url = ("https://finance.naver.com/marketindex/exchangeDailyQuote.naver?" + 
                f"marketindexCd=FX_{c_code}KRW&page={pageNum}")
            
            dfs = pd.read_html(url, header=1, encoding='cp949')

            # 예외처리
            if dfs[0].empty:
                if pageNum == 1:
                    print(f"c_code error : {c_code}")
                else :
                    print(f"Last Page : pageNum={pageNum}")
                break
            
            tbl = pd.concat([tbl, dfs[0]])
        
        # 인덱스 초기화
        tbl = tbl.reset_index(drop=True)

        return tbl



    #####   streamlit

    ### 메인화면
    c_code_list = list(c_code_dic().keys())
    c_name = st.selectbox('통화선택', c_code_list)
    clicked =  st.button("환율 데이터 가져오기")

    if clicked or 'exchange_tbl' in st.session_state:
        if clicked:
            # 전일 대비 제외, 날짜 인덱스 설정
            st.session_state.exchange_tbl = get_exchange(c_name)
            st.session_state.exchange_tbl = st.session_state.exchange_tbl.drop('전일대비', axis=1)
            st.session_state.exchange_tbl.set_index('날짜', inplace=True)
            # 인덱스 날짜 데이터로 변경
            st.session_state.exchange_tbl.index = pd.to_datetime(st.session_state.exchange_tbl.index, format='%Y.%m.%d')
            st.session_state.c_name = c_name

        exchange_tbl = st.session_state.exchange_tbl
        c_name = st.session_state.c_name


        ### 환율 데이터 표시
        st.subheader(c_name +" : "+ c_code_dic()[c_name])
        st.dataframe(exchange_tbl)



        ### 꺾은 선 그래프 그리기
        # 한글 폰트 설정
        plt.rc('font', family="Malgun Gothic")
        fontsize = 15

        graph = exchange_tbl['매매기준율'].plot(figsize=(12, 10), grid=True)

        # 최고값과 최저값 구하기
        max_value = exchange_tbl['매매기준율'].max()
        min_value = exchange_tbl['매매기준율'].min()
        max_date = exchange_tbl['매매기준율'].idxmax()
        max_date = pd.to_datetime(max_date)
        min_date = exchange_tbl['매매기준율'].idxmin()
        min_date = pd.to_datetime(min_date)

        # 최고값과 최저값 그래프에 표기
        graph.annotate(f'₩ {max_value}', 
                    xy=(max_date, max_value), 
                    xytext=(max_date, max_value*1.0015),
                    ha='center', fontsize=fontsize, color='red')
        
        graph.annotate(f'{max_date.strftime("%Y-%m-%d")}', 
                    xy=(max_date, max_value),
                    xytext=(max_date - pd.DateOffset(days=20), max_value),
                    ha='left', fontsize=fontsize, color='red')

        graph.annotate(f'₩ {min_value}', 
                    xy=(min_date, min_value), 
                    xytext=(min_date, min_value*0.9975),
                    ha='center', fontsize=fontsize, color='blue')
        
        graph.annotate(f'{min_date.strftime("%Y-%m-%d")}', 
                    xy=(min_date, min_value), 
                    xytext=(min_date - pd.DateOffset(days=20), min_value),
                    ha='left', fontsize=fontsize, color='blue')

        graph.plot(max_date, max_value, marker='^', markersize=10, color='red', label=f'최고값: {max_value}')
        graph.plot(min_date, min_value, marker='v', markersize=10, color='blue', label=f'최저값: {min_value}')


        # 제목, 라벨 설정
        graph.set_title('환율 (매매기준율)', fontsize="20")
        graph.set_xlabel('기간')
        graph.set_ylabel(f'원화/{c_code_dic()[c_name]}')
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.subplots_adjust(bottom=0.8)
        plt.subplots_adjust(top=1)
        plt.tight_layout()
        fig = graph.get_figure()      # fig 객체로 가져오기

        st.pyplot(fig)

        ### 파일 다운로드
        st.subheader("환율 데이터 파일 다운로드")
        csv_data = exchange_tbl.to_csv(encoding='utf-8-sig').encode('utf-8-sig')

        # 데이터 프레임 → 엑셀 데이터로 변경
        # 메모리 버퍼(임시장소)에 바이너리 객체 생성
        excel_data = BytesIO()
        exchange_tbl.to_excel(excel_data)
        excel_data.seek(0)

        st.download_button("CSV 파일 다운로드", csv_data, 
                        file_name=f'exchane_rate_{c_code_dic()[c_name]}.csv',
                        mime='text/csv')
        
        st.download_button("Excel 파일 다운로드", excel_data, 
                        file_name=f'exchane_rate_{c_code_dic()[c_name]}.xlsx')
        


"""
[ Main File ]

크롤링 해와서 streamlit 에 표시


"""



#####   streamlit.main
### 사이드바
st.sidebar.title("로그인")

# 세션 상태 초기화
if 'login_status' not in st.session_state:
    st.session_state['login_status'] = ''

# 로그인 상태 체크
if st.session_state['login_status'] != 'ok':
    # 로그인 폼
    st.sidebar.header("로그인")
    with st.sidebar.form("로그인"):
        user_id = st.text_input("사용자 ID", value='streamlit', max_chars=15)
        user_pw = st.text_input("비밀번호", value="1234", type="password")
        submitted = st.form_submit_button("로그인")
        if submitted:
            if (user_id == 'streamlit') & (user_pw == '1234'):
                st.session_state['login_status'] = 'ok'
                st.experimental_rerun()
            else:
                st.sidebar.error("로그인 실패")
else:
    # 로그아웃 버튼
    st.sidebar.header("로그아웃")
    if st.sidebar.button("로그아웃"):
        st.session_state['login_status'] = ''
        st.experimental_rerun()

### 로그인 후
if st.session_state['login_status'] == 'ok':

    selectbox_opt = ['환율조회', '']
    your_opt = st.sidebar.selectbox('메뉴', selectbox_opt)
    st.sidebar.write(your_opt)

    if your_opt == '환율조회':
        st.subheader('환율')
        ex_rate()
    else:
        pass