import streamlit as st

from config.settings import init_session_state
from utils.styling import apply_forensic_theme, render_header
from modules.image_analysis import render_image_analysis_tab
from modules.video_analysis import render_video_analysis_tab
from modules.audio_analysis import render_audio_analysis_tab
from modules.multimodal_fusion import render_multimodal_fusion_tab

st.set_page_config(
    page_title="CrimeVision | Forensic Analysis",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_forensic_theme()

st.markdown("""

<style>
/* Pure black foundation */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"] {
    background: #000000 !important;
    color: #E5E5E5 !important;
}

[data-testid="stHeader"] {
    background: #000000 !important;
}

/* Black sidebar */
[data-testid="stSidebar"] {
    background: #050505 !important;
    border-right: 1px solid #252525 !important;
}

/* Main content */
.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Dark panels and cards */
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stMetric"],
[data-testid="stExpander"],
[data-testid="stFileUploader"] {
    background: #070707 !important;
    border: 1px solid #242424 !important;
    border-radius: 10px !important;
}

/* Red-accented tabs */
button[data-baseweb="tab"] {
    background: #030303 !important;
    color: #929292 !important;
    border-bottom: 1px solid #242424 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #FF3333 !important;
    border-bottom: 2px solid #B91C1C !important;
}

/* Typography */
h1, h2, h3 {
    color: #F5F5F5 !important;
    letter-spacing: -0.4px;
}

p, label, [data-testid="stMarkdownContainer"] {
    color: #C7C7C7;
}

/* Inputs */
input, textarea,
[data-baseweb="select"] > div {
    background: #080808 !important;
    color: #E5E5E5 !important;
    border-color: #303030 !important;
}

/* Evidence uploader */
[data-testid="stFileUploader"] {
    border: 1px dashed #383838 !important;
}

/* Buttons: dark with crimson accents */
.stButton > button,
.stDownloadButton > button {
    background: #0A0A0A !important;
    color: #E5E5E5 !important;
    border: 1px solid #383838 !important;
    border-radius: 7px !important;
    transition: all 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #190505 !important;
    color: #FF4444 !important;
    border-color: #B91C1C !important;
}

/* Primary buttons */
.stButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"] {
    background: #8B0000 !important;
    color: #FFFFFF !important;
    border-color: #B91C1C !important;
}

.stButton > button[kind="primary"]:hover {
    background: #B91C1C !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: #F5F5F5 !important;
}

[data-testid="stMetricLabel"] {
    color: #929292 !important;
}

/* Links and focus indicators */
a {
    color: #E04444 !important;
}

*:focus-visible {
    outline-color: #B91C1C !important;
}

/* Dividers */
hr {
    border-color: #242424 !important;
}

/* Alerts */
[data-testid="stAlert"] {
    background: #090909 !important;
    border-radius: 8px !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #000000;
}

::-webkit-scrollbar-thumb {
    background: #333333;
    border-radius: 8px;
}

::-webkit-scrollbar-thumb:hover {
    background: #8B0000;
}
</style>
""", unsafe_allow_html=True)

init_session_state()


with st.sidebar:
    st.markdown("""
    <div style="
        padding: 24px 0 20px 0;
        border-bottom: 1px solid #252525;
        margin-bottom: 24px;
    ">
        <div style="
            color: #F2F2F2;
            font-family: 'Courier New', monospace;
            font-size: 25px;
            font-weight: 700;
            letter-spacing: 1px;
        ">
            <span style="color: #B91C1C;">CV</span> CRIMEVISION
        </div>
        <div style="
            color: #777777;
            font-size: 11px;
            letter-spacing: 2px;
            margin-top: 10px;
            text-transform: uppercase;
        ">
            Forensic Intelligence
        </div>
    </div>

    <div style="
        background: #080808;
        border: 1px solid #252525;
        border-left: 2px solid #8B1A1A;
        padding: 16px;
        margin-bottom: 20px;
        color: #B5B5B5;
        font-size: 13px;
        line-height: 1.8;
    ">
        Evidence analysis workspace.<br>
        Image / Video / Audio / Fusion
    </div>

    <div style="
        color: #666666;
        font-family: 'Courier New', monospace;
        font-size: 10px;
        letter-spacing: 1px;
    ">
        SYSTEM STATUS: <span style="color: #A52A2A;">ACTIVE</span>
        <br><br>
        ANALYSIS ASSISTANCE ONLY
    </div>
    """, unsafe_allow_html=True)

render_header()

image_tab, video_tab, audio_tab, fusion_tab = st.tabs([
    "🖼️ Image Analysis",
    "🎬 Video Analysis",
    "🎙️ Audio Analysis",
    "🧠 Multimodal Fusion",
])

with image_tab:
    try:
        render_image_analysis_tab()
    except Exception as e:
        st.error("Image analysis could not load.")
        st.exception(e)

with video_tab:
    try:
        render_video_analysis_tab()
    except Exception as e:
        st.error("Video analysis could not load.")
        st.exception(e)

with audio_tab:
    try:
        render_audio_analysis_tab()
    except Exception as e:
        st.error("Audio analysis could not load.")
        st.exception(e)

with fusion_tab:
    try:
        render_multimodal_fusion_tab()
    except Exception as e:
        st.error("Multimodal fusion could not load.")
        st.exception(e)
