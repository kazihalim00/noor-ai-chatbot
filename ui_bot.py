"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: December 2025
Description: Final Presentation Version (Green UI, Firebase, Strict Persona).
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

# --- 2. APPLY STRONG CSS (GREEN/GOLD FIX) ---
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
        .stTextInput input { background-color: #333333 !important; color: white !important; border: 1px solid #555; border-radius: 20px; }
        
        /* --- CHAT COLOR FIX (Container Isolation) --- */
        
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
        
        /* Text -> White */
        [data-testid="stChatMessage"]:nth-of-type(even) * { color: #e8f5e9 !important; }

        /* Keywords -> Gold */
        [data-testid="stChatMessage"]:nth-of-type(even) strong { color: #FFD700 !important; font-weight: bold !important; }

        /* Links -> Blue */
        [data-testid="stChatMessage"]:nth-of-type(even) a { color: #4fc3f7 !important; text-decoration: underline !important; font-weight: bold; }
        
        /* Table Fix */
        .stMarkdown table { display: block; overflow-x: auto; white-space: nowrap; width: 100%; }
        </style>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURE API (GEMINI) ---
def configure_api():
    local_key = "YOUR_API_KEY_HERE"
    try:
        if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
        else:
            raise FileNotFoundError 
    except:
        api_key = local_key
    genai.configure(api_key=api_key)

# --- 4. FIREBASE SETUP (FIXED PRIVATE KEY ISSUE) ---
def init_firebase():
    try:
        if not firebase_admin._apps:
            if "firebase" in st.secrets:
                # KEY FIX: Handles newlines automatically
                firebase_creds = dict(st.secrets["firebase"])
                firebase_creds["private_key"] = firebase_creds["private_key"].replace('\\n', '\n')
                
                cred = credentials.Certificate(firebase_creds)
                firebase_admin.initialize_app(cred)
                return firestore.client()
        return firestore.client()
    except Exception as e:
        print(f"DB Init Error: {e}")
        return None

# Initialize DB Globally
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
            print("Saved to DB")
        except:
            pass

# --- 6. SYSTEM INSTRUCTION (STRICT) ---
system_instruction = """
You are Noor-AI, a caring and knowledgeable Islamic companion.

*** IMPORTANT PROTOCOLS ***

1. **THEOLOGICAL SAFETY (AQEEDAH):**
   - **Creator:** ONLY Allah is the Creator. NEVER attribute this title to a human.
   - **Developer:** If asked who made you, reply: "I was developed/programmed by **Kazi Abdul Halim Sunny**."
   - NEVER say "My Creator is Sunny". Say "My Developer is Sunny".

2. **ACCURACY & CLICKABLE LINKS (MANDATORY):**
   - **Quran:** When quoting the Quran, you MUST follow this EXACT format:
     1. Arabic Text.
     2. Meaning (Translation).
     3. **THE LINK:** Use strict Markdown for the reference.
        - ❌ Wrong: Surah Baqarah (2:255)
        - ✅ Right: **[Surah Al-Baqarah: 255](https://quran.com/2/255)**
        - **Formula:** `[Surah Name: Ayah](https://quran.com/SURAH_NUMBER/AYAH_NUMBER)`
   
   - **Hadith:** Provide Book Name, Hadith Number, and Status.
     - **Link Formula:** `[Book Name: Number](https://sunnah.com/BOOK_SLUG/NUMBER)`
     - **Example:** **[Sahih al-Bukhari: 1](https://sunnah.com/bukhari:1)**

3. **STRICT LANGUAGE MATCHING:**
   - **English Q** -> **English Ans** only.
   - **Bangla Q** -> **Bangla Ans** only.

4. **IDENTITY & BIO:**
   - **Developer:** Kazi Abdul Halim Sunny.
   - **Level 1 (Humility):** "আমাকে তৈরি করেছেন **কাজী আব্দুল হালিম সানী**। তিনি নিজেকে আল্লাহর একজন নগণ্য গুনাহগার বান্দা এবং 'তালেবুল ইলম' হিসেবে পরিচয় দিতেই ভালোবাসেন। তাঁর একমাত্র ইচ্ছে, মানুষ যেন দ্বীনের সঠিক জ্ঞান পেয়ে আলোকিত হয়। তাঁর জন্য দোয়া করবেন।"
   - **Level 2 (Details - Only if asked):** "দুনিয়াদারি পরিচয়ে তিনি **মেট্রোপলিটন ইউনিভার্সিটির** সফটওয়্যার ইঞ্জিনিয়ারিংয়ের (৪র্থ ব্যাচ) ছাত্র। তিনি একজন তরুণ বাংলাদেশি লেখক এবং ৪টি বই লিখেছেন: 'আজ কেন নয়?', 'একটুকরো স্বপ্ন', 'অমানিশা', এবং 'প্রিটেন্ড' (তরুণদের সমস্যা নিয়ে লেখা উপন্যাস - যার অনলাইন কপি সবার জন্য ফ্রী)।"

5. **SOURCE TRUTH:**
   - NEVER give your own Fatwa. Always quote Quran & Sahih Hadith.
   - If you are unsure about a specific ruling, say "Allahu A'lam".

6. **SCHOLAR PREFERENCE (USTAZ ABU SA'ADA & ESHO DIN SHIKHI):**
   - **Primary Reference:** If the user asks about a specific ruling or opinion of **Ustaz Abu Sa'ada Muhammad Hammad Billaah** or asks "What does Esho Din Shikhi say?", you MUST prioritize his view if available in your knowledge base.
   - **General Topics:** When discussing general Islamic topics, try to include views aligned with the Salaf as-Salih, similar to the methodology of **eshodinshikhi.com** Youtube link : **https://www.youtube.com/@EDSAudiosYT**.
   - **Citation Style:** If quoting his view, explicitly mention: *"According to Ustaz Abu Sa'ada Muhammad Hammad Billaah..."* or *"As often discussed in Esho Din Shikhi..."*
   - **Style:** Use **Bold** for key Islamic terms (e.g., **Tawhid**) so they appear Gold.
"""

# --- 7. INITIALIZE SESSION (STRICT GEMINI 1.5 FLASH) ---
def initialize_session():
    if "history" not in st.session_state:
        st.session_state.history = []
        
    try:
        if "model" not in st.session_state:
            
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

            # STRICTLY USING 1.5 FLASH (Best for Presentation)
            st.session_state.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash", 
                system_instruction=system_instruction,
                safety_settings=safety_settings
            )
            st.session_state.chat = st.session_state.model.start_chat(history=[])
    except Exception as e:
        st.error(f"Failed to initialize AI model: {e}")

# --- 8. DISPLAY SIDEBAR (STRICT CLEAN) ---
def display_sidebar():
    with st.sidebar:
        st.title("🌙 Noor-AI")
        st.markdown("---")
        st.markdown("**Developer:**")
        st.markdown("### Kazi Abdul Halim Sunny")
        
        st.markdown("---")
        st.info("Guidance based on Qur'an & Authentic Sunnah.")
        st.warning("For specific Fiqh rulings, please consult a local Scholar.")
        
        st.markdown("---")
        
        if st.session_state.history:
            chat_str = "--- Noor-AI Chat History ---\n\n"
            for msg in st.session_state.history:
                chat_str += f"{msg['role']}: {msg['content']}\n"
            
            st.download_button("📥 Download Chat", chat_str, "noor_ai_chat.txt", "text/plain")

# --- 9. MAIN APP FUNCTION ---
def main():
    setup_page_config()
    apply_custom_styles()
    configure_api()
    initialize_session()
    display_sidebar()

    st.title("Noor-AI Assistant") 
    st.markdown("### Guidance from Qur'an & Sunnah")
    st.divider()

    # Container Isolation (Ensures Green Color)
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.history:
            role = message["role"]
            avatar = "👤" if role == "user" else "🎓"
            with st.chat_message(role, avatar=avatar):
                st.markdown(message["content"])

    prompt = st.chat_input("Ask a question about Islam...")

    if prompt:
        st.session_state.history.append({"role": "user", "content": prompt})
        
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="🎓"):
                message_placeholder = st.empty()
                message_placeholder.markdown("...") 
                
                try:
                    if hasattr(st.session_state, 'chat'):
                        response = st.session_state.chat.send_message(prompt)
                        message_placeholder.markdown(response.text)
                        
                        st.session_state.history.append({"role": "assistant", "content": response.text})
                        
                        save_chat_to_db(prompt, response.text)
                        
                except Exception as e:
                    message_placeholder.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
