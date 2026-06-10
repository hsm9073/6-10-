import streamlit as st
import pandas as pd

st.set_page_config(page_title="봄·가을이 정말 짧아지고 있는가?", layout="wide")

st.title("🌸🍂 봄·가을이 정말 짧아지고 있는가?")
st.write("""
서울의 장기간 기온 데이터를 이용하여
봄과 가을의 길이가 실제로 짧아지고 있는지 살펴봅니다.
""")

# 데이터 불러오기
df = pd.read_csv("ta_20260601093156.csv")

# 날짜 처리
df["날짜"] = pd.to_datetime(df["날짜"].astype(str).str.strip())
df["연도"] = df["날짜"].dt.year

# 계절 구분 기준
# 봄 : 평균기온 10~20℃
# 여름 : 평균기온 20℃ 초과
# 가을 : 평균기온 10~20℃
# 겨울 : 평균기온 10℃ 미만

def classify(temp):
    if temp < 10:
        return "겨울"
    elif temp <= 20:
        return "봄·가을"
    else:
        return "여름"

df["계절구분"] = df["평균기온(℃)"].apply(classify)

# 연도별 봄·가을 일수 계산
season_days = (
    df[df["계절구분"] == "봄·가을"]
    .groupby("연도")
    .size()
    .reset_index(name="봄·가을 일수")
)

st.header("연도별 봄·가을 일수")

st.line_chart(
    season_days.set_index("연도")
)

st.dataframe(season_days)

# 최근 30년 비교
st.header("최근 변화 살펴보기")

recent = season_days[season_days["연도"] >= season_days["연도"].max() - 30]

st.line_chart(
    recent.set_index("연도")
)

# 통계
old_period = season_days[
    (season_days["연도"] >= 1910) &
    (season_days["연도"] < 1940)
]["봄·가을 일수"]

new_period = season_days[
    season_days["연도"] >= season_days["연도"].max() - 30
]["봄·가을 일수"]

st.header("비교 결과")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "과거 평균 (1910~1939)",
        f"{old_period.mean():.1f}일"
    )

with col2:
    st.metric(
        f"최근 평균 ({season_days['연도'].max()-30}~{season_days['연도'].max()})",
        f"{new_period.mean():.1f}일"
    )

difference = new_period.mean() - old_period.mean()

if difference < 0:
    st.success(
        f"최근 봄·가을 일수가 평균 {abs(difference):.1f}일 감소했습니다."
    )
else:
    st.info(
        f"최근 봄·가을 일수가 평균 {difference:.1f}일 증가했습니다."
    )

st.header("결론")

st.write("""
이 분석에서는 평균기온이 10℃ 이상 20℃ 이하인 날을
봄·가을로 정의하였다.

그래프와 평균값을 통해 시간이 지남에 따라
봄·가을 기간이 변화하는지 확인할 수 있다.
""")
