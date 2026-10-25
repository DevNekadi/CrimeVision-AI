"""
CrimeVision AI - Custom Styling Module
Black-on-black forensic theme with restrained crimson accents.
"""

import streamlit as st


def apply_forensic_theme():
    """Apply the black and crimson forensic theme."""
    st.markdown("""
    <style>
    
     
    /* ─── Core Theme ─── */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: #000000 !important;
        color: #E5E5E5 !important;
    }

    [data-testid="stHeader"] {
        background: #000000 !important;
    }

    [data-testid="stSidebar"] {
        background: #050505 !important;
        border-right: 1px solid #242424;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ─── Main Forensic Header ─── */
    .forensic-header {
        background: linear-gradient(135deg, #080808 0%, #120303 100%);
        border: 1px solid #351010;
        border-left: 3px solid #B91C1C;
        border-radius: 4px;
        padding: 24px 30px;
        margin-bottom: 24px;
        text-align: left;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
    }

    .forensic-header h1 {
        color: #F5F5F5 !important;
        font-family: 'Courier New', monospace;
        font-size: 2.2em;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 0;
        text-shadow: 0 0 18px rgba(185, 28, 28, 0.18);
    }

    .forensic-header p {
        color: #858585 !important;
        font-size: 0.95em;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 8px;
    }

    /* ─── Evidence Cards ─── */
    .evidence-card {
        background: #080808;
        border: 1px solid #262626;
        border-radius: 5px;
        padding: 20px;
        margin: 10px 0;
        transition: border-color 0.2s ease;
    }

    .evidence-card:hover {
        border-color: #6B1717;
        box-shadow: 0 0 18px rgba(139, 0, 0, 0.08);
    }

    /* ─── Threat Level Badges ─── */
    .threat-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 3px;
        font-weight: 700;
        font-size: 0.78em;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .threat-low {
        background: #101010;
        color: #A3A3A3;
        border: 1px solid #404040;
    }

    .threat-medium {
        background: #171007;
        color: #D6A15D;
        border: 1px solid #705020;
    }

    .threat-high {
        background: #1B0505;
        color: #F05252;
        border: 1px solid #8B1A1A;
    }

    .threat-critical {
        background: #200303;
        color: #FF4545;
        border: 1px solid #B91C1C;
        animation: pulse 2.5s infinite;
    }

    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 0 0 rgba(185, 28, 28, 0);
        }
        50% {
            box-shadow: 0 0 14px rgba(185, 28, 28, 0.22);
        }
    }

    /* ─── Timeline ─── */
    .timeline-event {
        border-left: 2px solid #6B1717;
        padding: 12px 18px;
        margin: 7px 0;
        background: #070707;
        border-radius: 0 4px 4px 0;
    }

    .timeline-event .time {
        color: #D64B4B;
        font-weight: 700;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
    }

    .timeline-event .event-text {
        color: #C7C7C7;
        margin-top: 5px;
    }

    /* ─── Metric Cards ─── */
    .metric-card {
        background: #070707;
        border: 1px solid #292929;
        border-top: 2px solid #701818;
        border-radius: 4px;
        padding: 18px;
        text-align: left;
    }

    .metric-card .metric-value {
        font-family: 'Courier New', monospace;
        font-size: 2em;
        font-weight: 700;
        color: #F5F5F5;
        margin-top: 8px;
    }

    .metric-card .metric-label {
        color: #858585;
        font-size: 0.78em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* ─── Chat ─── */
    .chat-user {
        background: #0B0B0B;
        border: 1px solid #303030;
        border-left: 2px solid #555555;
        border-radius: 4px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #E0E0E0;
    }

    .chat-ai {
        background: #0C0606;
        border: 1px solid #351313;
        border-left: 2px solid #8B1A1A;
        border-radius: 4px;
        padding: 12px 16px;
        margin: 8px 0;
        color: #E0E0E0;
    }

    /* ─── Chain of Custody Badge ─── */
    .custody-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #090909;
        border: 1px solid #383838;
        border-radius: 3px;
        padding: 5px 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.8em;
        color: #D1D1D1;
    }

    /* ─── Detected Object Box ─── */
    .detection-box {
        background: #080808;
        border: 1px solid #222222;
        border-left: 3px solid #8B1A1A;
        padding: 13px 16px;
        margin: 7px 0;
        border-radius: 0 4px 4px 0;
    }

    .detection-box .obj-name {
        color: #E5E5E5;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9em;
    }

    .detection-box .obj-confidence {
        color: #A3A3A3;
        font-family: 'Courier New', monospace;
    }

    .detection-box .obj-coords {
        color: #737373;
        font-size: 0.8em;
    }

    /* ─── Tabs ─── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #030303;
        border-bottom: 1px solid #242424;
        border-radius: 4px 4px 0 0;
        padding: 5px 5px 0;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 3px 3px 0 0;
        color: #858585;
        font-weight: 600;
        padding: 10px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: #100404 !important;
        color: #F05252 !important;
        border-bottom: 2px solid #B91C1C !important;
    }

    /* ─── Global Controls ─── */
    .stButton > button,
    .stDownloadButton > button {
        background: #090909;
        color: #E5E5E5;
        border: 1px solid #383838;
        border-radius: 4px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #180505;
        color: #FFFFFF;
        border-color: #8B1A1A;
    }

    input, textarea {
        background: #080808 !important;
        color: #E5E5E5 !important;
        border-color: #303030 !important;
    }

    /* ─── Links and Separators ─── */
    a {
        color: #D64B4B !important;
    }

    hr {
        border-color: #252525 !important;
    }

    /* ─── Scrollbar ─── */
    ::-webkit-scrollbar {
        width: 7px;
        height: 7px;
    }

    ::-webkit-scrollbar-track {
        background: #000000;
    }

    ::-webkit-scrollbar-thumb {
        background: #303030;
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #7F1D1D;
    }
    
/* Remove default blue information panels */
[data-testid="stAlert"],
[data-testid="stAlertContainer"] {
    background: #080808 !important;
    color: #D0D0D0 !important;
    border: 1px solid #292929 !important;
    border-left: 2px solid #8B1A1A !important;
    border-radius: 4px !important;
}

/* Dark input and widget surfaces */
[data-baseweb="select"] > div,
[data-testid="stFileUploader"] section {
    background: #080808 !important;
    border-color: #303030 !important;
}

/* Keep the sidebar completely black */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: #050505 !important;
}

/* Red sidebar interaction accents */
[data-testid="stSidebar"] button:hover {
    border-color: #8B1A1A !important;
    color: #E5E5E5 !important;
}

    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Render the main application header."""
    st.markdown("""
    <div class="forensic-header">
        <h1>CRIMEVISION AI</h1>
        <p>Forensic Intelligence / Multimodal Evidence Analysis</p>
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, value: str, icon: str = "◈") -> str:
    """Return HTML for a styled metric card."""
    return f"""
    <div class="metric-card">
        <div style="font-size: 1.3em; color: #A52A2A;">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """


def render_threat_badge(level: str) -> str:
    """Return HTML for a styled threat-level badge."""
    css_class = f"threat-{level.lower()}"
    return f'<span class="threat-badge {css_class}">{level}</span>'


def render_evidence_id_badge(evidence_id: str) -> str:
    """Return HTML for an evidence ID badge."""
    return f'<span class="custody-badge">[EVIDENCE] {evidence_id}</span>'


def render_timeline_event(time: str, text: str, source: str = "") -> str:
    """Return HTML for a timeline event."""
    source_tag = (
        f' <span style="color: #A52A2A; font-size: 0.8em;">[{source}]</span>'
        if source else ""
    )
    return f"""
    <div class="timeline-event">
        <div class="time">{time}{source_tag}</div>
        <div class="event-text">{text}</div>
    </div>
    """


def render_detection_box(name: str, confidence: float, coords: str) -> str:
    """Return HTML for a detected object box."""
    return f"""
    <div class="detection-box">
        <div class="obj-name">{name}</div>
        <div class="obj-confidence">Confidence: {confidence:.1%}</div>
        <div class="obj-coords">[LOCATION] {coords}</div>
    </div>
    """
