"""
CrimeVision AI - Multimodal Fusion & Evidence Chat Module (Tab 4)
Unified forensic timeline and grounded RAG-based conversational interface.
"""

import streamlit as st
import json
from datetime import datetime
from typing import List, Dict, Any

from config.settings import THREAT_LEVELS
from utils.styling import (
    render_metric_card, render_timeline_event,
    render_evidence_id_badge, render_threat_badge
)
from utils.ai_engine import chat_with_evidence


def _build_master_timeline() -> List[Dict[str, Any]]:
    """Consolidate all evidence sources into a unified master timeline."""
    timeline = []
    
    # Image analysis events
    for result in st.session_state.get("image_analysis_results", []):
        for obj in result.get("detected_objects", []):
            timeline.append({
                "timestamp": result.get("analysis_timestamp", ""),
                "source": "🖼️ Image",
                "evidence_id": result.get("evidence_id", "N/A"),
                "event": f"Detected: {obj['name']} (Confidence: {obj['confidence']:.0%})",
                "priority": obj.get("priority", "Medium"),
                "details": {
                    "type": "detection",
                    "object": obj["name"],
                    "confidence": obj["confidence"],
                    "bbox": obj.get("bbox", ""),
                    "scene_class": result.get("scene_classification", ""),
                    "threat": result.get("threat_level", ""),
                }
            })
        # Add scene-level event
        timeline.append({
            "timestamp": result.get("analysis_timestamp", ""),
            "source": "🖼️ Image",
            "evidence_id": result.get("evidence_id", "N/A"),
            "event": f"Scene classified as {result.get('scene_classification', 'Unknown')} — "
                     f"Threat Level: {result.get('threat_level', 'Unknown')}",
            "priority": result.get("threat_level", "Medium"),
            "details": {"type": "classification"}
        })
    
    # Audio analysis events
    for result in st.session_state.get("audio_analysis_results", []):
        for entry in result.get("transcript", []):
            timeline.append({
                "timestamp": entry.get("timestamp", ""),
                "source": "🎙️ Audio",
                "evidence_id": result.get("evidence_id", "N/A"),
                "event": f"[{entry.get('speaker', 'Unknown')}] \"{entry.get('text', '')}\"",
                "priority": "Medium",
                "details": {
                    "type": "transcript",
                    "speaker": entry.get("speaker", ""),
                    "confidence": entry.get("confidence", 0),
                }
            })
        for event in result.get("key_events", []):
            timeline.append({
                "timestamp": event.get("time", ""),
                "source": "🎙️ Audio",
                "evidence_id": result.get("evidence_id", "N/A"),
                "event": f"KEY EVENT: {event.get('event', '')}",
                "priority": event.get("significance", "High"),
                "details": {"type": "key_event", "source_speaker": event.get("source", "")}
            })
    
    # Video analysis events
    for result in st.session_state.get("video_analysis_results", []):
        for event in result.get("events", []):
            timeline.append({
                "timestamp": event.get("timestamp", ""),
                "source": "🎬 Video",
                "evidence_id": result.get("evidence_id", "N/A"),
                "event": f"Frame #{event.get('frame', '?')}: {event.get('description', '')} "
                         f"[{event.get('crime_category', '')}]",
                "priority": "High" if event.get("confidence", 0) > 0.85 else "Medium",
                "details": {
                    "type": "video_event",
                    "frame": event.get("frame", 0),
                    "detection_type": event.get("detection_type", ""),
                    "crime_category": event.get("crime_category", ""),
                    "confidence": event.get("confidence", 0),
                }
            })
        # Trajectory events
        for point in result.get("suspect_trajectory", []):
            timeline.append({
                "timestamp": point.get("time", ""),
                "source": "🎬 Video",
                "evidence_id": result.get("evidence_id", "N/A"),
                "event": f"Suspect {point.get('action', 'detected')} at {point.get('position', 'unknown')}",
                "priority": "High",
                "details": {"type": "trajectory"}
            })
    
    # Sort by timestamp
    timeline.sort(key=lambda x: x.get("timestamp", ""))
    return timeline


def _get_evidence_summary() -> Dict[str, Any]:
    """Generate a summary of all available evidence for display."""
    image_results = st.session_state.get("image_analysis_results", [])
    audio_results = st.session_state.get("audio_analysis_results", [])
    video_results = st.session_state.get("video_analysis_results", [])
    
    total_detections = sum(
        len(r.get("detected_objects", [])) for r in image_results
    )
    total_speakers = set()
    for r in audio_results:
        total_speakers.update(r.get("speakers_identified", []))
    
    total_video_events = sum(
        len(r.get("events", [])) for r in video_results
    )
    
    # Highest threat
    threats = [r.get("threat_level", "Low") for r in image_results]
    threat_order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
    max_threat = max(threats, key=lambda t: threat_order.get(t, 0)) if threats else "N/A"
    
    return {
        "total_evidence_items": (
            len(st.session_state.get("image_evidence", []))
            + len(st.session_state.get("audio_evidence", []))
            + len(st.session_state.get("video_evidence", []))
        ),
        "analyzed_items": len(image_results) + len(audio_results) + len(video_results),
        "total_detections": total_detections,
        "total_speakers": len(total_speakers),
        "total_video_events": total_video_events,
        "highest_threat": max_threat,
        "scene_classifications": list(set(
            r.get("scene_classification", "") for r in image_results if r.get("scene_classification")
        )),
    }


def render_multimodal_fusion_tab():
    """Render the Multimodal Fusion & Evidence Chat tab."""
    st.markdown("## 🔗 Multimodal Fusion & Grounded Evidence Chat")
    st.markdown(
        "This module fuses all image, audio, and video analysis results into a "
        "**unified master forensic timeline**. Use the grounded chat interface to "
        "interrogate evidence in natural language with strict citation requirements."
    )
    
    st.divider()
    
    # ── Evidence Summary Dashboard ──
    summary = _get_evidence_summary()
    
    st.markdown("### 📊 Evidence Fusion Dashboard")
    
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        st.markdown(
            render_metric_card("Total Evidence", str(summary["total_evidence_items"]), "📦"),
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            render_metric_card("Analyzed", str(summary["analyzed_items"]), "✅"),
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            render_metric_card("Detections", str(summary["total_detections"]), "🔍"),
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            render_metric_card("Speakers", str(summary["total_speakers"]), "👥"),
            unsafe_allow_html=True
        )
    with m5:
        st.markdown(
            render_metric_card("Video Events", str(summary["total_video_events"]), "🎬"),
            unsafe_allow_html=True
        )
    with m6:
        threat = summary["highest_threat"]
        st.markdown(
            render_metric_card("Max Threat", threat, "⚠️"),
            unsafe_allow_html=True
        )
    
    st.divider()
    
    # ── Master Timeline ──
    col_timeline, col_chat = st.columns([1, 1])
    
    with col_timeline:
        st.markdown("### 📅 Master Forensic Event Ledger")
        
        master_timeline = _build_master_timeline()
        
        if master_timeline:
            # Filter controls
            source_filter = st.multiselect(
                "Filter by Source",
                options=["🖼️ Image", "🎙️ Audio", "🎬 Video"],
                default=["🖼️ Image", "🎙️ Audio", "🎬 Video"],
                key="timeline_filter"
            )
            
            priority_filter = st.multiselect(
                "Filter by Priority",
                options=["Critical", "High", "Medium", "Low"],
                default=["Critical", "High", "Medium"],
                key="priority_filter"
            )
            
            filtered = [
                e for e in master_timeline
                if e.get("source", "") in source_filter
                and e.get("priority", "") in priority_filter
            ]
            
            st.caption(f"Showing {len(filtered)} of {len(master_timeline)} events")
            
            # Display timeline
            timeline_container = st.container(height=500)
            with timeline_container:
                for event in filtered:
                    priority_color = {
                        "Critical": "#9c27b0",
                        "High": "#f44336",
                        "Medium": "#ff9800",
                        "Low": "#4caf50"
                    }.get(event.get("priority", "Medium"), "#8892b0")
                    
                    st.markdown(
                        f'<div style="border-left: 3px solid {priority_color}; padding: 8px 16px; '
                        f'margin: 4px 0; background: rgba(26,26,46,0.6); border-radius: 0 8px 8px 0;">'
                        f'<div style="display: flex; justify-content: space-between; align-items: center;">'
                        f'<span style="color: #00d4ff; font-family: monospace; font-size: 0.85em;">'
                        f'{event.get("timestamp", "N/A")}</span>'
                        f'<span style="font-size: 0.8em; color: {priority_color};">'
                        f'{event.get("priority", "")}</span>'
                        f'</div>'
                        f'<div style="color: #8892b0; font-size: 0.8em; margin: 2px 0;">'
                        f'{event.get("source", "")} • {event.get("evidence_id", "")}</div>'
                        f'<div style="color: #ccd6f6; margin-top: 4px;">{event.get("event", "")}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            
            # Export timeline data
            if st.button("📥 Export Timeline as JSON", key="export_timeline"):
                timeline_json = json.dumps(filtered, indent=2, default=str)
                st.download_button(
                    "⬇️ Download JSON",
                    data=timeline_json,
                    file_name=f"forensic_timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    key="download_timeline"
                )
        else:
            st.markdown("""
            <div class="evidence-card" style="text-align: center; padding: 30px;">
                <div style="font-size: 2em;">📅</div>
                <h4 style="color: #00d4ff;">No Timeline Events</h4>
                <p style="color: #8892b0;">Analyze evidence in the Image, Audio, and Video tabs to populate the master timeline.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # ── Grounded Evidence Chat ──
    with col_chat:
        st.markdown("### 💬 Forensic Evidence Chat (RAG)")
        st.caption(
            "Ask questions about the evidence. All responses are grounded in submitted "
            "evidence with zero hallucination. Evidence IDs are cited in every answer."
        )
        
        # Chat container
        chat_container = st.container(height=400)
        with chat_container:
            for msg in st.session_state.get("chat_history", []):
                if msg["role"] == "user":
                    st.markdown(
                        f'<div class="chat-user">🕵️ <strong>Investigator:</strong> {msg["content"]}</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="chat-ai">🤖 <strong>CrimeVision AI:</strong><br>{msg["content"]}</div>',
                        unsafe_allow_html=True
                    )
        
        # Example queries
        st.markdown("**💡 Suggested Queries:**")
        example_queries = [
            "Was a weapon visible before the suspect fled?",
            "Summarize the suspect's trajectory from entry to exit.",
            "What did witnesses report about the incident?",
            "Create a chronological timeline of all events.",
            "What is the overall threat assessment?",
        ]
        
        eq_cols = st.columns(2)
        for i, query in enumerate(example_queries):
            with eq_cols[i % 2]:
                if st.button(f"💬 {query[:45]}...", key=f"eq_{i}", use_container_width=True):
                    st.session_state["_pending_query"] = query
        
        # Chat input
        user_query = st.chat_input(
            "Ask about the evidence...",
            key="evidence_chat_input"
        )
        
        # Handle pending query from example buttons
        if st.session_state.get("_pending_query"):
            user_query = st.session_state.pop("_pending_query")
        
        if user_query:
            # Add user message
            st.session_state["chat_history"].append({
                "role": "user",
                "content": user_query,
                "timestamp": datetime.now().isoformat(),
            })
            
            # Get AI response
            with st.spinner("🔄 Analyzing evidence context..."):
                response = chat_with_evidence(user_query)
            
            # Add AI response
            st.session_state["chat_history"].append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat(),
            })
            
            st.rerun()
        
        # Clear chat
        if st.session_state.get("chat_history"):
            if st.button("🗑️ Clear Chat History", key="clear_chat"):
                st.session_state["chat_history"] = []
                st.rerun()
