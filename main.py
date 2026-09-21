import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


# ============================================================
# 1. 기본 페이지 설정
# ============================================================

st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# 2. 한국 시간 기준으로 '어제' 날짜 계산
# ============================================================
# Streamlit Cloud 서버가 한국 시간이 아닐 수 있기 때문에
# 서버의 현재 시간을 그대로 사용하지 않고 한국 시간(KST)을 지정합니다.

KST = ZoneInfo("Asia/Seoul")

now_kst = datetime.now(KST)
yesterday = now_kst - timedelta(days=1)

# KOBIS API에서 사용하는 날짜 형식: YYYYMMDD
target_date = yesterday.strftime("%Y%m%d")

# 화면에 보여줄 날짜
display_date = yesterday.strftime("%Y년 %m월 %d일")


# ============================================================
# 3. KOBIS API 주소
# ============================================================

API_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)


# ============================================================
# 4. 화면 제목
# ============================================================

st.title("🎬 어제의 박스오피스")
st.caption(f"{display_date} 기준 · KOBIS 일일 박스오피스")


# ============================================================
# 5. 인증키 가져오기
# ============================================================
# 실제 인증키를 코드에 직접 적지 않습니다.
# Streamlit Cloud의 Secrets에 KOBIS_KEY라는 이름으로 저장해야 합니다.
#
# 예:
# KOBIS_KEY = "발급받은_인증키"
#
# 실제 코드에는 인증키를 작성하지 않습니다.

try:
    KOBIS_KEY = st.secrets["KOBIS_KEY"]

except Exception:
    st.error("🔑 KOBIS 인증키를 불러오지 못했습니다.")

    st.info(
        """
        **확인할 내용**

        1. Streamlit Cloud의 앱 설정에서 **Secrets**를 열어 주세요.
        2. 다음과 같은 형식으로 `KOBIS_KEY`를 등록했는지 확인하세요.

        `KOBIS_KEY = "발급받은 인증키"`

        3. 인증키 이름이 정확히 `KOBIS_KEY`인지 확인하세요.
        """
    )

    st.stop()


# ============================================================
# 6. KOBIS API 요청
# ============================================================

params = {
    "key": KOBIS_KEY,
    "targetDt": target_date
}

try:
    response = requests.get(
        API_URL,
        params=params,
        timeout=10
    )

    # HTTP 오류가 발생하면 예외를 발생시킵니다.
    response.raise_for_status()

    # JSON으로 변환합니다.
    data = response.json()

except requests.exceptions.Timeout:
    st.error("⏰ KOBIS API 요청 시간이 초과되었습니다.")

    st.info(
        """
        **확인할 내용**

        - 인터넷 연결 상태를 확인해 주세요.
        - 잠시 후 앱을 새로고침해 주세요.
        - KOBIS 서버가 일시적으로 응답하지 않는 경우에도 이런 문제가 발생할 수 있습니다.
        """
    )

    st.stop()

except requests.exceptions.RequestException:
    st.error("🌐 KOBIS API에 연결하지 못했습니다.")

    st.info(
        """
        **확인할 내용**

        - 인터넷 연결 상태를 확인해 주세요.
        - KOBIS API 주소가 정상적으로 접속되는지 확인해 주세요.
        - 잠시 후 다시 실행해 주세요.
        """
    )

    st.stop()

except ValueError:
    st.error("⚠️ KOBIS에서 정상적인 JSON 데이터를 받지 못했습니다.")

    st.info(
        """
        **확인할 내용**

        - KOBIS API가 일시적으로 오류를 반환했는지 확인해 주세요.
        - 잠시 후 다시 실행해 주세요.
        """
    )

    st.stop()


# ============================================================
# 7. KOBIS API 자체 오류 확인
# ============================================================
# KOBIS는 인증키가 잘못되어도 HTTP 상태코드가 200으로 올 수 있습니다.
# 따라서 response.raise_for_status()만으로는 인증키 오류를 잡을 수 없습니다.
#
# API 응답 안에 faultInfo가 있는지 반드시 확인합니다.

if "faultInfo" in data:

    fault_info = data["faultInfo"]

    # 오류 메시지를 최대한 읽기 쉽게 가져옵니다.
    error_message = fault_info.get(
        "message",
        "KOBIS API에서 오류가 발생했습니다."
    )

    error_code = fault_info.get(
        "errorCode",
        ""
    )

    st.error("🚨 KOBIS API에서 오류가 발생했습니다.")

    if error_code:
        st.write(f"**오류 코드:** {error_code}")

    st.write(f"**오류 내용:** {error_message}")

    st.info(
        """
        **확인할 내용**

        - Streamlit Secrets의 `KOBIS_KEY`가 정확한지 확인하세요.
        - 인증키 앞뒤에 불필요한 공백이 없는지 확인하세요.
        - KOBIS에서 발급받은 인증키가 정상적으로 활성화되어 있는지 확인하세요.
        - API 요청 날짜가 정상적인지 확인하세요.
        """
    )

    st.stop()


# ============================================================
# 8. boxOfficeResult 확인
# ============================================================

if "boxOfficeResult" not in data:

    st.error("⚠️ 예상한 박스오피스 데이터를 찾을 수 없습니다.")

    st.info(
        """
        **확인할 내용**

        - KOBIS API 응답 형식이 정상인지 확인하세요.
        - KOBIS API가 일시적으로 오류를 반환했을 수 있으니 잠시 후 다시 실행하세요.
        """
    )

    st.stop()


box_office_result = data["boxOfficeResult"]


# ============================================================
# 9. 영화 목록 가져오기
# ============================================================

movie_list = box_office_result.get("dailyBoxOfficeList", [])


# 영화 목록이 비어 있는 경우
if not movie_list:

    st.warning("🎬 해당 날짜의 영화 목록이 없습니다.")

    st.info(
        f"""
        **확인할 내용**

        - 조회 날짜: **{display_date}**
        - KOBIS에서 해당 날짜의 일일 박스오피스가 아직 제공되지 않았을 수 있습니다.
        - KOBIS API가 정상적으로 데이터를 반환하는지 확인해 주세요.
        - 인증키가 정상인지도 함께 확인해 주세요.
        """
    )

    st.stop()


# ============================================================
# 10. 필요한 데이터만 표로 만들기
# ============================================================

rows = []

for movie in movie_list:

    rows.append(
        {
            "순위": int(movie.get("rank", 0)),
            "영화명": movie.get("movieNm", "-"),
            "개봉일": movie.get("openDt", "-"),
            "관객수": int(movie.get("audiCnt", 0)),
            "누적관객": int(movie.get("audiAcc", 0)),
            "스크린수": int(movie.get("scrnCnt", 0)),
        }
    )


df = pd.DataFrame(rows)


# ============================================================
# 11. 숫자를 보기 편하게 표시하기 위한 함수
# ============================================================

def number_format(value):
    """숫자에 천 단위 쉼표를 넣어 줍니다."""
    return f"{value:,}"


# ============================================================
# 12. 1위 영화 정보
# ============================================================

first_movie = df.iloc[0]

st.subheader("🏆 1위 영화")

st.markdown(
    f"## {first_movie['영화명']}"
)

# 지표 카드 3개
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="어제 관객수",
        value=f"{number_format(first_movie['관객수'])}명"
    )

with col2:
    st.metric(
        label="누적 관객수",
        value=f"{number_format(first_movie['누적관객'])}명"
    )

with col3:
    st.metric(
        label="스크린수",
        value=f"{number_format(first_movie['스크린수'])}개"
    )


# ============================================================
# 13. 관객수 상위 5편 막대그래프
# ============================================================

st.subheader("📊 관객수 상위 5편")

top5 = df.head(5).copy()

# 영화명을 인덱스로 설정하면 Streamlit에서 막대그래프의
# 가로축에 영화명이 표시됩니다.
chart_data = top5.set_index("영화명")[["관객수"]]

st.bar_chart(chart_data)


# ============================================================
# 14. 전체 박스오피스 표
# ============================================================

st.subheader("🎥 전체 박스오피스")

display_df = df.copy()

# 화면에서는 숫자에 쉼표를 넣어 읽기 쉽게 표시합니다.
display_df["관객수"] = display_df["관객수"].map(number_format)
display_df["누적관객"] = display_df["누적관객"].map(number_format)
display_df["스크린수"] = display_df["스크린수"].map(number_format)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 15. 데이터 기준 안내
# ============================================================

st.caption(
    f"※ 데이터 기준일: {display_date} · "
    "출처: 영화관입장권통합전산망(KOBIS)"
)
