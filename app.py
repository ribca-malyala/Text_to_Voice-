"""
Text to Voice (Text-to-Speech) App
Converts text into natural speech in many languages (incl. Indian
languages) using Google Text-to-Speech (gTTS). Needs internet,
but NO API key.
"""
from io import BytesIO

import streamlit as st
from gtts import gTTS

st.set_page_config(page_title="Text to Voice", page_icon="🔊", layout="centered")

# ---------------- INTERNAL CSS ----------------
st.markdown("""
<style>

/* ===== Main Background ===== */
.stApp {
    background: linear-gradient(
        135deg,
        #fff7fb 0%,
        #fff1f8 45%,
        #f8f1ff 100%
    );
}

/* ===== Main Container ===== */
.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ===== Main Title ===== */
h1 {
    text-align: center;
    color: #c05a91 !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

/* ===== Main Description ===== */
.stApp p {
    color: #6d5969;
}

/* ===== Sidebar ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #fff0f7 0%,
        #f8efff 100%
    );
    border-right: 1px solid #efd5e4;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #b85b8d !important;
}

/* ===== Text Area ===== */
.stTextArea textarea {
    background-color: #fffafd !important;
    color: #594b57 !important;
    border: 2px solid #edcadd !important;
    border-radius: 20px !important;
    padding: 15px !important;
    font-size: 16px !important;
    box-shadow: 0 5px 20px rgba(190, 100, 150, 0.08);
}

/* Text Area Focus */
.stTextArea textarea:focus {
    border-color: #d78ab0 !important;
    box-shadow: 0 0 0 3px rgba(215, 138, 176, 0.15) !important;
}

/* ===== Select Boxes ===== */
[data-baseweb="select"] > div {
    background-color: #fffafd !important;
    border: 1.5px solid #e6c6d8 !important;
    border-radius: 14px !important;
}

/* ===== Radio Buttons ===== */
[data-testid="stRadio"] label {
    color: #6a5665 !important;
}

/* ===== Checkbox ===== */
[data-testid="stCheckbox"] label {
    color: #6a5665 !important;
}

/* ===== Main Button ===== */
.stButton > button {
    width: 100%;
    border: none !important;
    border-radius: 20px !important;
    background: linear-gradient(
        135deg,
        #d982ad,
        #b995d1
    ) !important;
    color: white !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    padding: 0.75rem 1rem !important;
    box-shadow: 0 7px 20px rgba(188, 105, 151, 0.22);
    transition: all 0.25s ease;
}

/* Button Hover */
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(188, 105, 151, 0.30);
}

/* ===== Download Button ===== */
.stDownloadButton > button {
    width: 100%;
    border-radius: 18px !important;
    border: 2px solid #e1b7cf !important;
    background-color: #fff8fc !important;
    color: #ae5684 !important;
    font-weight: 700 !important;
    transition: all 0.25s ease;
}

/* Download Hover */
.stDownloadButton > button:hover {
    background-color: #fce9f3 !important;
    border-color: #d78bb0 !important;
    transform: translateY(-1px);
}

/* ===== File Uploader ===== */
[data-testid="stFileUploader"] {
    background-color: rgba(255, 248, 252, 0.85);
    border: 2px dashed #ddb2ca;
    border-radius: 20px;
    padding: 12px;
}

/* ===== Audio Player ===== */
audio {
    width: 100%;
    border-radius: 15px;
}

/* ===== Success / Warning / Error Boxes ===== */
[data-testid="stAlert"] {
    border-radius: 16px !important;
}

/* ===== Caption ===== */
.stCaption {
    color: #9a7f91 !important;
    font-size: 13px;
}

/* ===== Spinner ===== */
[data-testid="stSpinner"] {
    color: #b85b8d !important;
}

/* ===== Hide Streamlit Branding ===== */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


LANGUAGES = {
    "English": "en", "Hindi": "hi", "Telugu": "te", "Tamil": "ta",
    "Bengali": "bn", "Marathi": "mr", "Kannada": "kn", "Malayalam": "ml",
    "Gujarati": "gu", "Urdu": "ur", "French": "fr", "Spanish": "es",
    "German": "de", "Japanese": "ja",
}

ACCENTS = {  # Only applies to English
    "Indian": "co.in",
    "American": "com",
    "British": "co.uk",
    "Australian": "com.au",
}

SAMPLES = {
    "English": "Hello! Welcome to my text to speech project. Have a great day.",
    "Hindi": "नमस्ते! मेरे टेक्स्ट टू स्पीच प्रोजेक्ट में आपका स्वागत है।",
    "Telugu": "నమస్కారం! నా టెక్స్ట్ టు స్పీచ్ ప్రాజెక్ట్‌కు స్వాగతం.",
}


def synthesize(text: str, lang: str, tld: str, slow: bool) -> bytes:
    buf = BytesIO()
    gTTS(text=text, lang=lang, tld=tld, slow=slow).write_to_fp(buf)
    return buf.getvalue()


# ---------------- Sidebar ----------------
st.sidebar.header("Settings")
lang_name = st.sidebar.selectbox("Language", list(LANGUAGES.keys()))
accent = "Indian"
if lang_name == "English":
    accent = st.sidebar.selectbox("Accent", list(ACCENTS.keys()))
slow = st.sidebar.checkbox("Slow speech")
st.sidebar.caption("Tip: type the text in the same language you select.")

# ---------------- Main ----------------
st.title("🔊 Text to Voice")
st.write("Type or upload text and convert it to speech you can play and download.")

source = st.radio("Input type", ["Type text", "Upload .txt"], horizontal=True)
if source == "Type text":
    text = st.text_area(
        "Your text", value=SAMPLES.get(lang_name, ""), height=200, max_chars=5000
    )
else:
    file = st.file_uploader("Upload a .txt file", type=["txt"])
    text = file.read().decode("utf-8", errors="ignore") if file else ""
    if text:
        st.text_area("File content", text, height=200, disabled=True)

st.caption(f"{len(text)} characters")

if st.button("🔊 Convert to speech", type="primary"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Generating audio..."):
            try:
                audio = synthesize(text, LANGUAGES[lang_name], ACCENTS[accent], slow)
            except Exception as e:
                st.error(f"Failed: {e}. Check your internet connection.")
                st.stop()
        st.success("Done!")
        st.audio(audio, format="audio/mp3")
        st.download_button("⬇️ Download MP3", audio, "speech.mp3", "audio/mpeg")