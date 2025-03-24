import streamlit as st
import requests
import os
from gtts import gTTS  # Google Text-to-Speech
import re  # For text cleaning


USE_LOCAL_API = True  # 
LOCAL_API_URL = "http://127.0.0.1:8000"
HUGGING_FACE_API_URL = "https://LikhithDiwakar-news-summarization-app.hf.space"

API_URL = LOCAL_API_URL if USE_LOCAL_API else HUGGING_FACE_API_URL

st.title("📰 News Summarization & Sentiment Analysis")

company = st.text_input(" Enter Company Name:")

def clean_text(text):
    """Removes unnecessary symbols before converting to speech."""
    return re.sub(r'[{};=,.]', '', text).strip()

if st.button(" Fetch News & Analyze"):
    try:
        # 🔹 Request news data
        response = requests.get(f"{API_URL}/analyze/{company}", timeout=15)
        response.raise_for_status()  # Raise error if request fails

        if response.status_code == 200:
            data = response.json()
            st.write("##  Sentiment Analysis Report")

            text_for_tts = ""  # Store text for TTS conversion

            for article in data.get("Articles", []):
                title = clean_text(article.get("Title", "No Title"))
                summary = clean_text(article.get("Summary", "No summary available"))
                sentiment = clean_text(article.get("Sentiment", "Unknown"))
                topics = ', '.join(article.get("Topics", ["None"]))

                st.subheader(title)
                st.write(f"** Summary:** {summary}")
                st.write(f"** Sentiment:** {sentiment}")
                st.write(f"** Topics:** {topics}")
                st.write("---")

                # 🔊 Prepare text for speech
                text_for_tts += f"शीर्षक: {title}। सारांश: {summary}। भाव: {sentiment}। विषय: {topics}।\n\n"

            #  Display Comparative Sentiment Analysis
            st.write(" Comparative Sentiment Distribution")
            st.json(data.get("Comparative Sentiment Score", {}))

            #  Generate Hindi Text-to-Speech
            if text_for_tts.strip():
                tts = gTTS(text=text_for_tts, lang="hi")
                tts.save("tts_output.mp3")
                st.audio("tts_output.mp3", format="audio/mp3")
                st.success("✅ Hindi audio generated successfully!")
            else:
                st.warning("No text available for speech synthesis.")

        else:
            st.error("Failed to fetch news. Try again!")

    except requests.exceptions.RequestException as e:
        st.error(f" API Connection Failed: {e}")
