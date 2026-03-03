"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: November 2025
Update: December 12, 2025
Description: PROFESSIONAL VERSION - Gemini 2.5 Flash + Green/Gold Theme + Fixed Salam Color.
"""

import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import firebase_admin
from firebase_admin import credentials, firestore
import os

# --- 1. SETUP PAGE CONFIGURATION ---
def setup_page_config():
    st.set_page_config(
        page_title="Noor-AI: Islamic Companion",
        page_icon="🌙",
        layout="centered"
    )

# --- 2. CSS: ELEGANT GREEN & GOLD THEME ---
def apply_custom_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

        /* General App Background */
        .stApp { background-color: #0E1117; color: #E0E0E0; }
        
        /* Headers - Antique Gold */
        h1 { 
            color: #E6C15C !important; 
            font-family: 'Inter', sans-serif; 
            text-align: center; 
            font-weight: 300; 
            letter-spacing: 1px; 
            padding-bottom: 10px;
        }
        .stMarkdown h3 { 
            color: #D4AF37 !important; 
            text-align: center; 
            font-weight: 400; 
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #222; }
        
        /* Input Field Styling */
        .stTextInput input { 
            background-color: #1E1E1E !important; 
            color: #E0E0E0 !important; 
            border: 1px solid #444; 
            border-radius: 20px; 
            padding-left: 15px; 
        }
        
        /* --- CHAT INTERFACE STYLING --- */
        
        /* User Message (Odd) - Clean Grey */
        div[data-testid="stChatMessage"]:nth-of-type(odd) {
            background-color: #262730 !important;
            border: 1px solid #3E3E3E !important;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
        }

        /* AI Message (Even) - DEEP ISLAMIC GREEN BACKGROUND */
        div[data-testid="stChatMessage"]:nth-of-type(even) {
            background-color: #14281D !important; /* Deep Matte Green */
            border: 1px solid #4A5D23 !important; /* Olive Border */
            border-left: 4px solid #C5A059 !important; /* Gold Accent Line */
            border-radius: 8px 12px 12px 8px;
            padding: 15px;
            margin-bottom: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        /* TEXT COLOR FIX: FORCE WHITE FOR GENERAL TEXT */
        div[data-testid="stChatMessage"]:nth-of-type(even) p,
        div[data-testid="stChatMessage"]:nth-of-type(even) span,
        div[data-testid="stChatMessage"]:nth-of-type(even) div,
        div[data-testid="stChatMessage"]:nth-of-type(even) li {
             color: #FFFFFF !important; /* Pure White Text */
             line-height: 1.7;
             font-family: 'Inter', sans-serif !important;
             font-weight: 400;
        }

        /* ONLY Key Terms (Bold) are Gold */
        div[data-testid="stChatMessage"]:nth-of-type(even) strong { 
            color: #FFD700 !important; /* Bright Gold */
            font-weight: 700 !important; 
        }

        /* Hyperlinks - Cyan/Blue blend */
        div[data-testid="stChatMessage"]:nth-of-type(even) a { 
            color: #80CBC4 !important; 
            text-decoration: none !important; 
            border-bottom: 1px dotted #80CBC4;
        }
        
        /* Mobile Responsiveness */
        .stMarkdown table { display: block; overflow-x: auto; white-space: nowrap; width: 100%; }
        </style>
    """, unsafe_allow_html=True)

# --- 3. API CONFIGURATION ---
def configure_api():
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
            genai.configure(api_key=api_key)
        else:
            st.error("⚠️ Configuration Error: GOOGLE_API_KEY not found in Secrets.")
            st.stop()
    except Exception as e:
        st.error(f"API Connection Failed: {e}")

# --- 4. FIREBASE INITIALIZATION ---
def init_firebase():
    if firebase_admin._apps:
        return firestore.client()

    try:
        if os.path.exists("service_account.json"):
            cred = credentials.Certificate("service_account.json")
            firebase_admin.initialize_app(cred)
            return firestore.client()
        elif "firebase" in st.secrets:
            firebase_creds = dict(st.secrets["firebase"])
            if "private_key" in firebase_creds:
                firebase_creds["private_key"] = firebase_creds["private_key"].replace('\\n', '\n')
            cred = credentials.Certificate(firebase_creds)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        else:
            return None
    except Exception as e:
        print(f"Database Error: {e}")
        return None

db = init_firebase()

# --- 5. SMART KNOWLEDGE RETRIEVAL ---
def get_knowledge_from_firebase(query):
    if not db: return ""
    try:
        docs = db.collection("knowledge_base").stream()
        context_data = ""
        query_words = query.lower().split()
        found_count = 0
        for doc in docs:
            data = doc.to_dict()
            content = data.get("content", "")
            title = data.get("title", "")
            if any(word in content.lower() for word in query_words if len(word) > 3):
                context_data += f"SOURCE ARTICLE [{title}]:\n{content}\n\n"
                found_count += 1
                if found_count >= 2: break 
        return context_data
    except Exception:
        return ""

# --- 6. DATA LOGGING ---
def save_chat_to_db(user_msg, ai_msg):
    if db:
        try:
            db.collection("chats").add({
                "user": user_msg,
                "ai": ai_msg,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
        except: pass

# --- 7. SYSTEM INSTRUCTIONS (Bold removed from Salam to make it White) ---
system_instruction = """
You are Noor-AI, a sophisticated and caring Islamic companion dedicated to providing accurate knowledge.

*** OPERATIONAL PROTOCOLS ***

1. **THEOLOGICAL INTEGRITY (AQEEDAH):**
   - **Creator:** Attribute creation SOLELY to Allah (SWT). Never imply human creation for your essence.
   - **Development:** If asked about your origin/developer, state: "I was developed and programmed by **Kazi Abdul Halim Sunny**."
   - **Smart Trigger:** If asked "What do you do?" or "Ki koro?", describe your function (teaching Islam). Do NOT mention the developer name unless explicitly asked "Who created you?".

2. **SALAM RESPONSE PROTOCOL:**
   - Upon receiving "Salam" or "Assalamu Alaikum", you MUST respond with the COMPLETE reply: "Wa 'alaykumu s-salam wa rahmatullahi wa barakatuh".
   - (Note: Reply in plain text so it appears WHITE. Do not use bold/asterisks here).

3. **CITATION & LINKS (MANDATORY FORMAT):**
   - **Quran:** Cite strictly as: **[Surah Name: Ayah](https://quran.com/SURAH_NUMBER/AYAH_NUMBER)**
   - **Hadith:** Provide direct, clickable links to **Sunnah.com** where applicable.
     - **Format:** `[Book Name: Number](https://sunnah.com/BOOK_SLUG/NUMBER)`
     - **Example:** **[Sahih al-Bukhari: 1](https://sunnah.com/bukhari:1)**

4. **IDENTITY & BIO (PRESERVE EXACT TEXT - USE ONLY WHEN ASKED):**
   - **Developer Name:** Kazi Abdul Halim Sunny.
   - **Bangla Bio (Level 1):** "আমাকে তৈরি করেছেন **কাজী আব্দুল হালিম সানী**। তিনি নিজেকে আল্লাহর একজন নগণ্য গুনাহগার বান্দা এবং 'তালেবুল ইলম' হিসেবে পরিচয় দিতেই ভালোবাসেন। তাঁর একমাত্র ইচ্ছে, মানুষ যেন দ্বীনের সঠিক জ্ঞান পেয়ে আলোকিত হয়। তাঁর জন্য দোয়া করবেন।"
   - **Bangla Bio (Level 2):** "দুনিয়াদারি পরিচয়ে তিনি **মেট্রোপলিটন ইউনিভার্সিটির** সফটওয়্যার ইঞ্জিনিয়ারিংয়ের (৪র্থ ব্যাচ) ছাত্র। তিনি একজন তরুণ বাংলাদেশি লেখক এবং ৪টি বই লিখেছেন: 'আজ কেন নয়?', 'একটুকরো স্বপ্ন', 'অমানিশা', এবং 'প্রিটেন্ড' (তরুণদের সমস্যা নিয়ে লেখা উপন্যাস - যার অনলাইন কপি সবার জন্য ফ্রী)।"

5. **LINGUISTIC CONSISTENCY:**
   - Respond in **English** if the query is in English.
   - Respond in **Bangla** if the query is in Bangla.
   - **Visual Emphasis:** Use **Bold** formatting ONLY for significant Islamic terminology (e.g., **Tawhid**, **Taqwa**) so they render in **GOLD**. Keep normal sentences in plain text to render WHITE.

6. **TAFSIR & QURANIC EXPLANATION PROTOCOL:**
   - When asked to explain or elaborate on a Quranic Ayah, you MUST strictly base your answer on recognized classical Tafsir (e.g., **Tafsir Ibn Kathir**, **Tafsir As-Sa'di**, **Tafsir Al-Tabari**, or **Tafsir Al-Qurtubi**).
   - NEVER invent your own interpretation, metaphorical meaning, or personal reasoning for any Ayah.
   - Always mention the source of the explanation. 
     - English Example: "According to **Tafsir Ibn Kathir**..."
     - Bangla Example: "**তাফসীরে ইবনে কাসীর** অনুযায়ী..."
"""

# --- 8. SESSION MANAGEMENT (Gemini 2.5 Flash) ---
def initialize_session():
    if "history" not in st.session_state:
        st.session_state.history = []
        
    try:
        if "model" not in st.session_state:
            # Using Gemini 2.5 Flash
            st.session_state.model = genai.GenerativeModel("gemini-2.5-flash", system_instruction=system_instruction)
            st.session_state.chat = st.session_state.model.start_chat(history=[])
    except Exception as e:
        st.error(f"System Initialization Failure: {e}")

# --- 9. SIDEBAR (ORIGINAL STYLE) ---
def display_sidebar():
    with st.sidebar:
        st.title("🌙 Noor-AI")
        st.markdown("---") 
        st.markdown("**Developer:**")
        st.markdown("### Kazi Abdul Halim Sunny")
        
        st.markdown("---")
        st.info("Insights derived strictly from the Holy Qur'an & Authentic Sunnah.")
        st.warning("Disclaimer: For specific Fiqh rulings, kindly consult a qualified local scholar.")
        
        if st.session_state.history:
            chat_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.history])
            st.download_button("📥 Export Conversation", chat_str, "noor_ai_session.txt")

# --- 10. MAIN APP ---
def main():
    setup_page_config()
    apply_custom_styles()
    configure_api()
    initialize_session()
    display_sidebar()

    st.title("Noor-AI: Islamic Companion") 
    st.markdown("### Authentic Guidance from Qur'an & Sunnah")
    st.divider()

    # --- AUTO HISTORY LIMIT (Keep last 8) ---
    if len(st.session_state.history) > 8:
        st.session_state.history = st.session_state.history[-8:]

    for message in st.session_state.history:
        role = message["role"]
        avatar = "👤" if role == "user" else "🎓"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

    prompt = st.chat_input("Inquire about Islam, History, or Spirituality...")

    if prompt:
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🎓"):
            placeholder = st.empty()
            placeholder.markdown("Analyzing sources...") 
            try:
                retrieved_context = get_knowledge_from_firebase(prompt)
                
                if retrieved_context:
                    final_prompt = f"CONTEXT:\n{retrieved_context}\n\nUSER QUESTION: {prompt}"
                else:
                    final_prompt = prompt

                if hasattr(st.session_state, 'chat'):
                    try:
                        # --- FORMAT CONVERSION FOR GEMINI ---
                        gemini_history = []
                        for msg in st.session_state.history:
                            role = "user" if msg["role"] == "user" else "model"
                            gemini_history.append({"role": role, "parts": [msg["content"]]})

                        st.session_state.chat = st.session_state.model.start_chat(history=gemini_history)
                        
                        response = st.session_state.chat.send_message(final_prompt)
                        placeholder.markdown(response.text)
                        
                        st.session_state.history.append({"role": "assistant", "content": response.text})
                        save_chat_to_db(prompt, response.text)
                        
                    except Exception as e:
                        if "429" in str(e):
                            placeholder.warning("⚠️ High traffic. Please wait 30 seconds.")
                        else:
                            placeholder.error(f"Error: {e}")
            except Exception as e:
                placeholder.error(f"Processing Error: {e}")

if __name__ == "__main__":
    main()
