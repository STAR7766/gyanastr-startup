import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import json
import re

# Page Config
st.set_page_config(page_title="GyanAstr.ai", page_icon="🚀", layout="wide")

# --- API SETUP (CLOUD COMPATIBLE) ---
# Ye line check karegi ki code computer pe hai ya cloud pe
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ API Key not found! Please set it in Streamlit Secrets.")
    st.stop()

# --- FUNCTIONS ---
def get_gemini_response(prompt, content):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # Flash is faster for demos
        response = model.generate_content(prompt + "\n\nContent:\n" + content)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def get_youtube_transcript(url):
    try:
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([i['text'] for i in transcript]), None
        return None, "Invalid URL"
    except:
        return None, "No Captions Found"

# --- UI ---
st.title("🚀 GyanAstr.ai: The Startup Edition")
st.markdown("### Powered by Google Gemini 1.5 & Streamlit")

# Input
input_type = st.radio("Select Input:", ["YouTube Link", "Text Paste"])
content = ""

if input_type == "YouTube Link":
    url = st.text_input("YouTube URL:")
    if url and st.button("Get Transcript"):
        with st.spinner("Fetching..."):
            text, err = get_youtube_transcript(url)
            if err: st.error(err)
            else: 
                st.session_state['content'] = text
                st.success("Video Loaded!")
elif input_type == "Text Paste":
    txt = st.text_area("Paste Text Here:")
    if st.button("Load Text"):
        st.session_state['content'] = txt
        st.success("Text Loaded!")

# Analysis
if st.button("Generate Analysis") and 'content' in st.session_state:
    prompt = """
    You are GyanAstr. Analyze the content and give 3 sections:
    1. Summary (Bullet points)
    2. Mindmap Code (Strictly inside ```mermaid``` block)
    3. Quiz (Strictly inside ```json``` block like [{"question":"Q","answer":"A"}])
    """
    with st.spinner("AI Working..."):
        res = get_gemini_response(prompt, st.session_state['content'])
        st.markdown(res) # Direct output for safety
