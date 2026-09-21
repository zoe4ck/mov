import streamlit as st
import pandas as pd
import requests
import html

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import plotly.graph_objects as go


# ============================================================
# 1. 페이지 기본 설정
# ============================================================

st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. 영화관 느낌의 전체 디자인
# ============================================================
# Streamlit 기본 디자인 위에 CSS를 입혀서
# 영화관의 커튼, 필름, 간판, 티켓 느낌을 만듭니다.

st.markdown(
    """
    <style>

    /* ========================================================
       전체 배경
       ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 50% 10%,
                rgba(124, 47, 20, 0.25),
                transparent 32%
            ),
            radial-gradient(
                circle at 50% 70%,
                rgba(30, 45, 60, 0.16),
                transparent 40%
            ),
            linear-gradient(
                180deg,
                #080809 0%,
                #101116 45%,
                #070708 100%
            );

        color: #f4eee3;
    }


    /* ========================================================
       Streamlit 기본 요소 숨기기
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ========================================================
       화면 기본 여백
       ======================================================== */

    .block-container {
        max-width: 1450px;
        padding-top: 25px;
        padding-bottom: 40px;
    }


    /* ========================================================
       빨간 벨벳 커튼
       ======================================================== */

    .curtain-left,
    .curtain-right {
        position: fixed;

        top: 0;

        width: 105px;
        height: 100vh;

        z-index: 9999;

        pointer-events: none;

        opacity: 0.93;
    }


    .curtain-left {

        left: 0;

        background:
            repeating-linear-gradient(
                90deg,

                #250003 0px,
                #4c0008 15px,
                #810c14 32px,
                #a31b25 43px,
                #5b0008 62px,
                #270003 88px
            );

        border-right: 2px solid #9f7736;

        border-radius:
            0
            0
            55px
            0;

        box-shadow:
            inset -22px 0 35px rgba(0,0,0,0.8),
            10px 0 30px rgba(0,0,0,0.4);
    }


    .curtain-right {

        right: 0;

        background:
            repeating-linear-gradient(
                90deg,

                #270003 0px,
                #5b0008 20px,
                #a31b25 42px,
                #810c14 55px,
                #4c0008 75px,
                #250003 100px
            );

        border-left: 2px solid #9f7736;

        border-radius:
            0
            0
            0
            55px;

        box-shadow:
            inset 22px 0 35px rgba(0,0,0,0.8),
            -10px 0 30px rgba(0,0,0,0.4);
    }


    /* 커튼을 묶어 놓은 부분 */

    .curtain-tie-left,
    .curtain-tie-right {

        position: fixed;

        top: 190px;

        width: 42px;
        height: 125px;

        z-index: 10000;

        pointer-events: none;

        background:
            linear-gradient(
                90deg,
                #65050c,
                #b11d27,
                #65050c
            );

        border: 2px solid #c49b4e;

        box-shadow:
            0 0 18px rgba(0,0,0,0.7);
    }


    .curtain-tie-left {

        left: 68px;

        border-radius:
            0
            18px
            18px
            0;
    }


    .curtain-tie-right {

        right: 68px;

        border-radius:
            18px
            0
            0
            18px;
    }


    /* ========================================================
       극장 간판
       ======================================================== */

    .cinema-sign {

        max-width: 950px;

        margin:
            5px
            auto
            30px
            auto;

        text-align: center;

        padding:
            20px
            35px
            23px
            35px;

        background:
            linear-gradient(
                145deg,
                #24190c,
                #090909 48%,
                #26180a
            );

        border:
            2px solid
            #c69645;

        border-radius: 18px;

        box-shadow:
            0 0 0 4px #0c0b08,
            0 0 0 6px #5d431d,
            0 15px 50px rgba(0,0,0,0.75),
            0 0 35px rgba(218,164,72,0.16);
    }


    .sign-bulbs {

        color: #edc15e;

        font-size: 10px;

        letter-spacing: 9px;

        margin-bottom: 7px;

        text-shadow:
            0 0 8px #e8ae3d;
    }


    .sign-small {

        color: #d5b36d;

        font-size: 12px;

        letter-spacing: 6px;

        margin-bottom: 5px;
    }


    .sign-title {

        margin: 0;

        color: #f3c96d;

        font-size:
            clamp(
                34px,
                5vw,
                65px
            );

        font-weight: 900;

        letter-spacing: 2px;

        text-shadow:
            0 2px 0 #79531e,
            0 0 15px rgba(255,195,83,0.35);
    }


    .sign-subtitle {

        margin-top: 7px;

        color: #bcae92;

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
                rgba(19,25,31,0.98),
                rgba(5,8,11,0.98)
            );

        border:
            1px solid
            #9b7130;

        border-radius: 14px;

        padding: 27px;

        box-shadow:
            0 0 0 4px #070707,
            0 0 0 5px #493519,
            0 15px 45px rgba(0,0,0,0.45);

        overflow: hidden;
    }


    /* 위쪽 필름 구멍 */

    .film-frame::before {

        content: "";

        position: absolute;

        left: 10px;
        right: 10px;
        top: 7px;

        height: 8px;

        background:
            repeating-linear-gradient(
                90deg,
                #b58943 0px,
                #b58943 11px,
                transparent 11px,
                transparent 24px
            );

        opacity: 0.5;
    }


    /* 아래쪽 필름 구멍 */

    .film-frame::after {

        content: "";

        position: absolute;

        left: 10px;
        right: 10px;
        bottom: 7px;

        height: 8px;

        background:
            repeating-linear-gradient(
                90deg,
                #b58943 0px,
                #b58943 11px,
                transparent 11px,
                transparent 24px
            );

        opacity: 0.5;
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
            15px
            0;

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
       1위 영화 영역
       ======================================================== */

    .rank-one-label {

        display: inline-flex;

        align-items: center;

        gap: 8px;

        color: #f2c663;

        font-size: 13px;

        font-weight: 800;

        letter-spacing: 1px;

        margin-bottom: 8px;
    }


    .rank-one-badge {

        display: inline-flex;

        justify-content: center;

        align-items: center;

        width: 48px;
        height: 48px;

        border-radius: 50%;

        background:
            linear-gradient(
                145deg,
                #f6d37a,
                #99651d
            );

        color: #1c1208;

        font-size: 19px;

        font-weight: 900;

        box-shadow:
            0 0 0 3px #2e1e0b,
            0 0 0 4px #b78b3f;
    }


    .movie-title {

        margin:
            3px
            0
            10px
            0;

        color: #ffffff;

        font-size:
            clamp(
                25px,
                3vw,
                42px
            );

        font-weight: 900;
    }


    .movie-date {

        color: #bfb3a0;

        font-size: 13px;

        margin-bottom: 15px;
    }


    /* ========================================================
       지표 카드
       ======================================================== */

    .metric-card {

        min-height: 130px;

        padding: 18px;

        border-radius: 12px;

        background:
            linear-gradient(
                145deg,
                rgba(35,36,42,0.98),
                rgba(11,11,15,0.98)
            );

        border:
            1px solid
            #69532c;

        box-shadow:
            inset 0 0 20px rgba(255,255,255,0.025),
            0 8px 22px rgba(0,0,0,0.3);
    }


    .metric-icon {

        font-size: 22px;

        margin-bottom: 6px;
    }


    .metric-label {

        color: #aaa095;

        font-size: 12px;

        margin-bottom: 5px;
    }


    .metric-value {

        color: #f6f0e6;

        font-size: 23px;

        font-weight: 900;
    }


    /* ========================================================
       토마토 평점
       ======================================================== */

    .tomato-card {

        margin-top: 17px;

        padding: 17px 20px;

        background:
            linear-gradient(
                135deg,
                rgba(75,17,17,0.95),
                rgba(18,8,9,0.98)
            );

        border:
            1px solid
            #833d35;

        border-radius: 12px;

        box-shadow:
            inset 0 0 25px rgba(180,40,20,0.04);
    }


    .tomato-label {

        color: #e8bd62;

        font-size: 11px;

        font-weight: 800;

        letter-spacing: 2px;

        margin-bottom: 5px;
    }


    .tomato-icons {

        font-size: 25px;

        letter-spacing: 3px;

        margin: 3px 0;
    }


    .tomato-score {

        color: #d7c8b1;

        font-size: 12px;
    }


    /* ========================================================
       흥행 온도
       ======================================================== */

    .heat-card {

        padding: 20px;

        margin-top: 18px;

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                rgba(71,18,18,0.9),
                rgba(18,8,8,0.97)
            );

        border:
            1px solid
            #813a34;
    }


    .heat-label {

        color: #e4b65b;

        font-size: 12px;

        font-weight: 800;

        letter-spacing: 2px;
    }


    .heat-value {

        color: #fff0d1;

        font-size: 34px;

        font-weight: 900;

        margin: 3px 0;
    }


    .heat-text {

        color: #bdb09c;

        font-size: 12px;

        line-height: 1.6;
    }


    /* ========================================================
       영화 티켓
       ======================================================== */

    .ticket {

        position: relative;

        padding: 20px;

        margin-top: 20px;

        color: #24170a;

        background:
            linear-gradient(
                135deg,
                #c99c52,
                #f1d99b,
                #b77e31
            );

        border-radius: 8px;

        box-shadow:
            0 12px 25px rgba(0,0,0,0.35);
    }


    .ticket::before,
    .ticket::after {

        content: "";

        position: absolute;

        width: 21px;
        height: 21px;

        top: 50%;

        transform:
            translateY(-50%);

        border-radius: 50%;

        background: #09090a;
    }


    .ticket::before {
        left: -11px;
    }


    .ticket::after {
        right: -11px;
    }


    .ticket-small {

        font-size: 10px;

        letter-spacing: 3px;

        opacity: 0.7;
    }


    .ticket-title {

        font-size: 23px;

        font-weight: 900;

        margin:
            6px
            0;
    }


    .ticket-text {

        font-size: 12px;

        line-height: 1.7;
    }


    /* ========================================================
       필름 스트립 하단
       ======================================================== */

    .film-strip {

        min-height: 70px;

        margin-top: 40px;

        display: flex;

        justify-content: center;

        align-items: center;

        text-align: center;

        background:
            repeating-linear-gradient(
                90deg,
                #101010 0px,
                #101010 65px,
                #272727 65px,
                #272727 125px
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
       검색창
       ======================================================== */

    div[data-testid="stTextInput"] input {

        background:
            #101319 !important;

        color:
            #f4eee4 !important;

        border:
            1px solid
            #67502a !important;

        border-radius:
            8px !important;
    }


    /* ========================================================
       버튼
       ======================================================== */

    .stButton > button {

        background:
            linear-gradient(
                145deg,
                #6f1018,
                #39060a
            );

        color: #f5dfb2;

        border:
            1px solid
            #9c7130;

        border-radius: 8px;

        font-weight: 700;
    }


    .stButton > button:hover {

        border-color:
            #e0b65d;

        color:
            #ffffff;
    }


    /* ========================================================
       데이터프레임
       ======================================================== */

    div[data-testid="stDataFrame"] {

        border:
            1px solid
            #5e4827;

        border-radius:
            10px;

        overflow:
            hidden;
    }


    /* ========================================================
       모바일 대응
       ======================================================== */

    @media (max-width: 900px) {

        .curtain-left,
        .curtain-right {

            width: 35px;
        }

        .curtain-tie-left {

            left: 18px;
        }

        .curtain-tie-right {

            right: 18px;
        }

        .block-container {

            padding-left: 45px;
            padding-right: 45px;
        }
    }

    </style>


    <!-- 영화관 커튼 -->
    <div class="curtain-left"></div>
    <div class="curtain-right"></div>

    <!-- 커튼 묶음 -->
    <div class="curtain-tie-left"></div>
    <div class="curtain-tie-right"></div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. 한국 시간 기준으로 '어제' 계산
# ============================================================
# Streamlit Cloud 서버의 시간은 한국 시간이 아닐 수 있습니다.
# 따라서 반드시 Asia/Seoul 시간대를 사용합니다.

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
    "일"
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

        <div class="sign-bulbs">
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
    unsafe_allow_html=True
)


# ============================================================
# 6. KOBIS 인증키 가져오기
# ============================================================
# 실제 인증키는 절대로 코드에 작성하지 않습니다.
# Streamlit Cloud의 Secrets에서 가져옵니다.

try:

    KOBIS_KEY = st.secrets["KOBIS_KEY"]

except Exception:

    st.error(
        "🔐 KOBIS 인증키를 불러오지 못했습니다."
    )

    st.info(
        """
        ### 확인할 내용

        Streamlit Cloud에서

        **Settings → Secrets**

        로 들어가서 아래와 같이 등록했는지 확인하세요.

        ```toml
        KOBIS_KEY = "본인의_KOBIS_인증키"
        ```

        인증키 이름은 반드시 **KOBIS_KEY**여야 합니다.
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
