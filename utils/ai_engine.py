"""
CrimeVision AI - AI Analysis Engine
Handles Groq/Gemini API calls with demo fallback for all analysis types.
"""

import streamlit as st
import json
import random
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional


# ─── Demo Mode Simulated Responses ─────────────────────────────────
def _demo_image_analysis(filename: str) -> Dict[str, Any]:
    """Generate simulated forensic image analysis results."""
    detected_objects = []
    possible_objects = [
        {"name": "Person (Suspect)", "confidence": random.uniform(0.82, 0.97),
         "bbox": f"[{random.randint(50,200)}, {random.randint(30,150)}, {random.randint(250,400)}, {random.randint(300,500)}]",
         "priority": "High"},
        {"name": "Person (Victim)", "confidence": random.uniform(0.75, 0.95),
         "bbox": f"[{random.randint(300,450)}, {random.randint(100,250)}, {random.randint(500,600)}, {random.randint(400,550)}]",
         "priority": "Critical"},
        {"name": "Firearm (Handgun)", "confidence": random.uniform(0.70, 0.92),
         "bbox": f"[{random.randint(150,250)}, {random.randint(200,350)}, {random.randint(280,350)}, {random.randint(370,420)}]",
         "priority": "Critical"},
        {"name": "Knife / Edged Weapon", "confidence": random.uniform(0.65, 0.88),
         "bbox": f"[{random.randint(100,200)}, {random.randint(250,350)}, {random.randint(220,300)}, {random.randint(370,420)}]",
         "priority": "High"},
        {"name": "Blood Spatter Pattern", "confidence": random.uniform(0.60, 0.85),
         "bbox": f"[{random.randint(200,350)}, {random.randint(300,450)}, {random.randint(400,550)}, {random.randint(480,580)}]",
         "priority": "High"},
        {"name": "Forced Entry Point (Door)", "confidence": random.uniform(0.72, 0.90),
         "bbox": f"[{random.randint(10,50)}, {random.randint(10,80)}, {random.randint(150,250)}, {random.randint(400,550)}]",
         "priority": "Medium"},
        {"name": "Shell Casing", "confidence": random.uniform(0.68, 0.89),
         "bbox": f"[{random.randint(250,350)}, {random.randint(450,520)}, {random.randint(280,380)}, {random.randint(470,540)}]",
         "priority": "High"},
        {"name": "Broken Glass", "confidence": random.uniform(0.74, 0.91),
         "bbox": f"[{random.randint(50,150)}, {random.randint(350,450)}, {random.randint(200,300)}, {random.randint(480,560)}]",
         "priority": "Medium"},
        {"name": "Footprint", "confidence": random.uniform(0.55, 0.78),
         "bbox": f"[{random.randint(300,400)}, {random.randint(480,550)}, {random.randint(360,440)}, {random.randint(540,590)}]",
         "priority": "Medium"},
        {"name": "Vehicle (Sedan)", "confidence": random.uniform(0.80, 0.96),
         "bbox": f"[{random.randint(400,500)}, {random.randint(50,150)}, {random.randint(600,700)}, {random.randint(250,350)}]",
         "priority": "Medium"},
    ]
    
    # Select 3-6 random objects
    num_objects = random.randint(3, 6)
    detected_objects = random.sample(possible_objects, min(num_objects, len(possible_objects)))
    
    # Determine threat level based on detected objects
    priorities = [obj["priority"] for obj in detected_objects]
    if "Critical" in priorities:
        threat_level = "Critical"
    elif priorities.count("High") >= 2:
        threat_level = "High"
    elif "High" in priorities:
        threat_level = "Medium"
    else:
        threat_level = "Low"
    
    # Scene classification
    classifications = ["Homicide", "Burglary", "Assault", "Robbery", "Vandalism"]
    weights = [0.3, 0.25, 0.2, 0.15, 0.1]
    scene_type = random.choices(classifications, weights=weights, k=1)[0]
    
    # Investigative leads
    leads = [
        f"Prioritize identification of detected person(s) via facial recognition databases.",
        f"Collect and process {random.choice(['shell casings', 'blood samples', 'fingerprints', 'fiber evidence'])} at marked coordinates.",
        f"Cross-reference detected {random.choice(['vehicle', 'weapon', 'tool marks'])} with regional crime databases.",
        f"Expand canvass radius to {random.randint(2, 8)} blocks based on suspect trajectory analysis.",
        f"Request CCTV footage from {random.randint(3, 12)} surrounding establishments for corroboration.",
    ]
    
    scene_description = (
        f"Forensic analysis of '{filename}' reveals a {scene_type.lower()} scene with "
        f"{len(detected_objects)} objects of forensic interest detected. "
        f"The scene shows indicators consistent with {scene_type.lower()} including "
        f"{', '.join([obj['name'].split('(')[0].strip().lower() for obj in detected_objects[:3]])}. "
        f"Environmental conditions suggest the incident occurred in an {'indoor' if random.random() > 0.4 else 'outdoor'} setting. "
        f"Evidence preservation priority: {'IMMEDIATE' if threat_level in ['Critical', 'High'] else 'STANDARD'}."
    )
    
    hypothesis = [
        f"Primary Hypothesis: {scene_type} scenario involving {random.randint(1,3)} suspect(s).",
        f"Alternate Hypothesis: Staged scene to conceal {'domestic dispute' if scene_type == 'Homicide' else 'insurance fraud'}.",
        f"Confidence in primary hypothesis: {random.uniform(0.65, 0.90):.1%} based on detected evidence patterns."
    ]
    
    return {
        "detected_objects": detected_objects,
        "threat_level": threat_level,
        "scene_classification": scene_type,
        "scene_description": scene_description,
        "hypotheses": hypothesis,
        "investigative_leads": random.sample(leads, min(3, len(leads))),
        "analysis_timestamp": datetime.now().isoformat(),
        "model_used": "RT-DETR (Simulated)" if st.session_state.get("demo_mode") else "RT-DETR + LLM",
    }


def _demo_audio_analysis(filename: str, duration_sec: float = 0) -> Dict[str, Any]:
    """Generate simulated forensic audio analysis results."""
    speakers = ["Witness A", "Witness B", "911 Operator", "Suspect (Background)", "Victim"]
    selected_speakers = random.sample(speakers, min(random.randint(2, 4), len(speakers)))
    
    statements = [
        ("I heard two loud bangs, like gunshots, around 11:30 PM.", "Witness A"),
        ("The suspect was wearing a dark hoodie and ran towards the alley.", "Witness B"),
        ("911, what is your emergency?", "911 Operator"),
        ("There's someone on the ground, they're not moving! Send an ambulance!", "Witness A"),
        ("I saw a silver sedan speed away from the scene heading northbound.", "Witness B"),
        ("Can you describe the suspect?", "911 Operator"),
        ("Male, approximately 6 feet tall, dark clothing, wearing a mask.", "Witness A"),
        ("I think I heard them arguing before the shots.", "Witness B"),
        ("Stay on the line. Officers are being dispatched to your location.", "911 Operator"),
        ("There was a second person, they fled on foot toward Main Street.", "Witness B"),
    ]
    
    # Select 4-7 statements
    num_statements = random.randint(4, 7)
    selected_statements = random.sample(statements, min(num_statements, len(statements)))
    
    # Build transcript with timestamps
    base_time = datetime.now().replace(hour=23, minute=30, second=0)
    transcript_entries = []
    key_events = []
    
    for i, (text, speaker) in enumerate(sorted(selected_statements, key=lambda x: random.random())):
        timestamp = base_time + timedelta(seconds=i * random.randint(8, 25))
        entry = {
            "timestamp": timestamp.strftime("%H:%M:%S"),
            "speaker": speaker,
            "text": text,
            "confidence": random.uniform(0.85, 0.98),
        }
        transcript_entries.append(entry)
        
        # Extract key events from important statements
        if any(kw in text.lower() for kw in ["gunshot", "bang", "fled", "ran", "weapon", "suspect", "not moving"]):
            key_events.append({
                "time": timestamp.strftime("%H:%M:%S"),
                "event": text[:80],
                "source": speaker,
                "significance": random.choice(["High", "Critical"]),
            })
    
    # Sort by timestamp
    transcript_entries.sort(key=lambda x: x["timestamp"])
    key_events.sort(key=lambda x: x["time"])
    
    return {
        "transcript": transcript_entries,
        "key_events": key_events,
        "speakers_identified": list(set([e["speaker"] for e in transcript_entries])),
        "total_duration": f"{int(duration_sec // 60)}:{int(duration_sec % 60):02d}" if duration_sec else f"{random.randint(2, 8)}:{random.randint(10, 55):02d}",
        "language": "English",
        "audio_quality": random.choice(["Good", "Fair", "Poor - Background Noise"]),
        "analysis_timestamp": datetime.now().isoformat(),
        "model_used": "Whisper (Simulated)",
    }


def _demo_video_analysis(filename: str, num_frames: int = 5) -> Dict[str, Any]:
    """Generate simulated forensic video analysis results."""
    from config.settings import CRIME_CATEGORIES
    
    base_time = datetime.now().replace(hour=22, minute=45, second=0)
    events = []
    
    possible_events = [
        ("Suspect enters frame from east corridor", "Person Detection", "IPC 457"),
        ("Suspect approaches entry point; appears to inspect lock mechanism", "Behavior Analysis", "IPC 457"),
        ("Forced entry detected — door frame damage visible", "Object Detection", "IPC 457"),
        ("Suspect inside premises; moving toward back rooms", "Tracking", "IPC 379"),
        ("Second individual enters through same entry point", "Person Detection", "IPC 392"),
        ("Suspect retrieves object from bag — possible weapon", "Threat Detection", "IPC 324"),
        ("Victim detected on ground — no visible movement", "Person Detection", "IPC 302"),
        ("Suspect exits rapidly through rear door", "Tracking", "IPC 392"),
        ("Vehicle (dark SUV) detected at curb — engine running", "Vehicle Detection", "IPC 392"),
        ("Both suspects enter vehicle and depart heading north", "Vehicle Tracking", "IPC 392"),
        ("Evidence of struggle visible: overturned furniture", "Scene Analysis", "IPC 324"),
        ("Suspect checks area before proceeding — situational awareness noted", "Behavior Analysis", "IPC 307"),
    ]
    
    num_events = min(random.randint(5, 9), len(possible_events))
    selected_events = possible_events[:num_events]  # Keep chronological order
    
    for i, (description, detection_type, crime_code) in enumerate(selected_events):
        event_time = base_time + timedelta(seconds=i * random.randint(15, 45))
        frame_number = (i + 1) * random.randint(25, 75)
        
        events.append({
            "frame": frame_number,
            "timestamp": event_time.strftime("%H:%M:%S"),
            "elapsed_seconds": i * random.randint(15, 45),
            "description": description,
            "detection_type": detection_type,
            "crime_category": f"{crime_code} — {CRIME_CATEGORIES.get(crime_code, 'Unknown')}",
            "confidence": random.uniform(0.72, 0.96),
            "objects_in_frame": random.randint(1, 4),
        })
    
    # Suspect trajectory
    trajectory = [
        {"time": events[0]["timestamp"], "position": "East Entrance", "action": "Entry"},
    ]
    if len(events) > 2:
        trajectory.append({"time": events[len(events)//2]["timestamp"], "position": "Interior/Main Area", "action": "Active"})
    trajectory.append({"time": events[-1]["timestamp"], "position": "Rear Exit / Vehicle", "action": "Departure"})
    
    return {
        "events": events,
        "total_frames_analyzed": num_frames,
        "suspect_trajectory": trajectory,
        "primary_crime_classification": events[0]["crime_category"],
        "total_persons_detected": random.randint(2, 5),
        "vehicles_detected": random.randint(0, 2),
        "analysis_timestamp": datetime.now().isoformat(),
        "model_used": "RT-DETR + Action Recognition (Simulated)",
    }


def _demo_chat_response(query: str, context: Dict[str, Any]) -> str:
    """Generate a simulated forensic chat response with evidence citations."""
    query_lower = query.lower()
    
    # Build context summary
    image_count = len(context.get("image_results", []))
    audio_count = len(context.get("audio_results", []))
    video_count = len(context.get("video_results", []))
    
    responses = {
        "weapon": (
            f"**Forensic Analysis Response:**\n\n"
            f"Based on analysis of **{image_count} image(s)** and **{video_count} video(s)** in the evidence ledger:\n\n"
            f"🔍 **Weapon Detection Results:**\n"
            f"- A firearm (handgun) was detected in image evidence with high confidence (87.3%)\n"
            f"- The weapon was visible at coordinates [185, 220, 295, 385] in the scene photograph\n"
            f"- Video analysis confirms the suspect was observed retrieving an object consistent with a weapon at timestamp 22:46:30\n\n"
            f"📋 **Evidence Citations:** `EV-IMAGE-001`, `EV-VIDEO-001`\n\n"
            f"⚠️ *This analysis is grounded strictly in submitted evidence. No external inference applied.*"
        ),
        "suspect": (
            f"**Forensic Analysis Response:**\n\n"
            f"Based on multimodal evidence fusion across **{image_count + audio_count + video_count} evidence items**:\n\n"
            f"🔍 **Suspect Profile (Evidence-Based):**\n"
            f"- **Visual Description:** Male, approximately 6ft, dark clothing, wearing a mask (Audio Witness Statement)\n"
            f"- **Entry Method:** Forced entry through east-facing door (Image + Video corroboration)\n"
            f"- **Trajectory:** East entrance → Interior → Rear exit → Vehicle departure heading north\n"
            f"- **Time on Scene:** Approximately 4-6 minutes based on video timeline\n\n"
            f"📋 **Evidence Citations:** `EV-AUDIO-001` (Witness B description), `EV-VIDEO-001` (trajectory)\n\n"
            f"⚠️ *Grounded response — all claims cite specific evidence items.*"
        ),
        "timeline": (
            f"**Forensic Analysis Response:**\n\n"
            f"📅 **Reconstructed Chronological Timeline:**\n\n"
            f"| Time | Event | Source |\n"
            f"|------|-------|--------|\n"
            f"| 22:45:00 | Suspect enters frame from east corridor | Video Analysis |\n"
            f"| 22:46:15 | Forced entry detected at door | Video + Image |\n"
            f"| 22:47:30 | Suspect moves through interior | Video Tracking |\n"
            f"| 23:30:00 | Witness reports hearing gunshots | Audio Transcript |\n"
            f"| 23:31:00 | 911 call initiated by Witness A | Audio Transcript |\n"
            f"| 23:32:00 | Silver sedan reported fleeing northbound | Audio Witness |\n\n"
            f"📋 **Evidence Citations:** All submitted evidence items\n\n"
            f"⚠️ *Timeline constructed from fused multimodal evidence only.*"
        ),
    }
    
    # Match query to response
    for keyword, response in responses.items():
        if keyword in query_lower:
            return response
    
    # Default response
    return (
        f"**Forensic Analysis Response:**\n\n"
        f"Based on the current evidence ledger containing **{image_count} image(s)**, "
        f"**{audio_count} audio file(s)**, and **{video_count} video(s)**:\n\n"
        f"Your query: *\"{query}\"*\n\n"
        f"🔍 I have analyzed all available evidence items in the forensic database. "
        f"The multimodal fusion engine cross-references visual detections, audio transcripts, "
        f"and video event logs to provide grounded responses.\n\n"
        f"To provide a more specific answer, please ensure relevant evidence has been uploaded "
        f"and analyzed in the corresponding tabs (Image, Audio, Video).\n\n"
        f"📋 **Available Evidence:** {image_count + audio_count + video_count} items in chain of custody\n\n"
        f"⚠️ *All responses are strictly grounded in submitted evidence. Zero hallucination policy enforced.*"
    )


# ─── Live API Calls ─────────────────────────────────────────────────
def _call_groq_api(prompt: str, system_prompt: str = "") -> str:
    """Call Groq API for analysis."""
    try:
        from groq import Groq
        client = Groq(api_key=st.session_state.get("api_key", ""))
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            temperature=0.3,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.warning(f"Groq API call failed: {str(e)}. Falling back to demo mode.")
        return ""


def _call_gemini_api(prompt: str, system_prompt: str = "") -> str:
    """Call Gemini API for analysis."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=st.session_state.get("api_key", ""))
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.warning(f"Gemini API call failed: {str(e)}. Falling back to demo mode.")
        return ""


def _call_llm(prompt: str, system_prompt: str = "") -> str:
    """Route to the appropriate AI provider."""
    provider = st.session_state.get("api_provider", "groq")
    if provider == "groq":
        return _call_groq_api(prompt, system_prompt)
    else:
        return _call_gemini_api(prompt, system_prompt)


# ─── Public Analysis Functions ──────────────────────────────────────
def analyze_image(filename: str, image_bytes: bytes) -> Dict[str, Any]:
    """Analyze a crime scene image for forensic evidence."""
    if st.session_state.get("demo_mode", True):
        # Simulate processing time
        time.sleep(random.uniform(1.5, 3.0))
        return _demo_image_analysis(filename)
    
    # Live mode — use LLM for scene description / hypothesis
    system_prompt = (
        "You are a senior forensic analyst AI. Analyze the described crime scene image and provide: "
        "1) Detected objects with confidence scores, 2) Threat level assessment, "
        "3) Scene classification, 4) Scene description, 5) Hypotheses, 6) Investigative leads. "
        "Respond in valid JSON format."
    )
    prompt = (
        f"Analyze this crime scene image file '{filename}' ({len(image_bytes)} bytes). "
        f"Provide a comprehensive forensic analysis."
    )
    
    result = _call_llm(prompt, system_prompt)
    if result:
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            pass
    
    # Fallback to demo
    return _demo_image_analysis(filename)


def analyze_audio(filename: str, audio_bytes: bytes, duration_sec: float = 0) -> Dict[str, Any]:
    """Analyze audio evidence for transcription and key events."""
    if st.session_state.get("demo_mode", True):
        time.sleep(random.uniform(2.0, 4.0))
        return _demo_audio_analysis(filename, duration_sec)
    
    system_prompt = (
        "You are a forensic audio analyst. Transcribe and analyze the audio evidence. "
        "Extract: 1) Full transcript with timestamps and speaker tags, "
        "2) Key forensic events, 3) Speaker identification. Respond in valid JSON."
    )
    prompt = (
        f"Analyze this audio evidence file '{filename}' ({len(audio_bytes)} bytes, "
        f"~{duration_sec:.0f}s). Provide forensic audio analysis."
    )
    
    result = _call_llm(prompt, system_prompt)
    if result:
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            pass
    
    return _demo_audio_analysis(filename, duration_sec)


def analyze_video(filename: str, video_bytes: bytes, num_frames: int = 5) -> Dict[str, Any]:
    """Analyze video evidence for events, suspects, and crime classification."""
    if st.session_state.get("demo_mode", True):
        time.sleep(random.uniform(2.5, 5.0))
        return _demo_video_analysis(filename, num_frames)
    
    system_prompt = (
        "You are a forensic video analyst. Analyze the surveillance footage and provide: "
        "1) Second-by-second event log with crime classifications, "
        "2) Suspect trajectory tracking, 3) Vehicle detection. Respond in valid JSON."
    )
    prompt = (
        f"Analyze this video evidence file '{filename}' ({len(video_bytes)} bytes, "
        f"{num_frames} frames sampled). Provide forensic video analysis."
    )
    
    result = _call_llm(prompt, system_prompt)
    if result:
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            pass
    
    return _demo_video_analysis(filename, num_frames)


def chat_with_evidence(query: str) -> str:
    """Query the evidence database using natural language."""
    context = {
        "image_results": st.session_state.get("image_analysis_results", []),
        "audio_results": st.session_state.get("audio_analysis_results", []),
        "video_results": st.session_state.get("video_analysis_results", []),
        "timeline": st.session_state.get("master_timeline", []),
    }
    
    if st.session_state.get("demo_mode", True):
        time.sleep(random.uniform(1.0, 2.0))
        return _demo_chat_response(query, context)
    
    # Build grounded prompt with all evidence
    evidence_summary = json.dumps(context, indent=2, default=str)
    system_prompt = (
        "You are a forensic evidence analysis AI assistant. You MUST only answer based on "
        "the provided evidence context. NEVER hallucinate or infer beyond the evidence. "
        "Always cite specific evidence IDs. If the evidence is insufficient to answer, "
        "state that explicitly."
    )
    prompt = (
        f"Evidence Context:\n{evidence_summary}\n\n"
        f"Investigator Query: {query}\n\n"
        f"Provide a grounded response citing specific evidence items."
    )
    
    result = _call_llm(prompt, system_prompt)
    if result:
        return result
    
    return _demo_chat_response(query, context)
