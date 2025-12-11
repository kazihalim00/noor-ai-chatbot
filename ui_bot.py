"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: December 2025
Description: FINAL STRICT VERSION - Full Instructions, Green/Gold UI, Firebase, Full Salam.
"""

import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. SETUP PAGE ---
def setup_page_config():
    st.set_page_config(
        page_title="Noor-AI Pro",
        page_icon="🌙",
        layout="centered"
    )

# --- 2. CSS: GREEN & GOLD THEME (OLD LOGIC RESTORED) ---
def apply_custom_styles():
    st.markdown("""
        <style>
        /* General App Styling */
        .stApp { background-color: #121212; color: #FFFFFF; }
        
        /* Headers */
        h1 { color: #E0E0E0 !important; font-family: 'Helvetica Neue', sans-serif; text-align: center; font-weight: 300; }
        .stMarkdown h3 { color: #FDD835 !important; text-align: center; }
        
        /* Sidebar */
        [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #333; }
        
        /* Input Box */
        .stTextInput input { background-color: #333333 !important; color: white !important; border: 1px solid #555; border-radius: 20px; }
        
        /* --- CHAT MESSAGES --- */
        
        /* User (Odd) -> Grey */
        div[data-testid="stChatMessage"]:nth-of-type(odd) {
            background-color: #262626 !important;
            border: 1px solid #444 !important;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
        }

        /* AI (Even) -> Deep Green */
        div[data-testid="stChatMessage"]:nth-of-type(even) {
            background-color: #0d3b1e !important; /* Deep Green */
            border: 1px solid #1e5c30 !important;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        /* AI Text -> White */
        div[data-testid="stChatMessage"]:nth-of-type(even) p,
        div[data-testid="stChatMessage"]:nth-of-type(even) div,
        div[data-testid="stChatMessage"]:nth-of-type(even) li {
             color: #e8f5e9 !important; 
        }

        /* GOLDEN TEXT (Important) */
        div[data-testid="stChatMessage"]:nth-of-type(even) strong { 
            color: #FFD700 !important; /* Pure Gold */
            font-weight: bold !important; 
        }

        /* LINKS -> Blue */
        div[data-testid="stChatMessage"]:nth-of-type(even) a { 
            color: #4fc3f7 !important; 
            text-decoration: underline !important; 
            font-weight: bold; 
        }
        
        /* Mobile Table Fix */
        .stMarkdown table { display: block; overflow-x: auto; white-space: nowrap; width: 100%; }
        </style>
    """, unsafe_allow_html=True)

# --- 3. API CONFIG (DIRECT KEY) ---
def configure_api():
    
    api_key = "YOUR_REAL_KEY_HERE"
    
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"API Error: {e}")

# --- 4. FIREBASE SETUP ---
def init_firebase():
    try:
        if not firebase_admin._apps:
            if "firebase" in st.secrets:
                firebase_creds = dict(st.secrets["firebase"])
                if "private_key" in firebase_creds:
                    firebase_creds["private_key"] = firebase_creds["private_key"].replace('\\n', '\n')
                cred = credentials.Certificate(firebase_creds)
                firebase_admin.initialize_app(cred)
                return firestore.client()
        return firestore.client()
    except Exception as e:
        print(f"DB Error: {e}")
        return None

db = init_firebase()

# --- 5. SAVE FUNCTION ---
def save_chat_to_db(user_msg, ai_msg):
    if db:
        try:
            db.collection("chats").add({
                "user": user_msg,
                "ai": ai_msg,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            print("Chat saved.")
        except:
            pass

# --- 6. ULTIMATE SYSTEM INSTRUCTION (NOTHING MISSED) ---
system_instruction = """
You are Noor-AI, a caring and knowledgeable Islamic companion.

*** STRICT PROTOCOLS (DO NOT SKIP) ***

1. **THEOLOGICAL SAFETY (AQEEDAH):**
   - **Creator:** ONLY Allah is the Creator. NEVER attribute this title to a human.
   - **Developer:** If asked who made you, reply: "I was developed/programmed by **Kazi Abdul Halim Sunny**."

2. **SALAM PROTOCOL (FULL ANSWER):**
   - If user says "Salam" or "Assalamu Alaikum" (in any language), you MUST reply with the FULL answer: "**Wa 'alaykumu s-salam wa rahmatullahi wa barakatuh**". 
   - Never give a short "Walaikum Assalam".

3. **ACCURACY & CLICKABLE LINKS (MANDATORY):**
   - **Quran:** Use strict format: **[Surah Name: Ayah](https://quran.com/SURAH_NUMBER/AYAH_NUMBER)**
   - **Hadith:** Provide clickable link to **Sunnah.com** whenever possible.
     - **Formula:** `[Book Name: Number](https://sunnah.com/BOOK_SLUG/NUMBER)`
     - **Example:** **[Sahih al-Bukhari: 1](https://sunnah.com/bukhari:1)**

4. **IDENTITY & BIO (EXACT TEXT):**
   - **Developer:** Kazi Abdul Halim Sunny.
   - **Bangla Bio (Level 1):** "আমাকে তৈরি করেছেন **কাজী আব্দুল হালিম সানী**। তিনি নিজেকে আল্লাহর একজন নগণ্য গুনাহগার বান্দা এবং 'তালেবুল ইলম' হিসেবে পরিচয় দিতেই ভালোবাসেন। তাঁর একমাত্র ইচ্ছে, মানুষ যেন দ্বীনের সঠিক জ্ঞান পেয়ে আলোকিত হয়। তাঁর জন্য দোয়া করবেন।"
   - **Bangla Bio (Level 2 - Details):** "দুনিয়াদারি পরিচয়ে তিনি **মেট্রোপলিটন ইউনিভার্সিটির** সফটওয়্যার ইঞ্জিনিয়ারিংয়ের (৪র্থ ব্যাচ) ছাত্র। তিনি একজন তরুণ বাংলাদেশি লেখক এবং ৪টি বই লিখেছেন: 'আজ কেন নয়?', 'একটুকরো স্বপ্ন', 'অমানিশা', এবং 'প্রিটেন্ড' (তরুণদের সমস্যা নিয়ে লেখা উপন্যাস - যার অনলাইন কপি সবার জন্য ফ্রী)।"

5. **LANGUAGE MATCHING:**
   - **English Question** -> **English Answer**.
   - **Bangla Question** -> **Bangla Answer**.

6. **SCHOLAR PREFERENCE:**
   - Prioritize views of **Ustaz Abu Sa'ada Muhammad Hammad Billaah** & **Esho Din Shikhi**.
   - **Formatting:** Use **Bold** for key Islamic terms (e.g., **Tawhid**, **Jannah**) so they appear **GOLDEN**.
"""

# --- 7. SESSION ---
def initialize_session():
    if "history" not in st.session_state:
        st.session_state.history = []
        
    try:
        if "model" not in st.session_state:
            st.session_state.model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)
            st.session_state.chat = st.session_state.model.start_chat(history=[])
    except Exception as e:
        st.error(f"AI Init Failed: {e}")

# --- 8. SIDEBAR (RESTORED SPACING) ---
def display_sidebar():
    with st.sidebar:
        st.title("🌙 Noor-AI")
        st.markdown("---") 
        st.markdown("**Developer:**")
        st.markdown("### Kazi Abdul Halim Sunny")
        
        st.markdown("---")
        st.info("Guidance based on Qur'an & Authentic Sunnah.")
        st.warning("For specific Fiqh rulings, please consult a local Scholar.")
        
        if st.session_state.history:
            chat_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.history])
            st.markdown("---")
            st.download_button("📥 Download Chat", chat_str, "chat.txt")

# --- 9. MAIN APP ---
def main():
    setup_page_config()
    apply_custom_styles()
    configure_api()
    initialize_session()
    display_sidebar()

    st.title("Noor-AI Assistant") 
    st.markdown("### Guidance from Qur'an & Sunnah")
    st.divider()

    # --- DISPLAY CHAT HISTORY FIRST (Crucial for Green Color) ---
    for message in st.session_state.history:
        role = message["role"]
        avatar = "👤" if role == "user" else "🎓"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

    # --- INPUT ---
    prompt = st.chat_input("Ask a question about Islam...")

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
                    
                    # Save to Firebase
                    save_chat_to_db(prompt, response.text)
                    
            except Exception as e:
                placeholder.error(f"Error: {e}")

if __name__ == "__main__":
    main()
