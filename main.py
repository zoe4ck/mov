import html
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import requests
import streamlit as st


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="어제의 박스오피스",
    page_icon="🎬",
    layout="wide",
)

# ============================================================
# 영화관 디자인
# ============================================================

st.markdown(
    """
<style>
.stApp {
    background: radial-gradient(circle at 50% 0%, #351414 0%, #0b0b0d 38%, #050506 100%);
    color: #f5eee2;
}
#MainMenu, footer {
    visibility: hidden;
}
.block-container {
    max-width: 1400px;
    padding-top: 28px;
    padding-bottom: 50px;
}
.curtain {
    position: fixed;
    top: 0;
    width: 52px;
    height: 100vh;
    z-index: 9999;
    pointer-events: none;
    background: repeating-linear-gradient(
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
.sign {
    text-align: center;
    padding: 25px;
    margin: 5px auto 30px;
    max-width: 1000px;
    border: 2px solid #c79a4c;
    border-radius: 16px;
    background: linear-gradient(145deg, #241608, #080808, #241608);
    box-shadow: 0 0 0 4px #090909, 0 0 0 6px #59411f, 0 15px 45px #000;
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
.film {
    padding: 28px;
    border-radius: 14px;
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg, #17181d, #07080a);
    border: 1px solid #8d692f;
    box-shadow: 0 0 0 4px #070707, 0 0 0 5px #473619, 0 15px 40px #0008;
}
.film:before,
.film:after {
    content: "";
    position: absolute;
    left: 12px;
    right: 12px;
    height: 7px;
    background: repeating-linear-gradient(
        90deg,
        #b4883d 0px,
        #b4883d 12px,
        transparent 12px,
        transparent 26px
    );
    opacity: 0.5;
}
.film:before { top: 7px; }
.film:after { bottom: 7px; }
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
.metric {
    min-height: 118px;
    padding: 16px;
    border-radius: 11px;
    background: linear-gradient(145deg, #26272d, #0d0e12);
    border: 1px solid #65502d;
}
.metric-icon { font-size: 21px; }
.metric-label {
    color: #aaa096;
    font-size: 12px;
    margin: 6px 0;
}
.metric-value {
    color: #fff4df;
    font-size: 20px;
    font-weight: 900;
}
.tomato {
    margin-top: 17px;
    padding: 17px 20px;
    border-radius: 11px;
    background: linear-gradient(135deg, #451012, #100708);
    border: 1px solid #7c3832;
}
.tomato-label {
    color: #e9bf61;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}
.tomato-icons {
    font-size: 24px;
    margin: 5px 0;
}
.tomato-score {
    color: #bcb0a0;
    font-size: 12px;
}
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
    background: linear-gradient(90deg, #9e7837, transparent);
}
.info {
    padding: 19px;
    margin-top: 18px;
    border-radius: 11px;
    background: linear-gradient(135deg, #421113, #100708);
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
.ticket {
    margin-top: 30px;
    padding: 20px;
    border-radius: 8px;
    color: #241608;
    background: linear-gradient(135deg, #b98232, #f0d99b, #bd8535);
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
</style>
<div class="curtain left"></div>
<div class="curtain right"></div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# 한국 시간 기준 어제 계산
# ============================================================

kst = ZoneInfo("Asia/Seoul")
yesterday = datetime.now(kst) - timedelta(days=1)
target_dt = yesterday.strftime("%Y%m%d")
display_date = yesterday.strftime("%Y년 %m월 %d일")
weekday = ["월", "화", "수", "목", "금", "토", "일"][yesterday.weekday()]

# ============================================================
# 제목
# ============================================================

st.markdown(
    (
        '<div class="sign">'
        '<div class="bulbs">● ● ● ● ● ● ● ● ●</div>'
        '<div class="kicker">KOREA BOX OFFICE</div>'
        '<div class="title">어제의 박스오피스</div>'
        '<div class="subtitle">'
        + html.escape(display_date)
        + " ("
        + weekday
        + ") · KOBIS DAILY BOX OFFICE"
        + "</div></div>"
    ),
    unsafe_allow_html=True,
)

# ============================================================
# 인증키
# ============================================================

try:
    kobis_key = st.secrets["KOBIS_KEY"]
except Exception:
    st.error("🔐 KOBIS 인증키를 불러오지 못했습니다.")
    st.info(
        """
Streamlit Cloud의 **Settings → Secrets**에 아래처럼 등록하세요.

```toml
KOBIS_KEY = "본인의_KOBIS_인증키"
```
"""
    )
    st.stop()

# ============================================================
# KOBIS API
# ============================================================

API_URL = (
    "https://www.kobis.or.kr/"
    "kobisopenapi/webservice/rest/boxoffice/"
    "searchDailyBoxOfficeList.json"
)


@st.cache_data(ttl=3600)
def load_boxoffice(api_key, target_date):
    response = requests.get(
        API_URL,
        params={"key": api_key, "targetDt": target_date},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


try:
    data = load_boxoffice(kobis_key, target_dt)
except requests.exceptions.Timeout:
    st.error("⏰ KOBIS 서버 응답 시간이 초과되었습니다.")
    st.info("잠시 후 새로고침하고 KOBIS 서버 상태를 확인하세요.")
    st.stop()
except requests.exceptions.ConnectionError:
    st.error("🌐 KOBIS API에 연결하지 못했습니다.")
    st.info("인터넷 연결과 KOBIS API 서버 상태를 확인하세요.")
    st.stop()
except requests.exceptions.RequestException as error:
    st.error("⚠️ KOBIS API 요청에 실패했습니다.")
    st.info("오류 내용: " + str(error))
    st.stop()
except ValueError:
    st.error("⚠️ KOBIS에서 올바른 데이터를 받지 못했습니다.")
    st.info("잠시 후 다시 실행해 주세요.")
    st.stop()

# KOBIS는 인증키가 틀려도 200을 반환할 수 있으므로 faultInfo 확인
if "faultInfo" in data:
    fault = data.get("faultInfo", {})
    st.error("🚨 KOBIS API 오류")
    st.write("오류 코드:", fault.get("errorCode", "알 수 없음"))
    st.write("오류 내용:", fault.get("message", "알 수 없음"))
    st.info("Streamlit Secrets의 KOBIS_KEY 이름과 인증키를 확인하세요.")
    st.stop()

result = data.get("boxOfficeResult", {})
movies = result.get("dailyBoxOfficeList", [])

if not movies:
    st.warning("🎬 영화 목록이 없습니다.")
    st.info(
        "KOBIS에서 해당 날짜의 일일 박스오피스가 제공되는지, "
        "인증키가 정상인지 확인해 주세요."
    )
    st.stop()

# ============================================================
# 데이터 변환
# ============================================================

def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


rows = []

for movie in movies:
    rows.append(
        {
            "순위": to_int(movie.get("rank")),
            "순위변동값": to_int(movie.get("rankInten")),
            "영화명": movie.get("movieNm", "-"),
            "개봉일": movie.get("openDt", "-"),
            "관객수": to_int(movie.get("audiCnt")),
            "누적관객": to_int(movie.get("audiAcc")),
            "스크린수": to_int(movie.get("scrnCnt")),
        }
    )

df = pd.DataFrame(rows)

if df.empty:
    st.warning("🎬 영화 데이터가 비어 있습니다.")
    st.stop()


def number(value):
    return f"{int(value):,}"


def rank_change(value):
    value = int(value)
    if value > 0:
        return f"▲ {value}"
    if value < 0:
        return f"▼ {abs(value)}"
    return "━"


def tomato_icons(rating):
    if rating is None:
        return "🤍🤍🤍🤍🤍"

    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half

    return ("🍅" * full) + ("◐" if half else "") + ("🤍" * empty)


# ============================================================
# 개인 토마토 평점 저장
# ============================================================

if "tomato_ratings" not in st.session_state:
    st.session_state.tomato_ratings = {}

# ============================================================
# 1위 영화
# ============================================================

first = df.iloc[0]
first_name = str(first["영화명"])
first_rating = st.session_state.tomato_ratings.get(first_name)

left, right = st.columns([1.15, 1], gap="large")

with left:
    st.markdown('<div class="film">', unsafe_allow_html=True)

    st.markdown(
        (
            '<div class="movie-rank">🏆 1위 · DAILY BOX OFFICE</div>'
            '<div class="movie-title">'
            + html.escape(first_name)
            + '</div><div class="movie-date">개봉일 · '
            + html.escape(str(first["개봉일"]))
            + "</div>"
        ),
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)

    with a:
        st.markdown(
            (
                '<div class="metric"><div class="metric-icon">👥</div>'
                '<div class="metric-label">어제 관객수</div>'
                '<div class="metric-value">'
                + number(first["관객수"])
                + "명</div></div>"
            ),
            unsafe_allow_html=True,
        )

    with b:
        st.markdown(
            (
                '<div class="metric"><div class="metric-icon">🎟️</div>'
                '<div class="metric-label">누적 관객</div>'
                '<div class="metric-value">'
                + number(first["누적관객"])
                + "명</div></div>"
            ),
            unsafe_allow_html=True,
        )

    with c:
        st.markdown(
            (
                '<div class="metric"><div class="metric-icon">🎬</div>'
                '<div class="metric-label">스크린수</div>'
                '<div class="metric-value">'
                + number(first["스크린수"])
                + "개</div></div>"
            ),
            unsafe_allow_html=True,
        )

    score_text = (
        "아직 평가하지 않은 영화"
        if first_rating is None
        else f"내 평점 · {first_rating:.1f} / 5.0"
    )

    st.markdown(
        (
            '<div class="tomato"><div class="tomato-label">'
            "🍅 MY TOMATO RATING</div><div class=\"tomato-icons\">"
            + tomato_icons(first_rating)
            + '</div><div class="tomato-score">'
            + html.escape(score_text)
            + "</div></div>"
        ),
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# TOP 5 그래프
# ============================================================

with right:
    st.markdown('<div class="film">', unsafe_allow_html=True)
    st.markdown(
        '<div class="section">📊 관객수 TOP 5 <span class="line"></span></div>',
        unsafe_allow_html=True,
    )

    top5 = df.head(5).copy()
    chart_df = top5[["영화명", "관객수"]].copy()
    chart_df = chart_df.set_index("영화명")
    st.bar_chart(chart_df, y="관객수", height=330)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# 추가 흥행 지표
# ============================================================

st.markdown(
    '<div class="section">🍿 오늘의 흥행 지표 <span class="line"></span></div>',
    unsafe_allow_html=True,
)

total = int(df["관객수"].sum())
top5_total = int(top5["관객수"].sum())
ratio = (top5_total / total * 100) if total else 0

screens = int(first["스크린수"])
per_screen = int(first["관객수"]) / screens if screens else 0

if ratio >= 80:
    heat = "🔥 매우 집중"
elif ratio >= 60:
    heat = "🌡️ 높은 집중"
elif ratio >= 40:
    heat = "🎞️ 보통"
else:
    heat = "❄️ 관객 분산"

x, y = st.columns(2)

with x:
    st.markdown(
        (
            '<div class="info"><div class="info-label">BOX OFFICE HEAT</div>'
            '<div class="info-value">'
            + heat
            + '</div><div class="info-text">TOP 5 영화가 전체 목록 관객수의 '
            + f"<b>{ratio:.1f}%</b>를 차지합니다."
            + "</div></div>"
        ),
        unsafe_allow_html=True,
    )

with y:
    st.markdown(
        (
            '<div class="info"><div class="info-label">SCREEN EFFICIENCY</div>'
            '<div class="info-value">'
            + number(round(per_screen))
            + "명/스크린</div>"
            '<div class="info-text">1위 영화의 관객수를 스크린수로 나눈 참고용 지표입니다.</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )

# ============================================================
# 토마토 평점
# ============================================================

st.markdown(
    '<div class="section">🍅 나만의 토마토 평점 <span class="line"></span></div>',
    unsafe_allow_html=True,
)

st.caption(
    "KOBIS 공식 평점이 아닙니다. 사용자가 직접 기록하는 개인 평점입니다."
)

movie_col, score_col = st.columns(2)

with movie_col:
    selected_movie = st.selectbox(
        "평가할 영화",
        df["영화명"].tolist(),
    )

with score_col:
    options = [
        "평점 없음",
        "0.5",
        "1.0",
        "1.5",
        "2.0",
        "2.5",
        "3.0",
        "3.5",
        "4.0",
        "4.5",
        "5.0",
    ]

    old = st.session_state.tomato_ratings.get(str(selected_movie))
    index = 0 if old is None else int(old * 2)

    selected_score = st.selectbox(
        "토마토 점수",
        options,
        index=index,
    )

if selected_score == "평점 없음":
    st.session_state.tomato_ratings.pop(str(selected_movie), None)
else:
    st.session_state.tomato_ratings[str(selected_movie)] = float(selected_score)

current = st.session_state.tomato_ratings.get(str(selected_movie))
current_text = "평점 없음" if current is None else f"{current:.1f} / 5.0"

st.markdown(
    (
        '<div class="tomato"><div class="tomato-label">YOUR REVIEW</div>'
        '<div class="tomato-icons">'
        + tomato_icons(current)
        + '</div><div class="tomato-score"><b>'
        + html.escape(str(selected_movie))
        + "</b> · "
        + current_text
        + "</div></div>"
    ),
    unsafe_allow_html=True,
)

# ============================================================
# 검색 및 표
# ============================================================

st.markdown(
    '<div class="section">🔎 영화 검색 <span class="line"></span></div>',
    unsafe_allow_html=True,
)

search = st.text_input(
    "영화명 검색",
    placeholder="영화 제목을 입력하세요.",
)

if search.strip():
    shown = df[
        df["영화명"].astype(str).str.contains(
            search.strip(),
            case=False,
            na=False,
        )
    ].copy()
else:
    shown = df.copy()

st.markdown(
    '<div class="section">🎞️ 전체 박스오피스 <span class="line"></span></div>',
    unsafe_allow_html=True,
)

table = shown.copy()
table["순위 변동"] = table["순위변동값"].apply(rank_change)

table["🍅"] = table["영화명"].apply(
    lambda name: tomato_icons(
        st.session_state.tomato_ratings.get(str(name))
    )
)

for col in ["관객수", "누적관객", "스크린수"]:
    table[col] = table[col].apply(number)

table = table[
    [
        "순위",
        "순위 변동",
        "영화명",
        "🍅",
        "개봉일",
        "관객수",
        "누적관객",
        "스크린수",
    ]
]

if table.empty:
    st.warning("🔎 검색 결과가 없습니다.")
else:
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        height=520,
    )

# ============================================================
# 하단 영화 티켓
# ============================================================

st.markdown(
    (
        '<div class="ticket"><div class="ticket-small">'
        "CINEMA TICKET · KOBIS DAILY BOX OFFICE</div>"
        '<div class="ticket-title">🎟️ '
        + html.escape(display_date)
        + '</div><div class="ticket-text">'
        "한국 시간 기준 어제의 KOBIS 일일 박스오피스입니다."
        "<br>순위 · 영화명 · 개봉일 · 관객수 · 누적관객 · 스크린수는 KOBIS 데이터를 사용합니다."
        "<br>토마토 평점과 흥행 지표는 이 앱에서 추가한 참고용 기능입니다."
        "</div></div>"
    ),
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="film-strip">
    🎞️ TODAY'S SHOW · 어제의 영화관을 만나보세요 · 🍿 🎬
</div>
""",
    unsafe_allow_html=True,
)
