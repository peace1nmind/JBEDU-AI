"""
[ streamlit (input) ]

streamlit 텍스트, 날짜, 시간 입력


"""


#####   라이브러리

# 외부
import datetime
import streamlit as st



#####   streamlit

### 텍스트 입력
st.title("Text input")

user_id = st.text_input("Input ID : ",
                         value='streamlit', max_chars=15)
user_pw = st.text_input("Input Password : ",
                        value='1234', type='password')

if user_id == 'streamlit':
    if user_pw == '1234':
        st.write("Login Success")
    else:
        st.write("Password Incorrect")
else:
    st.write("Check your ID")


### 날짜 입력
st.title("Date input")

birthday = st.date_input("Birthday", value=datetime.date(2000,1,1))
st.write("Birthday : ", birthday)


### 날짜의 범위 지정
date_range = st.date_input("Choose start day, end day",
                           value=[datetime.date(2024,3,1), datetime.date(2024,5,30)],
                            min_value=datetime.date(2024,2,1),
                            max_value=datetime.date(2024,6,7))
st.write("Range : ", date_range)


### 시간 입력
st.title("Time input")

alarm_time = st.time_input("Alarm Time", value=datetime.time(7,30))
st.write("Alarm Time : ", alarm_time)


