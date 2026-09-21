import streamlit as st
import pandas as pd
import requests
import html

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import plotly.graph_objects as go


# ============================================================
# 1. Streamlit 기본 설정
# ============================================================

st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# 2. 영화관 느낌을 위한 CSS
# ============================================================

st.markdown(
    """
    <style>

    /* 전체 배경 */
    .stApp {
        background:
            radial-gradient(
                circle at 50% 0%,
                #351414 0%,
                #0b0b0d 38%,
                #050506 100%
            );
        color: #f5eee2;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 25px;
        padding-bottom: 50px;
    }


    /* ========================================================
       영화관 커튼
       ======================================================== */

    .curtain {
        position: fixed;
        top: 0;
        width: 58px;
        height: 100vh;

        z-index: 9999;

        pointer-events: none;

        background:
            repeating-linear-gradient(
                90deg,
                #260005 0px,
                #5c0710 12px,
                #a21c28 24px,
                #5c0710 38px,
                #260005 52px
            );

        box-shadow: 0 0 25px #000;
    }

    .curtain.left {
        left: 0;
        border-right: 2px solid #bd9144;
    }

    .curtain.right {
        right: 0;
        border-left: 2px solid #bd9144;
    }


    /* ========================================================
       영화관 간판
       ======================================================== */

    .sign {
        text-align: center;

        padding: 25px;

        margin: 5px auto 30px;

        max-width: 1000px;

        border: 2px solid #c79a4c;

        border-radius: 16px;

        background:
            linear-gradient(
                145deg,
                #241608,
                #080808,
                #241608
            );

        box-shadow:
            0 0 0 4px #090909,
            0 0 0 6px #59411f,
            0 15px 45px #000;
    }

    .bulbs {
        color: #f0c15d;
        letter-spacing: 8px;
        font-size: 11px;
    }

    .kicker {
        color: #d6b06a;
        letter-spacing: 5px;
        font-size: 12px;
    }

    .title {
        color: #f2cb73;

        font-size: clamp(35px, 5vw, 65px);

        font-weight: 900;

        text-shadow: 0 0 18px #6e4915;
    }

    .subtitle {
        color: #aaa092;
        font-size: 13px;
        letter-spacing: 2px;
    }


    /* ========================================================
       필름 프레임
       ======================================================== */

    .film {
        padding: 28px;

        border-radius: 14px;

        position: relative;

        overflow: hidden;

        background:
            linear-gradient(
                145deg,
                #17181d,
                #07080a
            );

        border: 1px solid #8d692f;

        box-shadow:
            0 0 0 4px #070707,
            0 0 0 5px #473619,
            0 15px 40px #0008;
    }

    .film:before,
    .film:after {
        content: "";

        position: absolute;

        left: 12px;
        right: 12px;

        height: 7px;

        background:
            repeating-linear-gradient(
                90deg,
                #b4883d 0px,
                #b4883d 12px,
                transparent 12px,
                transparent 26px
            );

        opacity: 0.5;
    }

    .film:before {
        top: 7px;
    }

    .film:after {
        bottom: 7px;
    }


    /* ========================================================
       영화 제목
       ======================================================== */

    .movie-rank {
        color: #f0c768;
        font-size: 14px;
        font-weight: 800;
    }

    .movie-title {
        color: white;

        font-size: clamp(27px, 3vw, 44px);

        font-weight: 900;

        margin: 12px 0 7px;
    }

    .movie-date {
        color: #aaa096;

        font-size: 13px;

        margin-bottom: 18px;
    }


    /* ========================================================
       지표 카드
       ======================================================== */

    .metric {
        min-height: 120px;

        padding: 17px;

        border-radius: 11px;

        background:
            linear-gradient(
                145deg,
                #26272d,
                #0d0e12
            );

        border: 1px solid #65502d;
    }

    .metric-icon {
        font-size: 21px;
    }

    .metric-label {
        color: #aaa096;
        font-size: 12px;
        margin: 6px 0;
    }

    .metric-value {
        color: #fff4df;
        font-size: 21px;
        font-weight: 900;
    }


    /* ========================================================
       토마토 평점
       ======================================================== */

    .tomato {
        margin-top: 17px;

        padding: 17px 20px;

        border-radius: 11px;

        background:
            linear-gradient(
                135deg,
                #451012,
                #100708
            );

        border: 1px solid #7c3832;
    }

    .tomato-label {
        color: #e9bf61;

        font-size: 11px;

        font-weight: 800;

        letter-spacing: 2px;
    }

    .tomato-icons {
        font-size: 25px;

        margin: 5px 0;
    }

    .tomato-score {
        color: #bcb0a0;
        font-size: 12px;
    }


    /* ========================================================
       섹션 제목
       ======================================================== */

    .section {
        display: flex;

        align-items: center;

        gap: 12px;

        margin: 32px 0 15px;

        color: #efc66b;

        font-size: 22px;

        font-weight: 900;
    }

    .line {
        height: 1px;

        flex: 1;

        background:
            linear-gradient(
                90deg,
                #9e7837,
                transparent
            );
    }


    /* ========================================================
       추가 지표
       ======================================================== */

    .info {
        padding: 19px;

        margin-top: 18px;

        border-radius: 11px;

        background:
            linear-gradient(
                135deg,
                #421113,
                #100708
            );

        border: 1px solid #733730;
    }

    .info-label {
        color: #e2b95e;

        font-size: 11px;

        font-weight: 800;

        letter-spacing: 2px;
    }

    .info-value {
        color: #fff0d1;

        font-size: 28px;

        font-weight: 900;

        margin: 5px 0;
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
        margin-top: 30px;

        padding: 20px;

        border-radius: 8px;

        color: #241608;

        background:
            linear-gradient(
                135deg,
                #b98232,
                #f0d99b,
                #bd8535
            );
    }

    .ticket-small {
        font-size: 10px;

        letter-spacing: 3px;

        opacity: 0.75;
    }

    .ticket-title {
        font-size: 23px;

        font-weight: 900;

        margin: 5px 0;
    }

    .ticket-text {
        font-size: 12px;

        line-height: 1.8;
    }


    /* ========================================================
       필름 스트립
       ======================================================== */

    .film-strip {
        margin-top: 35px;

        padding: 22px;

        text-align: center;

        border-top: 7px dotted #a47b36;

        border-bottom: 7px dotted #a47b36;

        background: #121212;

        color: #e0b65d;

        font-weight: 900;

        letter-spacing: 2px;
    }


    /* 모바일 */
    @media (max-width: 900px) {

        .curtain {
            width: 24px;
        }

        .block-container {
            padding-left: 35px;
            padding-right: 35px;
        }
    }

    </style>


    <div class="curtain left"></div>
    <div class="curtain right"></div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. 한국 시간 기준으로 '어제' 계산
# ============================================================

KST = ZoneInfo("Asia/Seoul")

now_kst = datetime.now(KST)

yesterday = now_kst - timedelta(days=1)

target_dt = yesterday.strftime("%Y%m%d")

display_date = yesterday.strftime("%Y년 %m월 %d일")

weekday_list = [
    "월",
    "화",
    "수",
    "목",
    "금",
    "토",
    "일"
]

weekday = weekday_list[yesterday.weekday()]


# ============================================================
# 4. 영화관 간판
# ============================================================

st.markdown(
    f"""
    <div class="sign">

        <div class="bulbs">
            ● ● ● ● ● ● ● ● ●
        </div>

        <div class="kicker">
            KOREA BOX OFFICE
        </div>

        <div class="title">
            어제의 박스오피스
        </div>

        <div class="subtitle">
            {display_date} ({weekday})
            · KOBIS DAILY BOX OFFICE
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 5. Secrets에서 KOBIS 인증키 가져오기
# ============================================================

try:

    KOBIS_KEY = st.secrets["KOBIS_KEY"]

except Exception:

    st.error(
        "🔐 KOBIS 인증키를 불러오지 못했습니다."
    )

    st.info(
        """
        Streamlit Cloud의

        **Settings → Secrets**

        에 아래처럼 등록했는지 확인하세요.

        ```toml
        KOBIS_KEY = "본인의_KOBIS_인증키"
        ```

        코드에 인증키를 직접 넣을 필요는 없습니다.
        """
    )

    st.stop()


# ============================================================
# 6. KOBIS API 주소
# ============================================================

API_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)


# ============================================================
# 7. KOBIS API 요청 함수
# ============================================================

@st.cache_data(ttl=3600)
def load_boxoffice(api_key, target_date):

    params = {
        "key": api_key,
        "targetDt": target_date
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# 8. API 요청
# ============================================================

try:

    data = load_boxoffice(
        KOBIS_KEY,
        target_dt
    )

except requests.exceptions.Timeout:

    st.error(
        "⏰ KOBIS 서버의 응답 시간이 초과되었습니다."
    )

    st.info(
        """
        잠시 후 새로고침해 주세요.

        인터넷 연결과 KOBIS 서버 상태도 확인해 주세요.
        """
    )

    st.stop()


except requests.exceptions.ConnectionError:

    st.error(
        "🌐 KOBIS API에 연결하지 못했습니다."
    )

    st.info(
        """
        인터넷 연결과 KOBIS API 서버 상태를
        확인한 뒤 다시 실행해 주세요.
        """
    )

    st.stop()


except requests.exceptions.RequestException as error:

    st.error(
        "⚠️ KOBIS API 요청에 실패했습니다."
    )

    st.info(
        f"오류 내용: `{error}`"
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
# 9. KOBIS API 자체 오류 확인
# ============================================================
# 인증키가 잘못되어도 HTTP 상태코드가 200일 수 있기 때문에
# faultInfo를 별도로 확인합니다.

if "faultInfo" in data:

    fault = data.get(
        "faultInfo",
        {}
    )

    error_code = fault.get(
        "errorCode",
        "알 수 없음"
    )

    error_message = fault.get(
        "message",
        "KOBIS API 오류"
    )

    st.error(
        "🚨 KOBIS API에서 오류를 반환했습니다."
    )

    st.write(
        f"**오류 코드:** {error_code}"
    )

    st.write(
        f"**오류 내용:** {error_message}"
    )

    st.info(
        """
        다음을 확인하세요.

        1. Secrets의 이름이 정확히 `KOBIS_KEY`인지
        2. 인증키 앞뒤에 공백이 없는지
        3. KOBIS에서 발급받은 인증키가 정상인지
        4. 잠시 후 다시 실행했는지
        """
    )

    st.stop()


# ============================================================
# 10. 응답 데이터 확인
# ============================================================

box_office_result = data.get(
    "boxOfficeResult",
    {}
)

movies = box_office_result.get(
    "dailyBoxOfficeList",
    []
)


# ============================================================
# 11. 영화 목록이 없는 경우
# ============================================================

if not movies:

    st.warning(
        f"🎬 {d
