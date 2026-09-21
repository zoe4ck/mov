import streamlit as st
import pandas as pd
import requests
import html

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import plotly.graph_objects as go


# ============================================================
# 1. 기본 설정
# ============================================================

st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# 2. 영화관 테마 CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 50% 8%,
                rgba(120, 40, 20, 0.22),
                transparent 32%
            ),
            linear-gradient(
                180deg,
                #080809 0%,
                #111217 50%,
                #070708 100%
            );

        color: #f5eee2;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 24px;
        padding-bottom: 40px;
    }


    /* ========================================================
       빨간 영화관 커튼
       ======================================================== */

    .curtain {
        position: fixed;
        top: 0;
        width: 85px;
        height: 100vh;
        z-index: 999;
        pointer-events: none;

        background:
            repeating-linear-gradient(
                90deg,
                #250003 0px,
                #520007 16px,
                #8b111b 32px,
                #a61c26 43px,
                #560007 60px,
                #250003 82px
            );

        opacity: 0.9;

        box-shadow:
            0 0 25px rgba(0, 0, 0, 0.7);
    }

    .curtain.left {
        left: 0;
        border-right: 2px solid #a67a36;
        border-radius: 0 0 45px 0;
    }

    .curtain.right {
        right: 0;
        border-left: 2px solid #a67a36;
        border-radius: 0 0 0 45px;
    }


    /* ========================================================
       극장 간판
       ======================================================== */

    .cinema-sign {
        max-width: 950px;

        margin:
            5px
            auto
            28px
            auto;

        text-align: center;

        padding:
            20px
            30px;

        background:
            linear-gradient(
                145deg,
                #261a0c,
                #080808 50%,
                #26190a
            );

        border:
            2px solid
            #c49748;

        border-radius: 18px;

        box-shadow:
            0 0 0 4px #090806,
            0 0 0 6px #513b1c,
            0 15px 50px rgba(0, 0, 0, 0.7);
    }

    .bulbs {
        color: #efc15d;
        font-size: 10px;
        letter-spacing: 8px;
        text-shadow: 0 0 8px #e6a933;
    }

    .sign-small {
        color: #d3ae67;
        font-size: 12px;
        letter-spacing: 5px;
        margin-top: 6px;
    }

    .sign-title {
        color: #f4ca6c;

        font-size:
            clamp(34px, 5vw, 64px);

        font-weight: 900;
        letter-spacing: 2px;

        margin:
            2px
            0;

        text-shadow:
            0 2px 0 #79521b,
            0 0 15px rgba(255, 190, 70, 0.3);
    }

    .sign-subtitle {
        color: #b9aa91;
        font-size: 12px;
        letter-spacing: 3px;
    }


    /* ========================================================
       필름 프레임
       ======================================================== */

    .film-frame {
        position: relative;

        background:
            linear-gradient(
                145deg,
                #141b21,
                #06090c
            );

        border:
            1px solid
            #97702f;

        border-radius: 14px;

        padding: 27px;

        box-shadow:
            0 0 0 4px #070707,
            0 0 0 5px #493519,
            0 15px 40px rgba(0, 0, 0, 0.45);

        overflow: hidden;
    }

    .film-frame::before,
    .film-frame::after {
        content: "";

        position: absolute;

        left: 10px;
        right: 10px;

        height: 8px;

        background:
            repeating-linear-gradient(
                90deg,
                #b58a43 0px,
                #b58a43 11px,
                transparent 11px,
                transparent 24px
            );

        opacity: 0.45;
    }

    .film-frame::before {
        top: 7px;
    }

    .film-frame::after {
        bottom: 7px;
    }


    /* ========================================================
       1위 영화
       ======================================================== */

    .rank-label {
        color: #f1c76a;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .rank-badge {
        display: inline-flex;

        width: 46px;
        height: 46px;

        align-items: center;
        justify-content: center;

        margin-right: 8px;

        border-radius: 50%;

        background:
            linear-gradient(
                145deg,
                #f5d37b,
                #99651e
            );

        color: #1c1208;

        font-size: 19px;
        font-weight: 900;

        box-shadow:
            0 0 0 3px #2d1d0b,
            0 0 0 4px #b4873b;
    }

    .movie-title {
        color: white;

        font-size:
            clamp(25px, 3vw, 42px);

        font-weight: 900;

        margin:
            12px
            0
            8px;
    }

    .movie-date {
        color: #bdb19e;
        font-size: 13px;
        margin-bottom: 15px;
    }


    /* ========================================================
       지표 카드
       ======================================================== */

    .metric-card {
        min-height: 125px;

        padding: 18px;

        border-radius: 12px;

        background:
            linear-gradient(
                145deg,
                #24252b,
                #0d0e12
            );

        border:
            1px solid
            #69532d;

        box-shadow:
            0 8px 20px rgba(0, 0, 0, 0.3);
    }

    .metric-icon {
        font-size: 22px;
    }

    .metric-label {
        color: #aaa095;
        font-size: 12px;
        margin: 6px 0;
    }

    .metric-value {
        color: #f7f0e5;
        font-size: 22px;
        font-weight: 900;
    }


    /* ========================================================
       토마토 평점
       ======================================================== */

    .tomato-card {
        margin-top: 17px;

        padding:
            17px
            20px;

        background:
            linear-gradient(
                135deg,
                #4b1111,
                #120809
            );

        border:
            1px solid
            #833d35;

        border-radius: 12px;
    }

    .tomato-label {
        color: #e8bd62;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2px;
    }

    .tomato-icons {
        font-size: 25px;
        letter-spacing: 2px;
        margin: 5px 0;
    }

    .tomato-score {
        color: #d2c5b2;
        font-size: 12px;
    }


    /* ========================================================
       섹션 제목
       ======================================================== */

    .section-title {
        display: flex;

        align-items: center;

        gap: 12px;

        margin:
            32px
            0
            15px;

        color: #efc66b;

        font-size: 22px;

        font-weight: 900;
    }

    .section-line {
        flex: 1;

        height: 1px;

        background:
            linear-gradient(
                90deg,
                #a27a38,
                transparent
            );
    }


    /* ========================================================
       추가 지표 카드
       ======================================================== */

    .info-card {
        padding: 19px;

        margin-top: 18px;

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #431313,
                #120809
            );

        border:
            1px solid
            #7e3a32;
    }

    .info-title {
        color: #e3b85e;

        font-size: 12px;

        font-weight: 800;

        letter-spacing: 2px;
    }

    .info-value {
        color: #fff0d1;

        font-size: 30px;

        font-weight: 900;

        margin: 4px 0;
    }

    .info-text {
        color: #bdb09d;

        font-size: 12px;

        line-height: 1.7;
    }


    /* ========================================================
       영화 티켓
       ======================================================== */

    .ticket {
        position: relative;

        margin-top: 24px;

        padding: 20px;

        color: #25170a;

        background:
            linear-gradient(
                135deg,
                #c99c52,
                #f0d99a,
                #b77e31
            );

        border-radius: 8px;

        box-shadow:
            0 12px 25px rgba(0, 0, 0, 0.35);
    }

    .ticket-small {
        font-size: 10px;
        letter-spacing: 3px;
        opacity: 0.7;
    }

    .ticket-title {
        font-size: 23px;
        font-weight: 900;
        margin: 6px 0;
    }

    .ticket-text {
        font-size: 12px;
        line-height: 1.7;
    }


    /* ========================================================
       하단 필름 스트립
       ======================================================== */

    .film-strip {
        min-height: 70px;

        margin-top: 38px;

        display: flex;

        align-items: center;

        justify-content: center;

        text-align: center;

        background:
            repeating-linear-gradient(
                90deg,
                #101010 0px,
                #101010 65px,
                #282828 65px,
                #282828 125px
            );

        border-top:
            8px dotted
            #a67c37;

        border-bottom:
            8px dotted
            #a67c37;

        color: #e4bb62;

        font-size: 17px;

        font-weight: 900;

        letter-spacing: 2px;
    }


    /* ========================================================
       입력창
       ======================================================== */

    div[data-testid="stTextInput"] input {
        background: #101319 !important;
        color: #f4eee4 !important;
        border-color: #67502a !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #101319 !important;
        color: #f4eee4 !important;
        border-color: #67502a !important;
    }


    /* ========================================================
       버튼
       ======================================================== */

    .stButton > button {
        background:
            linear-gradient(
                145deg,
                #721018,
                #39060a
            );

        color: #f5dfb2;

        border:
            1px solid
            #9c7130;

        border-radius: 8px;

        font-weight: 700;
    }


    /* ========================================================
       모바일
       ======================================================== */

    @media (max-width: 900px) {

        .curtain {
            width: 28px;
        }

        .block-container {
            padding-left: 38px;
            padding-right: 38px;
        }
    }

    </style>

    <div class="curtain left"></div>
    <div class="curtain right"></div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. 한국 시간 기준 '어제' 계산
# ============================================================
# Streamlit Cloud 서버 시간이 한국 시간이 아닐 수 있으므로
# 반드시 Asia/Seoul 시간대를 사용합니다.

KST = ZoneInfo("Asia/Seoul")

now_kst = datetime.now(KST)

yesterday = now_kst - timedelta(days=1)

target_date = yesterday.strftime("%Y%m%d")

display_date = yesterday.strftime("%Y년 %m월 %d일")

weekday_names = [
    "월",
    "화",
    "수",
    "목",
    "금",
    "토",
    "일",
]

weekday = weekday_names[yesterday.weekday()]


# ============================================================
# 4. KOBIS API 주소
# ============================================================

API_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)


# ============================================================
# 5. 극장 간판
# ============================================================

st.markdown(
    f"""
    <div class="cinema-sign">

        <div class="bulbs">
            ●　●　●　●　●　●　●　●　●
        </div>

        <div class="sign-small">
            KOREA BOX OFFICE
        </div>

        <div class="sign-title">
            어제의 박스오피스
        </div>

        <div class="sign-subtitle">
            {display_date} ({weekday}) 기준 · KOBIS DAILY BOX OFFICE
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 6. Secrets에서 KOBIS 인증키 가져오기
# ============================================================

try:

    KOBIS_KEY = st.secrets["KOBIS_KEY"]

except Exception:

    st.error(
        "🔐 KOBIS 인증키를 불러오지 못했습니다."
    )

    st.info(
        """
        ### 확인해 주세요

        Streamlit Cloud의

        **Settings → Secrets**

        에 다음과 같이 등록했는지 확인하세요.

        ```toml
        KOBIS_KEY = "본인의_KOBIS_인증키"
        ```

        이름은 반드시 `KOBIS_KEY`여야 합니다.
        """
    )

    st.stop()


# ============================================================
# 7. KOBIS API 요청 함수
# ============================================================

@st.cache_data(ttl=3600)
def get_box_office(api_key, date):

    params = {
        "key": api_key,
        "targetDt": date,
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# 8. API 요청 실행
# ============================================================

try:

    data = get_box_office(
        KOBIS_KEY,
        target_date,
    )

except requests.exceptions.Timeout:

    st.error(
        "⏰ KOBIS 서버의 응답 시간이 초과되었습니다."
    )

    st.info(
        """
        **확인할 내용**

        - 인터넷 연결 상태를 확인해 주세요.
        - 잠시 후 새로고침해 주세요.
        - KOBIS 서버가 일시적으로 응답하지 않을 수 있습니다.
        """
    )

    st.stop()


except requests.exceptions.ConnectionError:

    st.error(
        "🌐 KOBIS API에 연결하지 못했습니다."
    )

    st.info(
        """
        **확인할 내용**

        - 인터넷 연결 상태를 확인해 주세요.
        - KOBIS API 서버가 정상적으로 작동하는지 확인해 주세요.
        - 잠시 후 다시 실행해 주세요.
        """
    )

    st.stop()


except requests.exceptions.HTTPError as error:

    st.error(
        "🚨 KOBIS API에서 HTTP 오류가 발생했습니다."
    )

    st.info(
        f"오류 정보: `{error}`"
    )

    st.stop()


except requests.exceptions.RequestException:

    st.error(
        "⚠️ KOBIS API 요청에 실패했습니다."
    )

    st.info(
        "네트워크 연결이나 KOBIS API 상태를 확인해 주세요."
    )

    st.stop()


except ValueError:

    st.error(
        "⚠️ KOBIS에서 올바른 JSON 데이터를 받지 못했습니다."
    )

    st.info(
        "잠시 후 다시 실행해 주세요."
    )

    st.stop()


# ============================================================
# 9. KOBIS 자체 오류 확인
# ============================================================
# 인증키가 잘못되어도 HTTP 상태코드가 200일 수 있기 때문에
# faultInfo를 따로 확인합니다.

if "faultInfo" in data:

    fault_info = data.get(
        "faultInfo",
        {},
    )

    error_code = fault_info.get(
        "errorCode",
        "",
    )

    error_message = fault_info.get(
        "message",
        "KOBIS API에서 오류가 발생했습니다.",
    )

    st.error(
        "🚨 KOBIS API에서 오류가 발생했습니다."
    )

    if error_code:

        st.write(
            f"**오류 코드:** {error_code}"
        )

    st.write(
        f"**오류 내용:** {error_message}"
    )

    st.info(
        """
        ### 확인할 내용

        1. Streamlit Secrets의 `KOBIS_KEY`가 정확한지 확인
        2. 인증키 앞뒤에 불필요한 공백이 없는지 확인
        3. KOBIS에서 발급받은 인증키가 정상적으로 활성화되어 있는지 확인
        4. 잠시 후 다시 실행
        """
    )

    st.stop()


# ============================================================
# 10. 응답 구조 확인
# ============================================================

if "boxOfficeResult" not in data:

    st.error(
        "⚠️ 박스오피스 데이터를 찾을 수 없습니다."
    )

    st.info(
        """
        KOBIS API의 응답 구조가 예상과 다릅니다.

        잠시 후 다시 실행하거나
        KOBIS API 상태를 확인해 주세요.
        """
    )

    st.stop()


box_office_result = data["boxOfficeResult"]


# ============================================================
# 11. 영화 목록 가져오기
# ============================================================

movie_list = box_office_result.get(
    "dailyBoxOfficeList",
    [],
)


if not movie_list:

    st.warning(
        "🎬 해당 날짜의 박스오피스 영화 목록이 없습니다."
    )

    st.info(
        f"""
        ### 확인할 내용

        **조회 날짜:** {display_date}

        - KOBIS에서 해당 날짜의 데이터가 아직 제공되지 않았을 수 있습니다.
        - KOBIS API가 정상적으로 데이터를 반환하는지 확인해 주세요.
        - 인증키가 정상적으로 등록되어 있는지도 확인해 주세요.
        - 잠시 후 다시 실행해 보세요.
        """
    )

    st.stop()


# ============================================================
# 12. API 데이터를 DataFrame으로 변환
# ============================================================

rows = []


for movie in movie_list:

    try:
        rank = int(
            movie.get(
                "rank",
                0,
            )
        )
    except (TypeError, ValueError):
        rank = 0


    try:
        rank_inten = int(
