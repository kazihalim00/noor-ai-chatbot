"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Description: Restored Original Styling with Firebase & Auto-Model Logic.
"""

import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. SETUP PAGE CONFIGURATION ---
def setup_page_config():
    st.set_page_config(
        page_title="Noor-AI Pro",
        page_icon="🌙",
        layout="centered"
    )

#--- 2. APPLY YOUR ORIGINAL STYLES (Improved for Reliability) ---
def apply_custom_styles():
    st.markdown("""
        <style>
        /* General App Styling */
        .stApp { background-color: #121212; color: #FFFFFF; }
        
        /* Headers */
        h1, h2, h3 { color: #E0E0E0 !important; font-family: 'Helvetica Neue', sans-serif; text-align: center; }
        .stMarkdown h3 { color: #FDD835 !important; text-align: center; }
        
        /* Sidebar */
        [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #333; }
        .stTextInput input { background-color: #333333 !important; color: white !important; border: 1px solid #555; border-radius: 20px; }
        
        /* --- CHAT BUBBLES (Your Preferred Style) --- */
        
        /* User Message (ODD) -> Grey */
        div[data-testid="stChatMessage"]:nth-of-type(odd) {
            background-color: #262626 !important;
            border: 1px solid #444 !important;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
        }

        /* AI Message (EVEN) -> Deep Green */
        div[data-testid="stChatMessage"]:nth-of-type(even) {
            background-color: #0d3b1e !important;
            border: 1px solid #1e5c30 !important;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        /* AI Text Color */
        div[data-testid="stChatMessage"]:nth-of-type(even) * { color: #e8f5e9 !important; }
        
        /* Gold Keywords */
        div[data-testid="stChatMessage"]:nth-of-type(even) strong { color: #FFD700 !important; font-weight: bold !important; }
        
        /* Links */
        div[data-testid="stChatMessage"]:nth-of-type(even) a { color: #4fc3f7 !important; text-decoration: underline !important; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURE API (GEMINI & FIREBASE) ---
def configure_api():
    # A. Gemini
    local_key = "YOUR_API_KEY_HERE"
    try:
        if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
        else:
            raise FileNotFoundError 
    except:
        api_key = local_key
    genai.configure(api_key=api_key)

    # B. Firebase
    try:
        # Check if already initialized to prevent errors
        if not firebase_admin._apps:
            # Load from secrets
            if "firebase" in st.secrets:
                cred = credentials.Certificate(dict(st.secrets["firebase"]))
                firebase_admin.initialize_app(cred)
            else:
                print("⚠️ Firebase secrets not found.")
                return None
        return firestore.client()
    except Exception as e:
        # This will show the exact error in logs
        print(f"⚠️ Firebase Init Error: {e}")
        return None

# Connect DB globally
db = configure_api()

# --- 4. AUTO MODEL LOGIC ---
def get_working_model():
    print("Checking models...", end="\r")
    try:
        # Check for flash or pro
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name or "pro" in m.name:
                    return m.name
        # Fallback
        for m in genai.list_models():
             if 'generateContent' in m.supported_generation_methods:
                 return m.name
    except:
        return "models/gemini-1.5-flash"
    return "models/gemini-1.5-flash"

# --- 5. SYSTEM INSTRUCTION ---
system_instruction = """
You are Noor-AI, a caring and knowledgeable Islamic companion. *** IMPORTANT PROTOCOLS *** 
1. **THEOLOGICAL SAFETY (AQEEDAH):** - **Creator:** ONLY Allah is the Creator. NEVER attribute this title to a human. - **Developer:** If asked who made you, reply: "I was developed/programmed by **Kazi Abdul Halim Sunny**." 
2. **ACCURACY & CLICKABLE LINKS (MANDATORY):** - **Quran:** Quote as **[Surah Name: Ayah](https://quran.com/SURAH_NUMBER/AYAH_NUMBER)**. - **Hadith:** Provide Book Name, Hadith Number, and Status. 
3. **STRICT LANGUAGE MATCHING:** - English Q -> English Ans. - Bangla Q -> Bangla Ans. 
4. **IDENTITY & BIO:** - **Developer:** Kazi Abdul Halim Sunny (Student of Software Engineering, Metropolitan University). - **Author:** "আজ কেন নয়?", "একটুকরো স্বপ্ন", "অমানিশা", "প্রিটেন্ড". 
5. **SOURCE TRUTH:** - NEVER give your own Fatwa. Always quote Quran & Sahih Hadith. 
6. **SCHOLAR PREFERENCE:** - Prioritize **Ustaz Abu Sa'ada Muhammad Hammad Billaah** & **Esho Din Shikhi**. - Use **Bold** for key Islamic terms (e.g., **Tawhid**, **Jannah**) so they appear Gold. """

# --- 6. INITIALIZE SESSION ---
def initialize_session():
    if "history" not in st.session_state:
        st.session_state.history = []
        
    if "model" not in st.session_state:
        try:
            detected_model_name = get_working_model()
            st.session_state.current_model_name = detected_model_name 
            
            st.session_state.model = genai.GenerativeModel(
                model_name=detected_model_name, 
                system_instruction=system_instruction
            )
            st.session_state.chat = st.session_state.model.start_chat(history=[])
        except Exception as e:
            st.error(f"Model Error: {e}")

# --- 7. SAVE TO DB ---
def save_chat_to_db(user_msg, ai_msg):
    if db:
        try:
            db.collection("chats").add({
                "user": user_msg,
                "ai": ai_msg,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
        except Exception as e:
            print(f"DB Save Error: {e}")

# --- 8. SIDEBAR ---
def display_sidebar():
    with st.sidebar:
        st.title("🌙 Noor-AI")
        st.markdown("**Developer:**\n### Kazi Abdul Halim Sunny")
        st.info("Guidance based on Qur'an & Authentic Sunnah.")
        
        if st.session_state.history:
            chat_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.history])
            st.download_button("📥 Download Chat", chat_str, "chat.txt")
        
        st.markdown("---")
        
        # Database Status Indicator (Debugging)
        if db:
            st.caption("🟢 Database: `Connected`")
        else:
            st.caption("🔴 Database: `Disconnected`")
            # If disconnected, show why (Helpful for you)
            if "firebase" not in st.secrets:
                st.error("Missing [firebase] in secrets.")

        # Model Info (Bottom)
        if "current_model_name" in st.session_state:
            st.caption(f"🟢 Mode: `{st.session_state.current_model_name}`")

# --- 9. MAIN APP ---
def main():
    setup_page_config()
    apply_custom_styles()
    # initialize_session calls get_working_model internally
    initialize_session()
    display_sidebar()

    st.title("Noor-AI Assistant") 
    st.markdown("### Guidance from Qur'an & Sunnah")
    st.divider()

    # --- DISPLAY CHAT (OLD STYLE LOOP) ---
    for message in st.session_state.history:
        role = message["role"]
        avatar = "👤" if role == "user" else "🎓"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask about Islam...")

    if prompt:
        # 1. User Logic
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # 2. AI Logic
        with st.chat_message("assistant", avatar="🎓"):
            placeholder = st.empty()
            placeholder.markdown("...") 
            
            try:
                if hasattr(st.session_state, 'chat'):
                    response = st.session_state.chat.send_message(prompt)
                    placeholder.markdown(response.text)
                    
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                    
                    # 3. Save to Firebase
                    save_chat_to_db(prompt, response.text)
            except Exception as e:
                placeholder.error(f"Error: {e}")

if __name__ == "__main__":
    main()
