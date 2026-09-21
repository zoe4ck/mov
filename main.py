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
        "targetDt": date
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# 8. API 요청 실행
# ============================================================

try:

    data = get_box_office(
        KOBIS_KEY,
        target_date
    )

except requests.exceptions.Timeout:

    st.error(
        "⏰ KOBIS 서버의 응답 시간이 초과되었습니다."
    )

    st.info(
        """
        ### 확인할 내용

        - 인터넷 연결 상태를 확인해 주세요.
        - 잠시 후 다시 새로고침해 주세요.
        - KOBIS 서버가 일시적으로 응답하지 않을 수도 있습니다.
        """
    )

    st.stop()


except requests.exceptions.ConnectionError:

    st.error(
        "🌐 KOBIS API에 연결하지 못했습니다."
    )

    st.info(
        """
        ### 확인할 내용

        - 인터넷 연결 상태를 확인해 주세요.
        - KOBIS API 서버가 정상적으로 작동하는지 확인해 주세요.
        - 잠시 후 다시 실행해 주세요.
        """
    )

    st.stop()


except requests.exceptions.HTTPError as e:

    st.error(
        "🚨 KOBIS API에서 HTTP 오류가 발생했습니다."
    )

    st.info(
        f"""
        **오류 정보:** `{e}`

        잠시 후 다시 실행하거나 KOBIS API 상태를 확인해 주세요.
        """
    )

    st.stop()


except requests.exceptions.RequestException:

    st.error(
        "⚠️ KOBIS API 요청에 실패했습니다."
    )

    st.info(
        """
        네트워크 연결이나 KOBIS API 상태를 확인해 주세요.
        """
    )

    st.stop()


except ValueError:

    st.error(
        "⚠️ KOBIS에서 올바른 JSON 데이터를 받지 못했습니다."
    )

    st.info(
        """
        KOBIS API가 일시적으로 정상적인 데이터를 반환하지 않았을 수 있습니다.
        잠시 후 다시 시도해 주세요.
        """
    )

    st.stop()


# ============================================================
# 9. KOBIS 자체 오류 확인
# ============================================================
# 중요한 부분입니다.
#
# KOBIS는 인증키가 틀려도 HTTP 상태코드가 200일 수 있습니다.
# 따라서 faultInfo가 있는지 직접 확인해야 합니다.

if "faultInfo" in data:

    fault_info = data.get(
        "faultInfo",
        {}
    )

    error_code = fault_info.get(
        "errorCode",
        ""
    )

    error_message = fault_info.get(
        "message",
        "KOBIS API에서 오류가 발생했습니다."
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
# 10. boxOfficeResult 확인
# ============================================================

if "boxOfficeResult" not in data:

    st.error(
        "⚠️ 박스오피스 데이터를 찾을 수 없습니다."
    )

    st.info(
        """
        KOBIS API의 응답 구조가 예상과 다릅니다.

        KOBIS API가 일시적으로 오류를 반환했거나
        API 설정에 문제가 있을 수 있습니다.
        """
    )

    st.stop()


box_office_result = data["boxOfficeResult"]


# ============================================================
# 11. 영화 목록 가져오기
# ============================================================

movie_list = box_office_result.get(
    "dailyBoxOfficeList",
    []
)


# ============================================================
# 12. 영화 목록이 비어 있을 때
# ============================================================

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
# 13. 데이터를 DataFrame으로 변환
# ============================================================

rows = []


for movie in movie_list:

    # 숫자가 문자열로 오기 때문에 int로 변환합니다.
    try:
        rank = int(movie.get("rank", 0))
    except:
        rank = 0

    try:
        rank_inten = int(movie.get("rankInten", 0))
    except:
        rank_inten = 0

    try:
        audi_cnt = int(movie.get("audiCnt", 0))
    except:
        audi_cnt = 0

    try:
        audi_acc = int(movie.get("audiAcc", 0))
    except:
        audi_acc = 0

    try:
        scrn_cnt = int(movie.get("scrnCnt", 0))
    except:
        scrn_cnt = 0

    try:
        show_cnt = int(movie.get("showCnt", 0))
    except:
        show_cnt = 0

    rows.append(
        {
            "순위": rank,
            "순위변동": rank_inten,
            "영화명": movie.get(
                "movieNm",
                "-"
            ),
            "개봉일": movie.get(
                "openDt",
                "-"
            ),
            "관객수": audi_cnt,
            "누적관객": audi_acc,
            "스크린수": scrn_cnt,
            "상영횟수": show_cnt
        }
    )


df = pd.DataFrame(rows)


# ============================================================
# 14. 데이터가 만들어지지 않았을 때
# ============================================================

if df.empty:

    st.warning(
        "🎬 영화 데이터가 비어 있습니다."
    )

    st.info(
        """
        KOBIS에서 영화 목록을 받았지만
        화면에 표시할 데이터가 없습니다.

        잠시 후 다시 실행하거나 KOBIS API 응답을 확인해 주세요.
        """
    )

    st.stop()


# ============================================================
# 15. 숫자 표시 함수
# ============================================================

def format_number(value):

    return f"{int(value):,}"


# ============================================================
# 16. 순위 변동 표시 함수
# ============================================================

def rank_change(value):

    value = int(value)

    if value > 0:

        return f"▲ {value}"

    elif value < 0:

        return f"▼ {abs(value)}"

    else:

        return "━"


# ============================================================
# 17. 토마토 평점 세션 만들기
# ============================================================
# KOBIS에는 평점 정보가 없기 때문에
# 사용자가 직접 남기는 개인 평점을 저장합니다.
#
# 새로고침하면 초기화될 수 있습니다.
# 데이터 자체를 임의로 생성하지 않습니다.

if "tomato_ratings" not in st.session_state:

    st.session_state.tomato_ratings = {}


# ============================================================
# 18. 토마토 아이콘 표시 함수
# ============================================================

def tomato_display(rating):

    if rating is None:

        return "평점 없음"

    # 0.5 단위이므로
    # 전체 토마토 수를 계산합니다.
    full = int(rating)

    half = 1 if rating - full >= 0.5 else 0

    empty = 5 - full - half

    result = ""

    result += "🍅" * full

    if half:

        result += "🍅"

    result += "🤍" * empty

    return result


# ============================================================
# 19. 현재 1위 영화
# ============================================================

first_movie = df.iloc[0]

first_movie_name = first_movie["영화명"]

first_rating = st.session_state.tomato_ratings.get(
    first_movie_name,
    None
)


# ============================================================
# 20. 1위 영화 + TOP5 영역
# ============================================================

left_col, right_col = st.columns(
    [1.25, 1],
    gap="large"
)


# ============================================================
# 왼쪽 : 1위 영화
# ============================================================

with left_col:

    st.markdown(
        """
        <div class="film-frame">
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="rank-one-label">

            <span class="rank-one-badge">
                1
            </span>

            현재 박스오피스 1위

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="movie-title">
            {html.escape(first_movie_name)}
        </div>

        <div class="movie-date">
            개봉일 · {html.escape(str(first_movie["개봉일"]))}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # 1위 영화의 주요 지표
    # --------------------------------------------------------

    m1, m2, m3 = st.columns(3)


    with m1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    👥
                </div>

                <div class="metric-label">
                    어제 관객수
                </div>

                <div class="metric-value">
                    {format_number(first_movie["관객수"])}명
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with m2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    🎟️
                </div>

                <div class="metric-label">
                    누적 관객수
                </div>

                <div class="metric-value">
                    {format_number(first_movie["누적관객"])}명
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with m3:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-icon">
                    🎬
                </div>

                <div class="metric-label">
                    스크린수
                </div>

                <div class="metric-value">
                    {format_number(first_movie["스크린수"])}개
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # 1위 영화 토마토 평점
    # --------------------------------------------------------

    if first_rating is not None:

        tomato_text = tomato_display(
            first_rating
        )

        st.markdown(
            f"""
            <div class="tomato-card">

                <div class="tomato-label">
                    🍅 MY TOMATO RATING
                </div>

                <div class="tomato-icons">
                    {tomato_text}
                </div>

                <div class="tomato-score">
                    내가 남긴 평점 ·
                    {first_rating:.1f} / 5.0
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    else:

        st.markdown(
            """
            <div class="tomato-card">

                <div class="tomato-label">
                    🍅 MY TOMATO RATING
                </div>

                <div class="tomato-icons">
                    🤍🤍🤍🤍🤍
                </div>

                <div class="tomato-score">
                    아직 내가 평가하지 않은 영화
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# 오른쪽 : TOP 5 그래프
# ============================================================

with right_col:

    st.markdown(
        """
        <div class="film-frame">
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-title">
            📊 관객수 TOP 5
            <span class="section-line"></span>
        </div>
        """,
        unsafe_allow_html=True
    )


    top5 = df.head(5).copy()


    # 긴 영화 제목 때문에 그래프가 깨지지 않도록
    # 적당한 길이로 줄입니다.

    chart_names = []

    for name in top5["영화명"]:

        if len(name) > 12:

            chart_names.append(
                name[:12] + "…"
            )

        else:

            chart_names.append(name)


    # Plotly 막대그래프
    # 영화관 분위기에 맞춰 어두운 배경과 금색 계열을 사용합니다.

    fig = go.Figure()


    fig.add_trace(
        go.Bar(
            x=chart_names,
            y=top5["관객수"],
            text=[
                f"{format_number(x)}명"
                for x in top5["관객수"]
            ],
            textposition="outside",
            marker=dict(
                color=[
                    "#d95b5b",
                    "#d77b67",
                    "#b88bc4",
                    "#849dd4",
                    "#7196bd"
                ]
            )
        )
    )


    fig.update_layout(

        height=370,

        margin=dict(
            l=10,
            r=10,
            t=35,
            b=10
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            color="#e8dfd0"
        ),

        xaxis=dict(

            showgrid=False,

            tickfont=dict(
                size=11
            )
        ),

        yaxis=dict(

            showgrid=True,

            gridcolor="rgba(255,255,255,0.08)",

            zeroline=False,

            tickformat=","
        ),

        showlegend=False
    )


    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# 21. 흥행 온도
# ============================================================
# TOP 5가 전체 관객 중 어느 정도를 차지하는지 계산합니다.
#
# 이것은 공식 KOBIS 지표가 아니라
# 이 앱에서 보여주는 간단한 참고용 지표입니다.

total_audience = df["관객수"].sum()

top5_audience = top5["관객수"].sum()


if total_audience > 0:

    top5_ratio = (
        top5_audience
        / total_audience
        * 100
    )

else:

    top5_ratio = 0


if top5_ratio >= 80:

    heat_text = "🔥 뜨거운 흥행 집중"

elif top5_ratio >= 60:

    heat_text = "🌡️ 높은 흥행 집중"

elif top5_ratio >= 40:

    heat_text = "🎞️ 적당한 흥행 집중"

else:

    heat_text = "❄️ 관객 분산"


# ============================================================
# 22. 1위 스크린당 관객수
# ============================================================

if first_movie["스크린수"] > 0:

    audience_per_screen = (
        first_movie["관객수"]
        / first_movie["스크린수"]
    )

else:

    audience_per_screen = 0


heat_col, screen_col = st.columns(2)


with heat_col:

    st.markdown(
        f"""
        <div class="heat-card">

            <div class="heat-label">
                🍿 BOX OFFICE HEAT
            </div>

            <div class="heat-value">
                {heat_text}
            </div>

            <div class="heat-text">
                TOP 5 영화가 전체 박스오피스 관객의
                <b>{top5_ratio:.1f}%</b>를 차지하고 있습니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with screen_col:

    st.markdown(
        f"""
        <div class="heat-card">

            <div class="heat-label">
                🎟️ SCREEN EFFICIENCY
            </div>

            <div class="heat-value">
                {format_number(round(audience_per_screen))}명
            </div>

            <div class="heat-text">
                현재 1위 영화의
                <b>스크린 1개당 일일 관객수</b>입니다.
                <br>
                관객수 ÷ 스크린수로 계산했습니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 23. 토마토 평점 입력 영역
# ============================================================

st.markdown(
    """
    <div class="section-title">

        🍅 나만의 토마토 평점

        <span class="section-line"></span>

    </div>
    """,
    unsafe_allow_html=True
)


st.info(
    "🍅 KOBIS 일일 박스오피스 API에는 영화 평점 데이터가 없기 때문에 "
    "이 평점은 실제 Rotten Tomatoes 평점이 아니라 이 앱에서 직접 남기는 개인 평점입니다."
)


rating_col1, rating_col2 = st.columns(
    [1, 1]
)


with rating_col1:

    selected_movie = st.selectbox(
        "평가할 영화를 선택하세요.",
        df["영화명"].tolist(),
        key="rating_movie"
    )


with rating_col2:

    rating_labels = [
        "평점 없음",
        "🍅 0.5",
        "🍅 1.0",
        "🍅 1.5",
        "🍅 2.0",
        "🍅 2.5",
        "🍅 3.0",
        "🍅 3.5",
        "🍅 4.0",
        "🍅 4.5",
        "🍅 5.0"
    ]


    current_rating = st.session_state.tomato_ratings.get(
        selected_movie,
        None
    )


    if current_rating is None:

        default_index = 0

    else:

        default_index = int(
            current_rating * 2
        )


        # 0.5 → 1번째
        # 1.0 → 2번째
        # ...
        # 5.0 → 10번째

        default_index += 0


    selected_label = st.selectbox(
        "토마토 평점",
        rating_labels,
        index=default_index,
        key="rating_value"
    )


# 선택된 평점을 숫자로 변환

if selected_label == "평점 없음":

    new_rating = None

else:

    new_rating = float(
        selected_label
        .replace("🍅", "")
        .strip()
    )


# 평점 저장

if new_rating is None:

    if selected_movie in st.session_state.tomato_ratings:

        del st.session_state.tomato_ratings[
            selected_movie
        ]

else:

    st.session_state.tomato_ratings[
        selected_movie
    ] = new_rating


# 현재 선택 영화의 평점 표시

current_rating = st.session_state.tomato_ratings.get(
    selected_movie,
    None
)


if current_rating is not None:

    st.markdown(
        f"""
        <div class="tomato-card">

            <div class="tomato-label">
                MY TOMATO RATING
            </div>

            <div class="tomato-icons">
                {tomato_display(current_rating)}
            </div>

            <div class="tomato-score">
                <b>{html.escape(selected_movie)}</b>
                · {current_rating:.1f} / 5.0
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.caption(
        "아직 이 영화에 토마토 평점을 남기지 않았습니다."
    )


# ============================================================
# 24. 영화 검색
# ============================================================

st.markdown(
    """
    <div class="section-title">

        🔎 영화 검색

        <span class="section-line"></span>

    </div>
    """,
    unsafe_allow_html=True
)


search_text = st.text_input(
    "영화명을 검색하세요.",
    placeholder="예: 아바타, 미션, 좀비...",
    key="movie_search"
)


# 검색어가 있으면 영화 목록을 필터링

if search_text.strip():

    filtered_df = df[
        df["영화명"].str.contains(
            search_text.strip(),
            case=False,
            na=False
        )
    ].copy()

else:

    filtered_df = df.copy()


# ============================================================
# 25. 전체 박스오피스 표
# ============================================================

st.markdown(
    """
    <div class="section-title">

        🎞️ 전체 박스오피스

        <span class="section-line"></span>

    </div>
    """,
    unsafe_allow_html=True
)


# 표시용 데이터프레임을 따로 만듭니다.
# 원본 df는 숫자 계산을 위해 그대로 유지합니다.

display_df = filtered_df.copy()


# ------------------------------------------------------------
# 순위 변동
# ------------------------------------------------------------

display_df["순위 변동"] = display_df[
    "순위변동"
].apply(rank_change)


# ------------------------------------------------------------
# 토마토 평점
# ------------------------------------------------------------

display_df["🍅 토마토"] = display_df[
    "영화명"
].apply(
    lambda movie:
        tomato_display(
            st.session_state.tomato_ratings.get(
                movie,
                None
            )
        )
)


# ------------------------------------------------------------
# 숫자에 천 단위 쉼표 적용
# ------------------------------------------------------------

display_df["관객수"] = display_df[
    "관객수"
].apply(format_number)


display_df["누적관객"] = display_df[
    "누적관객"
].apply(format_number)


display_df["스크린수"] = display_df[
    "스크린수"
].apply(format_number)


# ------------------------------------------------------------
# 필요한 열만 선택
# ------------------------------------------------------------

display_df = display_df[
    [
        "순위",
        "순위 변동",
        "영화명",
        "🍅 토마토",
        "개봉일",
        "관객수",
        "누적관객",
        "스크린수"
    ]
]


# ------------------------------------------------------------
# 검색 결과가 없는 경우
# ------------------------------------------------------------

if display_df.empty:

    st.warning(
        f"🔎 '{search_text}'와 일치하는 영화가 없습니다."
    )

else:

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=520
    )


# ============================================================
# 26. 영화 티켓
# ============================================================

st.markdown(
    f"""
    <div class="ticket">

        <div class="ticket-small">
            CINEMA TICKET · KOBIS DAILY BOX OFFICE
        </div>

        <div class="ticket-title">
            🎟️ {display_date}
        </div>

        <div class="ticket-text">

            오늘의 상영 정보는
            <b>어제의 실제 박스오피스 데이터</b>를 기준으로 합니다.

            <br>

            조회일 · {display_date}

            <br>

            데이터 · 영화관입장권통합전산망(KOBIS)

        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 27. 데이터 안내
# ============================================================

st.markdown(
    """
    <div style="
        margin-top:25px;
        padding:18px;
        border:1px solid #403522;
        border-radius:10px;
        background:rgba(255,255,255,0.015);
        color:#9f9689;
        font-size:12px;
        line-height:1.8;
    ">

        🎬 <b>KOBIS 데이터 안내</b><br>

        순위 · 영화명 · 개봉일 · 관객수 · 누적관객수 ·
        스크린수는 KOBIS 일일 박스오피스 API에서 가져옵니다.

        <br><br>

        🍅 토마토 평점은 KOBIS에서 제공하는 공식 평점이 아니며,
        사용자가 직접 입력한 개인 평점입니다.

        <br>

        🍿 흥행 온도와 스크린당 관객수는
        KOBIS 데이터를 이용해 이 앱에서 계산한 참고용 지표입니다.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 28. 하단 필름 스트립
# ============================================================

st.markdown(
    """
    <div class="film-strip">

        🎞️　오늘, 어떤 영화를 보시겠어요?　🍿　🎬

    </div>
    """,
    unsafe_allow_html=True
)
