"""
[ streamlit (img) ]

streamlit 이미지 표시


"""


##### 라이브러리

# 내장
from PIL import Image

# 외부
import streamlit as st



#####   streamlit

st.title("Image")

# 로컬 파일을 열어서 표시
st.subheader("1. Local File")
img_file = Image.open(r"D:\JBEDU\Python\VSCode\VSCode_Workspace\0613_AI\data\avenue.jpg")
st.image(img_file, width=350, caption="컴퓨터 내의 이미지 파일을 열어서 표시한 이미지")

# 웹 상의 이미지를 표시
st.subheader("2. Web")
img_url = ("https://encrypted-tbn0.gstatic.com/" + 
           "images?q=tbn:ANd9GcRNTsrA2DD6DLXI9sYcclUOIa1jiAs6vdSSNw&s")
st.image(img_url, width=350, caption="웹 상의 이미지를 링크를 통해 표시한 이미지")


