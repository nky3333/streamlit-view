import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# 데이터프레임은 이미 코랩 안에 있음
# 이제 스트림릿 애플리케이션을 설정하고 사용할 것입니다.
df = pd.read_csv('data.csv') 
# 스트림릿 애플리케이션 설정
st.title('학교별 하복 + 동복 (평균)가격 그래프')

# 년도, 시도교육청, 학교급코드 선택 위젯 추가
selected_year = st.selectbox('년도 선택', df['년도'].unique())
selected_sido = st.selectbox('시도교육청 선택', df['시도교육청'].unique())
selected_grade = st.selectbox('학교급코드 선택 (3:중등, 4:고등)', df['학교급코드'].unique())

# 선택된 조합에 해당하는 데이터프레임 필터링
subset = df[(df['년도'] == selected_year) & (df['시도교육청'] == selected_sido) & (df['학교급코드'] == selected_grade)].copy()
if not subset.empty:
    # 하복(평균)가격과 동복(평균)가격의 합을 계산하여 정렬
    subset['합산가격'] = subset['하복(평균)가격'] + subset['동복(평균)가격']
    sorted_subset = subset.sort_values(by='합산가격')  # 합산가격 기준으로 정렬
    
    # 합산가격에 대한 막대 그래프 생성
    fig, ax = plt.subplots()
    ax.bar(sorted_subset['학교명'], sorted_subset['합산가격'], label='하복 + 동복')

    # 평균 값 계산
    average_price = sorted_subset['합산가격'].mean()

    # 평균값의 선 추가
    ax.axhline(y=average_price, color='r', linestyle='--', label='평균값')

    # y축 옆에 평균값 표시
    ax.text(0, average_price*1.05, f'평균: {average_price:.2f}', color='r', fontsize=8, va='center')

    # 그래프 제목과 레이블 설정
    ax.set_title(f'{selected_year}년 {selected_sido} {"중학교" if selected_grade == 3 else "고등학교"}')
    ax.set_xlabel('학교명')
    ax.set_ylabel('하복 + 동복 (평균)가격')
    plt.xticks(rotation=90)  # x축 레이블 회전
    plt.tight_layout()  # 그래프 간격 조정
    plt.legend()  # 범례 표시
    st.pyplot(fig)  # 그래프 출력
else:
    st.write('선택된 조합에 해당하는 데이터가 없습니다.')
