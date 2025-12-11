"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: December 2025
Description: Final Version - Green Color Fixed, Firebase DB Integrated, Auto-Model.
"""

import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import time

#  Firebase Library
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. SETUP PAGE CONFIGURATION ---
def setup_page_config():
    st.set_page_config(
        page_title="Noor-AI Pro",
        page_icon="🌙",
        layout="centered"
    )

# --- 2. APPLY STRONG CSS (CONTAINER FIX FOR GREEN COLOR) ---
def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main Background */
        .stApp { background-color: #121212; color: #FFFFFF; }
        
        /* Headers */
        h1, h2, h3 { color: #E0E0E0 !important; font-family: 'Helvetica Neue', sans-serif; text-align: center; font-weight: 300; }
        .stMarkdown h3 { color: #FDD835 !important; text-align: center; }
        
        /* Sidebar */
        [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #333; }
        
        /* Input Box */
        .stTextInput input { background-color: #333333 !important; color: white !important; border: 1px solid #555; border-radius: 20px; }
        
        /* --- CHAT MESSAGE STYLING (The Fix) --- */
        /* We target the specific container structure to ensure Odd/Even works */
        
        /* User (Odd) -> Grey */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stChatMessage"]:nth-of-type(odd) {
            background-color: #262626 !important; 
            border: 1px solid #444 !important; 
            border-radius: 12px; 
            padding: 15px;
        }

        /* AI (Even) -> Deep Green */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stChatMessage"]:nth-of-type(even) {
            background-color: #0d3b1e !important; 
            border: 1px solid #1e5c30 !important; 
            border-radius: 12px; 
            padding: 15px;
        }
        
        /* Text Color -> White */
        [data-testid="stChatMessage"]:nth-of-type(even) * { color: #e8f5e9 !important; }

        /* Keywords -> Gold */
        [data-testid="stChatMessage"]:nth-of-type(even) strong { color: #FFD700 !important; font-weight: bold !important; }

        /* Links -> Blue */
        [data-testid="stChatMessage"]:nth-of-type(even) a { color: #4fc3f7 !important; text-decoration: underline !important; font-weight: bold; }
        
        /* Mobile Table Fix */
        .stMarkdown table { display: block; overflow-x: auto; white-space: nowrap; width: 100%; }
        </style>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURE API (GEMINI & FIREBASE) ---
def configure_api():
    # A. Gemini Setup
    local_key = "YOUR_API_KEY_HERE"
    try:
        if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
        else:
            raise FileNotFoundError 
    except:
        api_key = local_key
    genai.configure(api_key=api_key)

    # B. Firebase Setup
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(dict(st.secrets["firebase"]))
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"⚠️ Firebase skipped (Check Secrets): {e}")
        return None

# (Global Variable)
db = configure_api()

# --- 4. SAVE TO DB FUNCTION ---
def save_chat_to_db(user_msg, ai_msg):
    if db:
        try:
            db.collection("chats").add({
                "user": user_msg,
                "ai": ai_msg,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            print("✅ Saved to Firebase")
        except Exception as e:
            print(f"❌ DB Save Error: {e}")

# --- 5. AUTO MODEL DETECTION ---
def get_working_model():
    print("System: Checking models...", end="\r")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if "flash" in m.name or "pro" in m.name:
                    return m.name
        # Fallback loop
        for m in genai.list_models():
             if 'generateContent' in m.supported_generation_methods:
                 return m.name
    except:
        return None
    return "models/gemini-1.5-flash"

# --- 6. SYSTEM INSTRUCTION ---
system_instruction = """
You are Noor-AI, a caring and knowledgeable Islamic companion.

*** IMPORTANT PROTOCOLS ***
1. **THEOLOGICAL SAFETY (AQEEDAH):**
   - **Creator:** ONLY Allah is the Creator. NEVER attribute this title to a human.
   - **Developer:** If asked who made you, reply: "I was developed/programmed by **Kazi Abdul Halim Sunny**."

2. **ACCURACY & CLICKABLE LINKS (MANDATORY):**
   - **Quran:** Quote as **[Surah Name: Ayah](https://quran.com/SURAH_NUMBER/AYAH_NUMBER)**.
   - **Hadith:** Provide Book Name, Hadith Number, and Status.

3. **STRICT LANGUAGE MATCHING:**
   - English Q -> English Ans.
   - Bangla Q -> Bangla Ans.

4. **IDENTITY & BIO:**
   - **Developer:** Kazi Abdul Halim Sunny (Student of Software Engineering, Metropolitan University).
   - **Author:** "আজ কেন নয়?", "একটুকরো স্বপ্ন", "অমানিশা", "প্রিটেন্ড".

5. **SOURCE TRUTH:**
   - NEVER give your own Fatwa. Always quote Quran & Sahih Hadith.

6. **SCHOLAR PREFERENCE:**
   - Prioritize **Ustaz Abu Sa'ada Muhammad Hammad Billaah** & **Esho Din Shikhi**.
   - Use **Bold** for key Islamic terms (e.g., **Tawhid**, **Jannah**) so they appear Gold.
"""

# --- 7. INITIALIZE SESSION ---
def initialize_session():
    if "history" not in st.session_state:
        st.session_state.history = []
        
    try:
        # Auto Detect Model Only Once
        if "model" not in st.session_state:
            detected_model_name = get_working_model()
            st.session_state.current_model_name = detected_model_name 
            
            st.session_state.model = genai.GenerativeModel(
                model_name=detected_model_name, 
                system_instruction=system_instruction
            )
            st.session_state.chat = st.session_state.model.start_chat(history=[])
    except Exception as e:
        st.error(f"Failed to initialize AI model: {e}")

# --- 8. DISPLAY SIDEBAR ---
def display_sidebar():
    with st.sidebar:
        st.title("🌙 Noor-AI")
        st.markdown("**Developer:**\n### Kazi Abdul Halim Sunny")
        st.info("Guidance based on Qur'an & Authentic Sunnah.")
        
        if st.session_state.history:
            chat_str = "--- Chat History ---\n\n"
            for msg in st.session_state.history:
                chat_str += f"{msg['role']}: {msg['content']}\n"
            st.download_button("📥 Download Chat", chat_str, "chat.txt")
        
        st.markdown("---")
        # Status Indicators
        if db:
            st.caption("🟢 Database: `Connected`")
        else:
            st.caption("🔴 Database: `Disconnected`")
            
        if "current_model_name" in st.session_state:
            st.caption(f"🟢 AI Model: `{st.session_state.current_model_name}`")

# --- 9. MAIN APP ---
def main():
    setup_page_config()
    apply_custom_styles()
    # configure_api is called globally for DB
    initialize_session()
    display_sidebar()

    st.title("Noor-AI Assistant") 
    st.markdown("### Guidance from Qur'an & Sunnah")
    st.divider()

    # CONTAINER ISOLATION (Critical for Green Color)
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.history:
            role = message["role"]
            avatar = "👤" if role == "user" else "🎓"
            with st.chat_message(role, avatar=avatar):
                st.markdown(message["content"])

    prompt = st.chat_input("Ask a question about Islam...")

    if prompt:
        # 1. Add User Message
        st.session_state.history.append({"role": "user", "content": prompt})
        
        # 2. Display and Process inside Container
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="🎓"):
                placeholder = st.empty()
                placeholder.markdown("...") 
                
                try:
                    if hasattr(st.session_state, 'chat'):
                        response = st.session_state.chat.send_message(prompt)
                        placeholder.markdown(response.text)
                        
                        # 3. Add AI Message to History
                        st.session_state.history.append({"role": "assistant", "content": response.text})
                        
                        # 4. Save to Firebase
                        save_chat_to_db(prompt, response.text)
                        
                except Exception as e:
                    placeholder.error(f"Error: {e}")

if __name__ == "__main__":
    main()
