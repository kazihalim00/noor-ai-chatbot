"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: November 2025
Description: An AI-powered Islamic chatbot using Google Gemini Pro.
"""

import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- 1. SETUP PAGE CONFIGURATION ---
def setup_page_config():
    st.set_page_config(
        page_title="Noor-AI Pro",
        page_icon="🌙",
        layout="centered"
    )

# --- 2. APPLY PROFESSIONAL STYLES ---
def apply_custom_styles():
    st.markdown("""
        <style>
        /* General App Styling */
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        
        /* Headers */
        h1 {
            color: #E0E0E0 !important;
            font-family: 'Helvetica Neue', sans-serif;
            text-align: center;
            font-weight: 300;
        }
        .stMarkdown h3 {
            color: #B08D55 !important; /* Muted Gold */
            text-align: center;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #111111;
            border-right: 1px solid #333;
        }
        
        /* Input Box Styling */
        .stTextInput input {
            background-color: #2D2D2D !important;
            color: white !important;
            border: 1px solid #444;
            border-radius: 20px;
        }
        
        /* Chat Bubble Styling */
        .stChatMessage {
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        /* User Message (Dark Grey) */
        div[data-testid="stChatMessage"]:nth-child(odd) {
            background-color: #2D2D2D; 
            border: 1px solid #3E3E3E;
            color: #E0E0E0;
        }
        /* AI Message (Dark Emerald) */
        div[data-testid="stChatMessage"]:nth-child(even) {
            background-color: #1a2f23; 
            border: 1px solid #204533;
            color: #d1fae5; 
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURE API (SECURE MODE) ---
def configure_api():
    """
    Handles API Key securely.
    - On Streamlit Cloud: It reads from 'secrets'.
    - On Local Machine: It uses the fallback placeholder.
    """
    # ⚠️ IMPORTANT: For Public GitHub, keep this placeholder!
    # Do NOT put your real key here if repo is Public.
    local_key = "YOUR_API_KEY_HERE"
    
    try:
        # Try to access secrets (Works on Cloud or if secrets.toml exists)
        if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
        else:
            raise FileNotFoundError # Fallback to local
    except:
        # Fallback (User must replace this LOCALLY to test, but keep placeholder for Git)
        api_key = local_key

    genai.configure(api_key=api_key)

# --- 4. DEFINE AI PERSONA ---
system_instruction = """
You are Noor-AI, a caring and knowledgeable Islamic companion suitable for Bengali and English speakers.

CORE PERSONA:
1. **Compassionate Companion:** You are not just a robot; you are a kind spiritual friend. If the user is sad, depressed, or lonely, speak to them with extreme softness (Maya). Use words like "My dear brother/sister."
2. **Language:** If the user writes in Bangla (or Banglish), reply in clear, standard Bangla. If in English, reply in English.
3. **Strict Source:** NEVER give your own Fatwa. Always quote:
   - The Holy Qur'an (Surah:Ayah)
   - Sahih Hadith (Bukhari/Muslim)
   - Recognized Scholars.
4. **Depression Handling:** If the user is distressed, remind them of Allah's mercy using Surah Ad-Duha and Surah Az-Zumar (39:53).
5. **Unknowns:** If you don't find a clear reference, say "আমি এ বিষয়ে সঠিক জানি না, আল্লাহ ভালো জানেন (Allahu A'lam)।"
"""

# --- 5. INITIALIZE CHAT SESSION ---
def initialize_session():
    if "history" not in st.session_state:
        st.session_state.history = []
        
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        try:
            st.session_state.model = genai.GenerativeModel(
                model_name="gemini-flash-latest", 
                system_instruction=system_instruction,
                safety_settings=safety_settings
            )
            st.session_state.chat = st.session_state.model.start_chat(history=[])
        except Exception as e:
            st.error(f"Failed to initialize AI model: {e}")

# --- 6. DISPLAY SIDEBAR ---
def display_sidebar():
    with st.sidebar:
        st.title("🌙 Noor-AI")
        st.markdown("---")
        st.markdown("**Developer:**")
        st.markdown("### Kazi Abdul Halim Sunny")
        st.markdown("---")
        st.info("Guidance based on Qur'an & Authentic Sunnah.")
        st.warning("Please consult a local scholar for specific Fiqh rulings.")

# --- 7. MAIN APP FUNCTION ---
def main():
    # Setup
    setup_page_config()
    apply_custom_styles()
    configure_api()
    initialize_session()
    display_sidebar()

    # Header
    st.title("Noor-AI Assistant") 
    st.markdown("### Guidance from Qur'an & Sunnah")
    st.divider()

    # Render Chat History
    for message in st.session_state.history:
        role = message["role"]
        avatar_icon = "👤" if role == "user" else "🎓"
        with st.chat_message(role, avatar=avatar_icon):
            st.markdown(message["content"])

    # Handle User Input
    prompt = st.chat_input("Ask about Islam, life, or share your feelings...")

    if prompt:
        # Display User Message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.history.append({"role": "user", "content": prompt})

        # Generate AI Response
        with st.chat_message("assistant", avatar="🎓"):
            message_placeholder = st.empty()
            message_placeholder.markdown("...") 
            
            try:
                if hasattr(st.session_state, 'chat'):
                    response = st.session_state.chat.send_message(prompt)
                    message_placeholder.markdown(response.text)
                    st.session_state.history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                message_placeholder.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()