from pathlib import Path

main_py = r'''import html
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import plotly.graph_objects as go
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
# 영화관 스타일 CSS
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
    padding-top: 25px;
    padding-bottom: 50px;
}
.curtain {
    position: fixed;
    top: 0;
    width: 55px;
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
.film:before {
    top: 7px;
}
.film:after {
    bottom: 7px;
}
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
    min-height: 120px;
    padding: 17px;
    border-radius: 11px;
    background: linear-gradient(145deg, #26272d, #0d0e12);
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
    font-size: 25px;
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
@media (max-width: 900px) {
    .curtain {
        width: 22px;
    }
    .block-container {
        padding-left: 32px;
        padding-right: 32px;
    }
}
</style>
<div class="curtain left"></div>
<div class="curtain right"></div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# 한국 시간 기준 '어제' 계산
# ============================================================

kst = ZoneInfo("Asia/Seoul")
now_kst = datetime.now(kst)
yesterday = now_kst - timedelta(days=1)

target_dt = yesterday.strftime("%Y%m%d")
display_date = yesterday.strftime("%Y년 %m월 %d일")

weekday_names = ["월", "화", "수", "목", "금", "토", "일"]
weekday = weekday_names[yesterday.weekday()]

# ============================================================
# 상단 영화관 간판
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
# Secrets에서 인증키 가져오기
# ============================================================

try:
    kobis_key = st.secrets["KOBIS_KEY"]
except Exception:
    st.error("🔐 KOBIS 인증키를 불러오지 못했습니다.")
    st.info(
        """
Streamlit Cloud에서 **Settings → Secrets**를 열고 아래처럼 등록했는지 확인하세요.

```toml
KOBIS_KEY = "본인의_KOBIS_인증키"
