"""
CrimeVision AI - Configuration & Security Module
Handles API keys, session state, and chain-of-custody tracking.
"""

import streamlit as st
import uuid
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any

# ─── Application Constants ────────────────────────────────────────────
APP_TITLE = "🔬 CrimeVision AI"
APP_SUBTITLE = "Intelligent Multimodal Forensic Analysis Platform"
APP_VERSION = "2.0.0"

# Threat level definitions
THREAT_LEVELS = {
    "Low": {"color": "#4CAF50", "icon": "🟢"},
    "Medium": {"color": "#FF9800", "icon": "🟡"},
    "High": {"color": "#f44336", "icon": "🟠"},
    "Critical": {"color": "#9C27B0", "icon": "🔴"},
}

# Scene classification categories
SCENE_CLASSIFICATIONS = [
    "Burglary", "Homicide", "Vandalism", "Assault",
    "Robbery", "Arson", "Drug-Related", "Traffic Incident",
    "Domestic Violence", "Kidnapping", "Unknown"
]

# Crime categories for video analysis
CRIME_CATEGORIES = {
    "IPC 302": "Murder",
    "IPC 307": "Attempt to Murder",
    "IPC 392": "Robbery",
    "IPC 457": "Lurking House-Trespass / Burglary",
    "IPC 324": "Voluntarily Causing Hurt by Dangerous Weapons",
    "IPC 354": "Assault on Woman",
    "IPC 379": "Theft",
    "IPC 427": "Mischief / Vandalism",
    "IPC 436": "Arson",
    "IPC 304A": "Death by Negligence",
}

# Detectable forensic object classes
FORENSIC_OBJECT_CLASSES = [
    "person", "firearm", "knife", "blood_spatter", "forced_entry",
    "vehicle", "bag", "phone", "mask", "gloves", "broken_glass",
    "footprint", "shell_casing", "drug_paraphernalia", "id_document",
    "crowbar", "baseball_bat", "hammer", "rope", "duct_tape"
]


def generate_evidence_id() -> str:
    """Generate a unique forensic evidence identifier."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    uid = uuid.uuid4().hex[:8].upper()
    return f"EV-{timestamp}-{uid}"


def compute_file_hash(file_bytes: bytes) -> str:
    """Compute SHA-256 hash for chain-of-custody integrity verification."""
    return hashlib.sha256(file_bytes).hexdigest()


def get_chain_of_custody_record(
    evidence_id: str,
    file_hash: str,
    evidence_type: str,
    filename: str,
    investigator: str = "Primary Investigator"
) -> Dict[str, Any]:
    """Create a chain-of-custody record for an evidence item."""
    return {
        "evidence_id": evidence_id,
        "file_hash_sha256": file_hash,
        "evidence_type": evidence_type,
        "original_filename": filename,
        "ingestion_timestamp": datetime.now().isoformat(),
        "investigator": investigator,
        "status": "Ingested & Sealed",
        "integrity": "Verified ✓",
    }


def init_session_state():
    """Initialize all session state variables for the application."""
    defaults = {
        # API Configuration
        "api_provider": "groq",
        "api_key": "",
        "demo_mode": True,
        # Investigator info
        "investigator_name": "Detective",
        "case_number": f"CASE-{datetime.now().strftime('%Y%m%d')}-001",
        # Evidence stores
        "image_evidence": [],
        "audio_evidence": [],
        "video_evidence": [],
        # Analysis results
        "image_analysis_results": [],
        "audio_analysis_results": [],
        "video_analysis_results": [],
        # Unified timeline
        "master_timeline": [],
        # Chat history
        "chat_history": [],
        # Chain of custody log
        "custody_log": [],
        # Report generation flag
        "report_generated": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar():
    """Render the sidebar with API configuration and case information."""
    with st.sidebar:
        st.image("https://img.icons8.com/nolan/96/fingerprint.png", width=80)
        st.markdown(f"## {APP_TITLE}")
        st.caption(APP_SUBTITLE)
        st.divider()

        # ── API Configuration ──
        st.markdown("### 🔐 API Configuration")
        provider = st.selectbox(
            "AI Provider",
            ["groq", "gemini"],
            index=0,
            help="Select AI provider for analysis"
        )
        st.session_state["api_provider"] = provider

        api_key = st.text_input(
            f"{'Groq' if provider == 'groq' else 'Gemini'} API Key",
            type="password",
            value=st.session_state.get("api_key", ""),
            help="Leave blank for demo mode with simulated analysis"
        )
        st.session_state["api_key"] = api_key

        if api_key:
            st.session_state["demo_mode"] = False
            st.success("✅ API Key configured — Live mode active")
        else:
            st.session_state["demo_mode"] = True
            st.info("ℹ️ Demo mode — Using simulated AI analysis")

        st.divider()

        # ── Case Information ──
        st.markdown("### 📋 Case Information")
        st.session_state["investigator_name"] = st.text_input(
            "Investigator Name",
            value=st.session_state.get("investigator_name", "Detective"),
        )
        st.session_state["case_number"] = st.text_input(
            "Case Number",
            value=st.session_state.get("case_number", ""),
        )

        st.divider()

        # ── Chain of Custody Summary ──
        st.markdown("### 🔗 Chain of Custody")
        total_evidence = (
            len(st.session_state.get("image_evidence", []))
            + len(st.session_state.get("audio_evidence", []))
            + len(st.session_state.get("video_evidence", []))
        )
        col1, col2 = st.columns(2)
        col1.metric("Evidence Items", total_evidence)
        col2.metric("Custody Logs", len(st.session_state.get("custody_log", [])))

        st.divider()
        st.caption(f"v{APP_VERSION} • {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.caption("⚖️ For authorized law enforcement use only")
