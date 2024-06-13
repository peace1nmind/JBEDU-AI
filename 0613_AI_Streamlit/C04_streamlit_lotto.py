"""
[ streamlit ]

로또 생성기


"""


#####   라이브러리

# 내장
import random
import datetime

# 외부
import streamlit as st



#####   streamlit

### lotto

# 로또 생성 함수
def generate_lotto():
    lotto = []

    while len(lotto) < 6:
        lottoNum = str(random.randint(1, 45))
        lotto.append(lottoNum.zfill(2))
    
    lotto.sort()

    return lotto

# 로또 번호 표기
st.title("Lotto Generator")

button = st.button("Make Lotto")

if button:
    for i in range(1, 6):
        lotto_numbers = generate_lotto()
        lotto_numbers = ', '.join(map(str, lotto_numbers))
        st.subheader(f"No.{i} Lucky Num : {lotto_numbers}")
    st.write(f"Generated Time : {datetime.datetime.now().strftime('%Y-%m-%d  %H:%M')}")


