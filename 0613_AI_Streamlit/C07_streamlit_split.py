"""
[  ]


"""


#####   라이브러리

# 내장
from PIL import Image

# 외부
import streamlit as st
import pandas as pd



#####   streamlit

st.title("Split Screen")

### 2개로 세로단 분할
st.header("Split 2 part")

factory2 = pd.read_csv("0613_AI/data/공장별_생산현황2.csv", index_col='year')

# 열 2개로 분할 (동일한 너비)
[col1, col2] = st.columns(2)

with col1:
    st.subheader("factory2 data")
    st.dataframe(factory2, width=300)

with col2:
    st.subheader("plot")
    st.line_chart(factory2)


### 3개로 세로단 분할
st.header("Split 3 part")

colums = st.columns([1.2, 1.0, 0.8])

folder = "D:/JBEDU/Python/VSCode/VSCode_Workspace/0613_AI/data/"
img_files = ['dog.png', 'cat.png', 'bird.png']
img_captions= ['Dog', 'Cat', 'Bird']

for i in range(len(colums)):
    with colums[i]:
        st.subheader(img_captions[i])
        img = Image.open(folder+img_files[i])
        st.image(img)
