"""
[ Main File ]

크롤링 해와서 streamlit 에 표시


"""


#####   라이브러리

import streamlit as st
import C01_1_ExchangeRate as er


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
        er.ex_rate()
    else:
        pass