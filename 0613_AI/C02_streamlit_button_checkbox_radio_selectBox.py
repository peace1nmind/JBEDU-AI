"""
[ streamlit (input) ]

streamlit 버튼, 체크박스, 라디오버튼, 콤보박스


"""


#####   라이브러리

# 외부
import streamlit as st



#####   streamlit

### 버튼
st.title("Button")
button_clicked = st.button("Button1")
st.write("Button1 button_clicked status: ", button_clicked)

if button_clicked:
    st.write("Button1 is button_clicked")
else:
    st.write("Button1 is not button_clicked")


### 체크박스
st.title("CheckBox")
checkbox_clicked = st.checkbox("CheckBox1")
st.write("CheckBox1 clicked status: ", checkbox_clicked)


### 라디오버튼
st.title("Radio Button")
radio_op1 = [i for i in range(10, 41, 10)]
radio1_selected = st.radio("Q1. 5x5+5 = ?", radio_op1)
st.write("Answer: ", radio1_selected)

radio_op2 = ['마라톤', '축구', '수영', '발레']
radio2_selected = st.radio("Q2. choose your favorite sports", 
                           radio_op2)
st.write("Answer: ", radio2_selected) 


### 콤보박스
st.title("ComboBox")
combo_op = ['하이든', '모짜르트', '베토벤', 'BTS']
combo1_selected = st.selectbox("Q3. choose your favorite musician",
                               combo_op)
st.write("Answer: ", combo1_selected)


