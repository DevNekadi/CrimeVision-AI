"""
CrimeVision AI - Image Analysis Module (Tab 1)
Crime Scene Visual Evidence Tagger with RT-DETR simulation.
"""

import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import random
from datetime import datetime
from typing import Optional

from config.settings import (
    generate_evidence_id, compute_file_hash, 
    get_chain_of_custody_record, THREAT_LEVELS
)
from utils.styling import (
    render_threat_badge, render_evidence_id_badge,
    render_detection_box, render_metric_card
)
from utils.ai_engine import analyze_image


def _draw_detections_on_image(image: Image.Image, detections: list) -> Image.Image:
    """Draw bounding boxes and labels on the image for detected objects."""
    draw_img = image.copy()
    draw = ImageDraw.Draw(draw_img)
    
    # Color map for different priorities
    priority_colors = {
        "Critical": "#ff0000",
        "High": "#ff6600",
        "Medium": "#ffcc00",
        "Low": "#00ff00",
    }
    
    for det in detections:
        try:
            bbox = eval(det.get("bbox", "[0,0,100,100]")) if isinstance(det.get("bbox"), str) else det.get("bbox", [0,0,100,100])
            color = priority_colors.get(det.get("priority", "Medium"), "#00d4ff")
            
            # Scale bbox to image size if needed
            w, h = draw_img.size
            x1 = min(int(bbox[0]), w - 1)
            y1 = min(int(bbox[1]), h - 1)
            x2 = min(int(bbox[2]), w - 1)
            y2 = min(int(bbox[3]), h - 1)
            
            # Draw rectangle
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            
            # Draw label background
            label = f"{det['name']} ({det['confidence']:.0%})"
            text_bbox = draw.textbbox((x1, y1 - 18), label)
            draw.rectangle([text_bbox[0] - 2, text_bbox[1] - 2, text_bbox[2] + 2, text_bbox[3] + 2], fill=color)
            draw.text((x1, y1 - 18), label, fill="white")
        except Exception:
            continue
    
    return draw_img


def render_image_analysis_tab():
    """Render the Image Analysis tab content."""
    st.markdown("## 📸 Crime Scene Visual Evidence Tagger")
    st.markdown(
        "Upload crime scene photographs for AI-powered forensic object detection. "
        "The system simulates **RT-DETR** to identify persons, weapons, blood spatter, "
        "and forced entry points with confidence scores and spatial coordinates."
    )
    
    st.divider()
    
    # ── Upload Section ──
    uploaded_files = st.file_uploader(
        "📂 Upload Crime Scene Image(s)",
        type=["jpg", "jpeg", "png", "bmp", "tiff", "webp"],
        accept_multiple_files=True,
        help="Supported formats: JPG, PNG, BMP, TIFF, WebP. Max 500MB per file.",
        key="image_uploader"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Check if already processed
            existing_ids = [e.get("filename") for e in st.session_state.get("image_evidence", [])]
            if uploaded_file.name in existing_ids:
                continue
            
            file_bytes = uploaded_file.read()
            uploaded_file.seek(0)
            
            # Generate evidence tracking
            evidence_id = generate_evidence_id()
            file_hash = compute_file_hash(file_bytes)
            custody_record = get_chain_of_custody_record(
                evidence_id, file_hash, "Image", uploaded_file.name,
                st.session_state.get("investigator_name", "Detective")
            )
            
            # Store evidence
            st.session_state["image_evidence"].append({
                "evidence_id": evidence_id,
                "filename": uploaded_file.name,
                "file_hash": file_hash,
                "file_bytes": file_bytes,
                "custody_record": custody_record,
                "ingestion_time": datetime.now().isoformat(),
            })
            st.session_state["custody_log"].append(custody_record)
        
        st.success(f"✅ {len(uploaded_files)} image(s) ingested into evidence chain")
    
    # ── Display & Analyze Stored Evidence ──
    if st.session_state.get("image_evidence"):
        st.divider()
        st.markdown("### 🔍 Evidence Gallery & Analysis")
        
        for idx, evidence in enumerate(st.session_state["image_evidence"]):
            with st.expander(
                f"📷 {evidence['filename']} — `{evidence['evidence_id']}`",
                expanded=(idx == 0)
            ):
                # Chain of custody badge
                st.markdown(
                    render_evidence_id_badge(evidence["evidence_id"]),
                    unsafe_allow_html=True
                )
                st.caption(f"SHA-256: `{evidence['file_hash'][:32]}...`")
                
                col_img, col_info = st.columns([2, 1])
                
                with col_img:
                    try:
                        image = Image.open(io.BytesIO(evidence["file_bytes"]))
                        st.image(image, caption=f"Original: {evidence['filename']}", use_container_width=True)
                    except Exception as e:
                        st.error(f"Cannot display image: {e}")
                
                with col_info:
                    st.markdown("**📋 Evidence Metadata**")
                    try:
                        image = Image.open(io.BytesIO(evidence["file_bytes"]))
                        st.write(f"- **Dimensions:** {image.size[0]} × {image.size[1]} px")
                        st.write(f"- **Format:** {image.format or 'Unknown'}")
                        st.write(f"- **Mode:** {image.mode}")
                    except Exception:
                        pass
                    st.write(f"- **Size:** {len(evidence['file_bytes']) / 1024:.1f} KB")
                    st.write(f"- **Ingested:** {evidence['ingestion_time'][:19]}")
                
                # Analysis button
                analysis_key = f"analysis_{evidence['evidence_id']}"
                
                if st.button(
                    f"🔬 Run Forensic Analysis",
                    key=f"btn_{evidence['evidence_id']}",
                    type="primary",
                    use_container_width=True
                ):
                    with st.spinner("🔄 Running RT-DETR object detection and forensic scene analysis..."):
                        result = analyze_image(evidence["filename"], evidence["file_bytes"])
                        result["evidence_id"] = evidence["evidence_id"]
                        
                        # Store result
                        # Remove old result for same evidence if re-analyzing
                        st.session_state["image_analysis_results"] = [
                            r for r in st.session_state["image_analysis_results"]
                            if r.get("evidence_id") != evidence["evidence_id"]
                        ]
                        st.session_state["image_analysis_results"].append(result)
                        
                        # Add to master timeline
                        for obj in result.get("detected_objects", []):
                            st.session_state["master_timeline"].append({
                                "timestamp": result["analysis_timestamp"],
                                "source": "Image Analysis",
                                "evidence_id": evidence["evidence_id"],
                                "event": f"Detected: {obj['name']} (Confidence: {obj['confidence']:.0%})",
                                "priority": obj.get("priority", "Medium"),
                            })
                
                # Display analysis results if available
                existing_results = [
                    r for r in st.session_state.get("image_analysis_results", [])
                    if r.get("evidence_id") == evidence["evidence_id"]
                ]
                
                if existing_results:
                    result = existing_results[-1]
                    st.divider()
                    
                    # ── Summary Metrics ──
                    m1, m2, m3, m4 = st.columns(4)
                    with m1:
                        st.markdown(
                            render_metric_card("Threat Level", result.get("threat_level", "N/A"), "⚠️"),
                            unsafe_allow_html=True
                        )
                    with m2:
                        st.markdown(
                            render_metric_card("Classification", result.get("scene_classification", "N/A"), "🏷️"),
                            unsafe_allow_html=True
                        )
                    with m3:
                        st.markdown(
                            render_metric_card("Objects Found", str(len(result.get("detected_objects", []))), "🔎"),
                            unsafe_allow_html=True
                        )
                    with m4:
                        st.markdown(
                            render_metric_card("Model", result.get("model_used", "N/A")[:12], "🤖"),
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("")
                    
                    # ── Threat Level Badge ──
                    threat = result.get("threat_level", "Medium")
                    st.markdown(
                        f"**Threat Assessment:** {render_threat_badge(threat)}",
                        unsafe_allow_html=True
                    )
                    
                    # ── Annotated Image ──
                    st.markdown("#### 🖼️ Annotated Evidence (Detected Objects)")
                    try:
                        img = Image.open(io.BytesIO(evidence["file_bytes"]))
                        annotated = _draw_detections_on_image(img, result.get("detected_objects", []))
                        st.image(annotated, caption="AI-Annotated Crime Scene", use_container_width=True)
                    except Exception:
                        st.info("Annotation overlay unavailable for this image format.")
                    
                    # ── Detected Objects ──
                    st.markdown("#### 🔎 Detected Forensic Objects")
                    for obj in result.get("detected_objects", []):
                        st.markdown(
                            render_detection_box(
                                obj["name"],
                                obj["confidence"],
                                f"BBox: {obj.get('bbox', 'N/A')}"
                            ),
                            unsafe_allow_html=True
                        )
                    
                    # ── Scene Description ──
                    st.markdown("#### 📝 Scene Description")
                    st.info(result.get("scene_description", "No description available."))
                    
                    # ── Hypotheses ──
                    st.markdown("#### 🧠 Scenario Hypotheses")
                    for h in result.get("hypotheses", []):
                        st.markdown(f"- {h}")
                    
                    # ── Investigative Leads ──
                    st.markdown("#### 🎯 Prioritized Investigative Leads")
                    for i, lead in enumerate(result.get("investigative_leads", []), 1):
                        st.markdown(f"**{i}.** {lead}")
    else:
        st.markdown("""
        <div class="evidence-card" style="text-align: center; padding: 40px;">
            <div style="font-size: 3em;">📸</div>
            <h3 style="color: #00d4ff;">No Image Evidence Loaded</h3>
            <p style="color: #8892b0;">Upload crime scene photographs above to begin forensic analysis.</p>
        </div>
        """, unsafe_allow_html=True)
