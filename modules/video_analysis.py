"""
CrimeVision AI - Video Analysis Module (Tab 3)
CCTV Video Analysis, Event Progression & Crime Classification.
"""

import streamlit as st
import numpy as np
import io
import random
from datetime import datetime
from typing import Optional

from config.settings import (
    generate_evidence_id, compute_file_hash,
    get_chain_of_custody_record, CRIME_CATEGORIES
)
from utils.styling import (
    render_evidence_id_badge, render_metric_card,
    render_timeline_event, render_threat_badge
)
from utils.ai_engine import analyze_video


def _extract_video_metadata(file_bytes: bytes, filename: str) -> dict:
    """Extract basic video metadata."""
    try:
        import cv2
        import tempfile
        import os
        
        # Write to temp file for OpenCV
        temp_path = os.path.join(tempfile.gettempdir(), f"cv_temp_{filename}")
        with open(temp_path, "wb") as f:
            f.write(file_bytes)
        
        cap = cv2.VideoCapture(temp_path)
        if cap.isOpened():
            fps = cap.get(cv2.CAP_PROP_FPS) or 30
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            cap.release()
            
            try:
                os.unlink(temp_path)
            except Exception:
                pass
            
            return {
                "fps": fps,
                "frame_count": frame_count,
                "width": width,
                "height": height,
                "duration_seconds": duration,
                "duration_formatted": f"{int(duration // 60)}:{int(duration % 60):02d}",
            }
        cap.release()
        try:
            os.unlink(temp_path)
        except Exception:
            pass
    except ImportError:
        pass
    except Exception:
        pass
    
    # Fallback metadata
    estimated_duration = len(file_bytes) / 500000  # very rough estimate
    return {
        "fps": 30,
        "frame_count": int(estimated_duration * 30),
        "width": 1920,
        "height": 1080,
        "duration_seconds": estimated_duration,
        "duration_formatted": f"{int(estimated_duration // 60)}:{int(estimated_duration % 60):02d}",
    }


def _extract_sample_frames(file_bytes: bytes, filename: str, num_frames: int = 4) -> list:
    """Extract sample frames from video for display."""
    frames = []
    try:
        import cv2
        import tempfile
        import os
        from PIL import Image
        
        temp_path = os.path.join(tempfile.gettempdir(), f"cv_frames_{filename}")
        with open(temp_path, "wb") as f:
            f.write(file_bytes)
        
        cap = cv2.VideoCapture(temp_path)
        if cap.isOpened():
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total_frames > 0:
                interval = max(1, total_frames // (num_frames + 1))
                for i in range(1, num_frames + 1):
                    frame_pos = min(i * interval, total_frames - 1)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
                    ret, frame = cap.read()
                    if ret:
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        pil_image = Image.fromarray(frame_rgb)
                        frames.append({
                            "image": pil_image,
                            "frame_number": frame_pos,
                            "timestamp": f"{frame_pos / cap.get(cv2.CAP_PROP_FPS):.1f}s"
                        })
        cap.release()
        try:
            os.unlink(temp_path)
        except Exception:
            pass
    except ImportError:
        pass
    except Exception:
        pass
    
    return frames


def render_video_analysis_tab():
    """Render the Video Analysis tab content."""
    st.markdown("## 🎬 CCTV Video Analysis & Event Progression")
    st.markdown(
        "Upload surveillance or CCTV footage for frame-by-frame forensic analysis. "
        "The system processes video frames to detect suspect trajectories, vehicle movements, "
        "and classifies events by **legal penal crime categories**."
    )
    
    st.divider()
    
    # ── Upload Section ──
    uploaded_files = st.file_uploader(
        "📂 Upload Video Evidence",
        type=["mp4", "avi", "mov", "mkv", "wmv", "flv", "webm"],
        accept_multiple_files=True,
        help="Supported: MP4, AVI, MOV, MKV, WMV, WebM. Max 500MB per file.",
        key="video_uploader"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            existing_ids = [e.get("filename") for e in st.session_state.get("video_evidence", [])]
            if uploaded_file.name in existing_ids:
                continue
            
            file_bytes = uploaded_file.read()
            uploaded_file.seek(0)
            
            evidence_id = generate_evidence_id()
            file_hash = compute_file_hash(file_bytes)
            custody_record = get_chain_of_custody_record(
                evidence_id, file_hash, "Video", uploaded_file.name,
                st.session_state.get("investigator_name", "Detective")
            )
            
            metadata = _extract_video_metadata(file_bytes, uploaded_file.name)
            
            st.session_state["video_evidence"].append({
                "evidence_id": evidence_id,
                "filename": uploaded_file.name,
                "file_hash": file_hash,
                "file_bytes": file_bytes,
                "metadata": metadata,
                "custody_record": custody_record,
                "ingestion_time": datetime.now().isoformat(),
            })
            st.session_state["custody_log"].append(custody_record)
        
        st.success(f"✅ {len(uploaded_files)} video(s) ingested into evidence chain")
    
    # ── Display & Analyze Video Evidence ──
    if st.session_state.get("video_evidence"):
        st.divider()
        st.markdown("### 🔍 Video Evidence & Frame Analysis")
        
        for idx, evidence in enumerate(st.session_state["video_evidence"]):
            with st.expander(
                f"🎥 {evidence['filename']} — `{evidence['evidence_id']}`",
                expanded=(idx == 0)
            ):
                st.markdown(
                    render_evidence_id_badge(evidence["evidence_id"]),
                    unsafe_allow_html=True
                )
                st.caption(f"SHA-256: `{evidence['file_hash'][:32]}...`")
                
                meta = evidence.get("metadata", {})
                
                # Video metadata cards
                m1, m2, m3, m4, m5 = st.columns(5)
                with m1:
                    st.markdown(
                        render_metric_card("Duration", meta.get("duration_formatted", "N/A"), "⏱️"),
                        unsafe_allow_html=True
                    )
                with m2:
                    st.markdown(
                        render_metric_card("FPS", f"{meta.get('fps', 'N/A'):.0f}", "🎞️"),
                        unsafe_allow_html=True
                    )
                with m3:
                    st.markdown(
                        render_metric_card("Frames", str(meta.get("frame_count", "N/A")), "📊"),
                        unsafe_allow_html=True
                    )
                with m4:
                    st.markdown(
                        render_metric_card("Resolution", f"{meta.get('width', '?')}×{meta.get('height', '?')}", "📐"),
                        unsafe_allow_html=True
                    )
                with m5:
                    st.markdown(
                        render_metric_card("Size", f"{len(evidence['file_bytes']) / (1024*1024):.1f} MB", "💾"),
                        unsafe_allow_html=True
                    )
                
                # Video playback
                st.markdown("**▶️ Video Playback**")
                try:
                    st.video(evidence["file_bytes"], format=f"video/{evidence['filename'].split('.')[-1]}")
                except Exception:
                    st.warning("Video playback not available for this format in browser.")
                
                # Frame sampling config
                st.markdown("**⚙️ Frame Sampling Configuration**")
                col_cfg1, col_cfg2 = st.columns(2)
                with col_cfg1:
                    num_frames = st.slider(
                        "Frames to sample",
                        min_value=3, max_value=20, value=6,
                        key=f"frames_{evidence['evidence_id']}",
                        help="Number of evenly-spaced frames to extract and analyze"
                    )
                with col_cfg2:
                    st.info(f"Sampling interval: ~{meta.get('duration_seconds', 30) / num_frames:.1f}s between frames")
                
                # Sample frame display
                sample_frames = _extract_sample_frames(evidence["file_bytes"], evidence["filename"], min(num_frames, 4))
                if sample_frames:
                    st.markdown("**📸 Sample Frames**")
                    frame_cols = st.columns(len(sample_frames))
                    for i, frame_data in enumerate(sample_frames):
                        with frame_cols[i]:
                            st.image(
                                frame_data["image"],
                                caption=f"Frame #{frame_data['frame_number']} ({frame_data['timestamp']})",
                                use_container_width=True
                            )
                
                # Analysis button
                if st.button(
                    f"🔬 Run Video Forensic Analysis",
                    key=f"btn_video_{evidence['evidence_id']}",
                    type="primary",
                    use_container_width=True
                ):
                    with st.spinner("🔄 Processing frames: object detection, tracking, and crime classification..."):
                        result = analyze_video(
                            evidence["filename"],
                            evidence["file_bytes"],
                            num_frames
                        )
                        result["evidence_id"] = evidence["evidence_id"]
                        
                        st.session_state["video_analysis_results"] = [
                            r for r in st.session_state["video_analysis_results"]
                            if r.get("evidence_id") != evidence["evidence_id"]
                        ]
                        st.session_state["video_analysis_results"].append(result)
                        
                        # Add events to master timeline
                        for event in result.get("events", []):
                            st.session_state["master_timeline"].append({
                                "timestamp": event.get("timestamp", ""),
                                "source": "Video Analysis",
                                "evidence_id": evidence["evidence_id"],
                                "event": f"{event.get('description', '')} [{event.get('crime_category', '')}]",
                                "priority": "High" if event.get("confidence", 0) > 0.85 else "Medium",
                            })
                
                # Display analysis results
                existing_results = [
                    r for r in st.session_state.get("video_analysis_results", [])
                    if r.get("evidence_id") == evidence["evidence_id"]
                ]
                
                if existing_results:
                    result = existing_results[-1]
                    st.divider()
                    
                    # Summary metrics
                    s1, s2, s3, s4 = st.columns(4)
                    with s1:
                        st.markdown(
                            render_metric_card("Events Logged", str(len(result.get("events", []))), "📋"),
                            unsafe_allow_html=True
                        )
                    with s2:
                        st.markdown(
                            render_metric_card("Persons", str(result.get("total_persons_detected", 0)), "👤"),
                            unsafe_allow_html=True
                        )
                    with s3:
                        st.markdown(
                            render_metric_card("Vehicles", str(result.get("vehicles_detected", 0)), "🚗"),
                            unsafe_allow_html=True
                        )
                    with s4:
                        st.markdown(
                            render_metric_card("Crime Type", result.get("primary_crime_classification", "N/A")[:18], "⚖️"),
                            unsafe_allow_html=True
                        )
                    
                    # ── Chronological Event Log Table ──
                    st.markdown("#### 📋 Chronological Event Log")
                    
                    # Build event data for table
                    event_table_data = []
                    for event in result.get("events", []):
                        event_table_data.append({
                            "Frame": event.get("frame", ""),
                            "Timestamp": event.get("timestamp", ""),
                            "Event Description": event.get("description", ""),
                            "Detection Type": event.get("detection_type", ""),
                            "Crime Category": event.get("crime_category", ""),
                            "Confidence": f"{event.get('confidence', 0):.1%}",
                            "Objects": event.get("objects_in_frame", 0),
                        })
                    
                    if event_table_data:
                        st.dataframe(
                            event_table_data,
                            use_container_width=True,
                            hide_index=True,
                        )
                    
                    # ── Event Timeline (Visual) ──
                    st.markdown("#### 🕐 Event Progression Timeline")
                    for event in result.get("events", []):
                        st.markdown(
                            render_timeline_event(
                                event.get("timestamp", ""),
                                f"{event.get('description', '')} — "
                                f"*{event.get('crime_category', '')}* "
                                f"(Confidence: {event.get('confidence', 0):.0%})",
                                event.get("detection_type", "")
                            ),
                            unsafe_allow_html=True
                        )
                    
                    # ── Suspect Trajectory ──
                    st.markdown("#### 🗺️ Suspect Trajectory")
                    trajectory = result.get("suspect_trajectory", [])
                    if trajectory:
                        traj_cols = st.columns(len(trajectory))
                        for i, point in enumerate(trajectory):
                            with traj_cols[i]:
                                arrow = "🟢" if point.get("action") == "Entry" else ("🔴" if point.get("action") == "Departure" else "🟡")
                                st.markdown(
                                    f'<div style="background: rgba(0,212,255,0.1); border: 1px solid #00d4ff33; '
                                    f'border-radius: 10px; padding: 15px; text-align: center;">'
                                    f'<div style="font-size: 1.5em;">{arrow}</div>'
                                    f'<div style="color: #00d4ff; font-weight: 700;">{point.get("action", "")}</div>'
                                    f'<div style="color: #ccd6f6; font-size: 0.9em;">{point.get("position", "")}</div>'
                                    f'<div style="color: #8892b0; font-size: 0.8em;">{point.get("time", "")}</div>'
                                    f'</div>',
                                    unsafe_allow_html=True
                                )
                                if i < len(trajectory) - 1:
                                    st.markdown(
                                        '<div style="text-align: center; color: #00d4ff; font-size: 1.2em;">→</div>',
                                        unsafe_allow_html=True
                                    )
                    
                    st.caption(
                        f"Analysis Model: {result.get('model_used', 'N/A')} | "
                        f"Frames Analyzed: {result.get('total_frames_analyzed', 'N/A')} | "
                        f"Analyzed: {result.get('analysis_timestamp', '')[:19]}"
                    )
    else:
        st.markdown("""
        <div class="evidence-card" style="text-align: center; padding: 40px;">
            <div style="font-size: 3em;">🎬</div>
            <h3 style="color: #00d4ff;">No Video Evidence Loaded</h3>
            <p style="color: #8892b0;">Upload CCTV or surveillance footage above to begin video forensic analysis.</p>
        </div>
        """, unsafe_allow_html=True)
