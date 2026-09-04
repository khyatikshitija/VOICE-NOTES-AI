import streamlit as st
from faster_whisper import WhisperModel
from openai import OpenAI
import os
from audio_recorder_streamlit import audio_recorder
if "processed" not in st.session_state:
    st.session_state.processed = False
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0e1117, #1a233a, #0e1117);
        color: #fafafa;
    }
    .stFileUploader {
    background: rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stButton > button {
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    border: 1px solid rgba(255, 255, 255, 0.3);
    background: rgba(255, 255, 255, 0.12);
    transition: 0.3s;
    }

.stButton > button:hover {
    transform: scale(1.02);
    background: rgba(255, 255, 255, 0.2);
    }

.result-card {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 16px;
    padding: 20px;
    margin: 15px 0;
    backdrop-filter: blur(10px);
    }    
    </style>
    """,
    unsafe_allow_html=True
)

#llm optional 
api_key = os.getenv("OPENAI_API_KEY")

if api_key and api_key!="VOICE_NOTES":
    client = OpenAI(api_key=api_key)
else:
    client=None

#building blocks
st.markdown("""
<div style = "font-size:30px;line-height:2.2;text-align:center;font-family:'Trebuchet MS',sans-serif;">
<strong>🎙️ YOUR PERSONAL VOICE ASSISTANT 🎙️</strong>
</div>
""",unsafe_allow_html=True)
st.markdown("""
<div style="font-size:25px;line-height:2.2;text-align:center;font-family:'Georgia';">
<emp>Don't know where to how to organise your clutter thoughts!!!</emp>
</div>""",
unsafe_allow_html=True)
st.markdown(
    "<h3 style = 'text-align:center;'>THEN JUST...</h3>",
    unsafe_allow_html=True
    )
st.markdown("""
<div style = "font-size:22px;line-height:2.2;font-family:'Georgia';">
<div style = "margin-left:10%"><b>UPLOAD</b><i> your voice note,</i></div>
<div style = "margin-left:25%"><b>TRANSCRIBE</b> <i>it instantly,</i></div>
<div style = "margin-left:40%"><b>ORGANISE</b> <i>your thoughts.</i></div>
</div>
""",unsafe_allow_html=True)

st.divider()

st.markdown("### 🎤 Upload your voice note")

audio_file = st.file_uploader(
    "Choose an audio file",
    type=["mp3", "wav", "m4a", "webm"]
)

st.markdown("#### 🎙️ Or Record your voice")

recorded_audio = audio_recorder(
    text="Click to record",
    recording_color="#ff4b4b",
    neutral_color="#6c757d",
    icon_name="microphone",
    icon_size="2x",
)

if recorded_audio:
    audio_file = recorded_audio
    st.session_state.recorded_audio = recorded_audio
elif audio_file:
    st.session_state.audio_file=audio_file
elif "audio_file" in st.session_state:
    audio_file=st.session_state.audio_file
else:
    audio_file=None

    # Play uploaded recording
if audio_file:
    st.subheader("Your Recording")
    st.audio(audio_file)

    if st.button("🎙️ TRANSCRIBE 🎙️", use_container_width=True):
        st.session_state.processed = True
        with st.spinner("Preparing audio..."):

            if hasattr(audio_file,"name"):
                audio_path = "temp_uploaded" + os.path.splitext(audio_file.name)[1]
            else:
                audio_path = "temp_recorded.wav"

            with open(audio_path, "wb") as f:
                if hasattr(audio_file,"getbuffer"):
                    f.write(audio_file.getbuffer())
                else:
                    f.write(audio_file)

            wav_path = "temp_audio.wav"

            result = os.system(
                f'ffmpeg -y -i "{audio_path}" -ar 16000 -ac 1 "{wav_path}"'
            )

            if result != 0 or not os.path.exists(wav_path):
                st.error("Audio conversion failed. Please try another audio file.")
                st.stop()

        with st.spinner("Transcribing..."):

            model = WhisperModel(
                "small",
                device="cpu",
                compute_type="int8"
            )

            segments, info = model.transcribe(
                wav_path,
                beam_size=5,
                vad_filter=True,
                condition_on_previous_text=False
            )

            st.session_state.language=info.language
            st.session_state.language_probability=info.language_probability

            transcript = ""

            for segment in segments:
                transcript += segment.text.strip() + " "

            transcript = transcript.strip()

        st.session_state.transcript = transcript
        if not transcript:
            st.warning("No speech detected. Please upload a clearer voice note.")
            st.stop()
#SUMMARY and ACTION ITEMS...
        if client:
            with st.spinner("Generating summary and action items..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a voice notes assistant. "
                                "Analyze the user's transcript and provide a concise, useful response.\n\n"
                                "Format your response exactly as:\n"
                                "SUMMARY:\n"
                                "Write a 1-3 sentence summary.\n\n"
                                "ACTION ITEMS:\n"
                                "- List each clear task as a separate bullet point.\n"
                                "Do not invent tasks that are not present in the transcript."
                            )
                        },                 
                        {
                            "role":"user",
                            "content":transcript
                        }
                    ]
                )

                ai_output=response.choices[0].message.content
                st.session_state.ai_output=ai_output
            st.subheader("AI Summary and Action items")
            st.write(ai_output)
        else:
            sentences = [
                s.strip()
                for s in transcript.replace("|",".").split(".")
                if s.strip()
            ]
            if len(sentences)<=2:
                summary =" ".join(sentences)
            else:
                summary=" ".join(sentences[:2])

            if summary and not summary.endswith("."):
                summary+="."

            st.session_state.summary = summary

            action_keywords = [
                "need to",
                "have to",
                "should",
                "must",
                "todo",
                "to do",
                "need",
                "plan to",
                "remember to",
                "learning outcome",
                "think",
                "better",
                "solve",
                "help",
                "karna hai",
                "karna hoga",
                "karo",
                "karna",
                "krna hai",
                "krna hoga",
                "padho",
                "socho",
                "suno",
                "prayas",
                "prayaash",
                "करना है",
                "करना होगा",
                "करो",
                "पढ़ो",
                "पढ़ना है",
                "पढ़ना होगा",
                "पूरा करना है",
                "पूरा करना होगा",
                "करनी है",
                "करना चाहिए"
            ]

            action_items = []

            for sentence in sentences:
                sentence_clean = sentence.strip()

                if any(
                    keyword in sentence_clean.lower()
                    for keyword in action_keywords
                    ):
                        action_items.append(sentence_clean)
            st.session_state.action_items = action_items


if  st.session_state.get("processed",False):

    if "language" in st.session_state:
        st.info(
            f"Detected language:{st.session_state.language}"
            f"({st.session_state.language_probability:.0%}confidence)"
        )

    if "transcript" in st.session_state:
        st.markdown(f"""
        <div class ="result-card">
        <h3>Transcript</h3>
        <p>{st.session_state.transcript}</p>
        </div>
        """,
        unsafe_allow_html=True)
        
    if "ai_output" in st.session_state:
        st.subheader("🤖 AI Summary & Action Items")
        st.write(st.session_state.ai_output)

    elif "summary" in st.session_state:
        st.markdown(f"""
        <div class="result-card">
        <h3>📝 Summary</h3>
        <p>{st.session_state.summary}</p>
        </div>""",
        unsafe_allow_html=True)
    if "action_items" in st.session_state:
        st.markdown("""
        <h3>✅ Action Items</h3>
        """,
        unsafe_allow_html=True)

    if st.session_state.get("action_items",[]):
        for item in st.session_state.action_items:
            st.checkbox(item, key=f"action_{item}")
    else:
        st.write("No action item detected.")
    
    st.divider()

    if st.button("↻ New Note", use_container_width=True):
        st.session_state.clear()
        st.rerun()
