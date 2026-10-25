"""
CrimeVision AI - Audio Analysis Module (Tab 2)
Witness Audio Transcription & Forensic Timeline Extraction.
"""

import streamlit as st
import io
import random
from datetime import datetime
from typing import Optional

from config.settings import (
    generate_evidence_id, compute_file_hash,
    get_chain_of_custody_record
)
from utils.styling import (
    render_evidence_id_badge, render_metric_card,
    render_timeline_event
)
from utils.ai_engine import analyze_audio


def render_audio_analysis_tab():
    """Render the Audio Analysis tab content."""
    st.markdown("## 🎙️ Witness Audio Transcription & Timeline")
    st.markdown(
        "Upload witness statements, 911/112 emergency calls, or surveillance audio. "
        "The system uses **Whisper-based transcription** to extract speaker-tagged "
        "transcripts, key forensic events, and chronological timelines."
    )
    
    st.divider()
    
    # ── Upload Section ──
    uploaded_files = st.file_uploader(
        "📂 Upload Audio Evidence",
        type=["wav", "mp3", "m4a", "ogg", "flac", "aac", "wma"],
        accept_multiple_files=True,
        help="Supported: WAV, MP3, M4A, OGG, FLAC, AAC. Max 500MB per file.",
        key="audio_uploader"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Check if already ingested
            existing_ids = [e.get("filename") for e in st.session_state.get("audio_evidence", [])]
            if uploaded_file.name in existing_ids:
                continue
            
            file_bytes = uploaded_file.read()
            uploaded_file.seek(0)
            
            # Generate evidence tracking
            evidence_id = generate_evidence_id()
            file_hash = compute_file_hash(file_bytes)
            custody_record = get_chain_of_custody_record(
                evidence_id, file_hash, "Audio", uploaded_file.name,
                st.session_state.get("investigator_name", "Detective")
            )
            
            # Estimate duration (rough: ~16KB per second for WAV, varies)
            estimated_duration = len(file_bytes) / 16000  # rough estimate
            
            # Store evidence
            st.session_state["audio_evidence"].append({
                "evidence_id": evidence_id,
                "filename": uploaded_file.name,
                "file_hash": file_hash,
                "file_bytes": file_bytes,
                "estimated_duration": estimated_duration,
                "custody_record": custody_record,
                "ingestion_time": datetime.now().isoformat(),
            })
            st.session_state["custody_log"].append(custody_record)
        
        st.success(f"✅ {len(uploaded_files)} audio file(s) ingested into evidence chain")
    
    # ── Display & Analyze Stored Audio Evidence ──
    if st.session_state.get("audio_evidence"):
        st.divider()
        st.markdown("### 🔍 Audio Evidence & Transcription")
        
        for idx, evidence in enumerate(st.session_state["audio_evidence"]):
            with st.expander(
                f"🎵 {evidence['filename']} — `{evidence['evidence_id']}`",
                expanded=(idx == 0)
            ):
                # Chain of custody badge
                st.markdown(
                    render_evidence_id_badge(evidence["evidence_id"]),
                    unsafe_allow_html=True
                )
                st.caption(f"SHA-256: `{evidence['file_hash'][:32]}...`")
                
                # Audio metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(
                        render_metric_card("File Size", f"{len(evidence['file_bytes']) / 1024:.1f} KB", "💾"),
                        unsafe_allow_html=True
                    )
                with col2:
                    st.markdown(
                        render_metric_card("Est. Duration", f"{evidence['estimated_duration']:.0f}s", "⏱️"),
                        unsafe_allow_html=True
                    )
                with col3:
                    st.markdown(
                        render_metric_card("Format", evidence['filename'].split('.')[-1].upper(), "📁"),
                        unsafe_allow_html=True
                    )
                
                # Audio player
                st.markdown("**🔊 Audio Playback**")
                try:
                    st.audio(evidence["file_bytes"], format=f"audio/{evidence['filename'].split('.')[-1]}")
                except Exception:
                    st.warning("Audio playback not available for this format.")
                
                # Analysis button
                if st.button(
                    f"🔬 Transcribe & Analyze",
                    key=f"btn_audio_{evidence['evidence_id']}",
                    type="primary",
                    use_container_width=True
                ):
                    with st.spinner("🔄 Running Whisper transcription and forensic event extraction..."):
                        result = analyze_audio(
                            evidence["filename"],
                            evidence["file_bytes"],
                            evidence.get("estimated_duration", 0)
                        )
                        result["evidence_id"] = evidence["evidence_id"]
                        
                        # Store result
                        st.session_state["audio_analysis_results"] = [
                            r for r in st.session_state["audio_analysis_results"]
                            if r.get("evidence_id") != evidence["evidence_id"]
                        ]
                        st.session_state["audio_analysis_results"].append(result)
                        
                        # Add key events to master timeline
                        for event in result.get("key_events", []):
                            st.session_state["master_timeline"].append({
                                "timestamp": event.get("time", ""),
                                "source": "Audio Analysis",
                                "evidence_id": evidence["evidence_id"],
                                "event": f"[{event.get('source', 'Unknown')}] {event.get('event', '')}",
                                "priority": event.get("significance", "Medium"),
                            })
                
                # Display analysis results
                existing_results = [
                    r for r in st.session_state.get("audio_analysis_results", [])
                    if r.get("evidence_id") == evidence["evidence_id"]
                ]
                
                if existing_results:
                    result = existing_results[-1]
                    st.divider()
                    
                    # ── Summary Metrics ──
                    m1, m2, m3, m4 = st.columns(4)
                    with m1:
                        st.markdown(
                            render_metric_card(
                                "Speakers", str(len(result.get("speakers_identified", []))), "👥"
                            ),
                            unsafe_allow_html=True
                        )
                    with m2:
                        st.markdown(
                            render_metric_card(
                                "Duration", result.get("total_duration", "N/A"), "⏱️"
                            ),
                            unsafe_allow_html=True
                        )
                    with m3:
                        st.markdown(
                            render_metric_card(
                                "Key Events", str(len(result.get("key_events", []))), "🔑"
                            ),
                            unsafe_allow_html=True
                        )
                    with m4:
                        st.markdown(
                            render_metric_card(
                                "Quality", result.get("audio_quality", "N/A")[:8], "📊"
                            ),
                            unsafe_allow_html=True
                        )
                    
                    # ── Speaker Identification ──
                    st.markdown("#### 👥 Identified Speakers")
                    speaker_cols = st.columns(len(result.get("speakers_identified", ["N/A"])))
                    colors = ["#00d4ff", "#4caf50", "#ff9800", "#f44336", "#9c27b0"]
                    for i, speaker in enumerate(result.get("speakers_identified", [])):
                        with speaker_cols[i % len(speaker_cols)]:
                            color = colors[i % len(colors)]
                            st.markdown(
                                f'<div style="background: {color}22; border: 1px solid {color}; '
                                f'border-radius: 8px; padding: 10px; text-align: center;">'
                                f'<strong style="color: {color};">{speaker}</strong></div>',
                                unsafe_allow_html=True
                            )
                    
                    # ── Full Transcript ──
                    st.markdown("#### 📝 Full Transcript")
                    for entry in result.get("transcript", []):
                        speaker_color = colors[
                            result.get("speakers_identified", []).index(entry["speaker"]) % len(colors)
                        ] if entry["speaker"] in result.get("speakers_identified", []) else "#8892b0"
                        
                        st.markdown(
                            f'<div style="border-left: 3px solid {speaker_color}; padding: 8px 16px; '
                            f'margin: 4px 0; background: rgba(26,26,46,0.6); border-radius: 0 8px 8px 0;">'
                            f'<span style="color: #00d4ff; font-family: monospace; font-size: 0.85em;">'
                            f'{entry.get("timestamp", "")}</span> '
                            f'<strong style="color: {speaker_color};">{entry.get("speaker", "")}:</strong> '
                            f'<span style="color: #ccd6f6;">{entry.get("text", "")}</span> '
                            f'<span style="color: #4caf50; font-size: 0.8em;">({entry.get("confidence", 0):.0%})</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    
                    # ── Key Forensic Events Timeline ──
                    st.markdown("#### 🔑 Key Forensic Events (Chronological)")
                    if result.get("key_events"):
                        for event in result["key_events"]:
                            significance_color = "#f44336" if event.get("significance") == "Critical" else "#ff9800"
                            st.markdown(
                                render_timeline_event(
                                    event.get("time", ""),
                                    f"{event.get('event', '')} — *Significance: "
                                    f"<span style='color:{significance_color};'>{event.get('significance', 'N/A')}</span>*",
                                    event.get("source", "")
                                ),
                                unsafe_allow_html=True
                            )
                    else:
                        st.info("No critical forensic events extracted from this audio.")
                    
                    # ── Analysis Info ──
                    st.caption(
                        f"Transcription Model: {result.get('model_used', 'N/A')} | "
                        f"Language: {result.get('language', 'N/A')} | "
                        f"Analyzed: {result.get('analysis_timestamp', '')[:19]}"
                    )
    else:
        st.markdown("""
        <div class="evidence-card" style="text-align: center; padding: 40px;">
            <div style="font-size: 3em;">🎙️</div>
            <h3 style="color: #00d4ff;">No Audio Evidence Loaded</h3>
            <p style="color: #8892b0;">Upload witness statements or emergency call recordings above to begin transcription analysis.</p>
        </div>
        """, unsafe_allow_html=True)
