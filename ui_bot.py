"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: November 2025
Description: An AI-powered Islamic chatbot using Google Gemini Pro.
Features: Fixed Clickable Links, Accurate Citations, Strict Theological Safety, Author Bio.
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

# --- 2. APPLY PROFESSIONAL & HIGH CONTRAST STYLES ---
def apply_custom_styles():
    st.markdown("""
        <style>
        /* General App Styling */
        .stApp {
            background-color: #121212; /* Deep Black */
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
            color: #FDD835 !important; /* Bright Gold */
            text-align: center;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #000000;
            border-right: 1px solid #333;
        }
        
        /* Input Box Styling */
        .stTextInput input {
            background-color: #333333 !important;
            color: white !important;
            border: 1px solid #555;
            border-radius: 20px;
        }
        
        /* Chat Bubble Styling */
        .stChatMessage {
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 12px;
        }
        
        /* User Message */
        div[data-testid="stChatMessage"]:nth-child(odd) {
            background-color: #262626; 
            border: 1px solid #444;
        }
        div[data-testid="stChatMessage"]:nth-child(odd) p,
        div[data-testid="stChatMessage"]:nth-child(odd) div {
            color: #FFFFFF !important;
        }

        /* AI Message */
        div[data-testid="stChatMessage"]:nth-child(even) {
            background-color: #0d3b1e; 
            border: 1px solid #1e5c30;
        }
        div[data-testid="stChatMessage"]:nth-child(even) p, 
        div[data-testid="stChatMessage"]:nth-child(even) div,
        div[data-testid="stChatMessage"]:nth-child(even) li,
        div[data-testid="stChatMessage"]:nth-child(even) span {
            color: #ffffff !important; 
            font-weight: 400; 
        }
        div[data-testid="stChatMessage"]:nth-child(even) h1,
        div[data-testid="stChatMessage"]:nth-child(even) h2,
        div[data-testid="stChatMessage"]:nth-child(even) h3,
        div[data-testid="stChatMessage"]:nth-child(even) strong {
            color: #FFD700 !important; /* Gold Headers */
        }
        /* LINK STYLING (Blue & Underlined) */
        div[data-testid="stChatMessage"]:nth-child(even) a {
            color: #4fc3f7 !important; 
            text-decoration: underline !important;
            font-weight: bold;
        }

        /* Mobile Table Fix */
        .stMarkdown table {
            display: block;
            overflow-x: auto;
            white-space: nowrap;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURE API (SECURE MODE) ---
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

# --- 4. DEFINE AI PERSONA (STRICT LINKS ADDED) ---
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

3. **STRICT LANGUAGE MATCHING:**
   - **English Q** -> **English Ans** only.
   - **Bangla Q** -> **Bangla Ans** only.

4. **IDENTITY & BIO:**
   - **Developer:** Kazi Abdul Halim Sunny.
   - **Level 1 (Humility):** "আমাকে তৈরি করেছেন **কাজী আব্দুল হালিম সানী**। তিনি নিজেকে আল্লাহর একজন নগণ্য গুনাহগার বান্দা এবং 'তালেবুল ইলম' হিসেবে পরিচয় দিতেই ভালোবাসেন। তাঁর একমাত্র ইচ্ছে, মানুষ যেন দ্বীনের সঠিক জ্ঞান পেয়ে আলোকিত হয়। তাঁর জন্য দোয়া করবেন।"
   - **Level 2 (Details - Only if asked):** "দুনিয়াদারি পরিচয়ে তিনি **মেট্রোপলিটন ইউনিভার্সিটির** সফটওয়্যার ইঞ্জিনিয়ারিংয়ের (৪র্থ ব্যাচ) ছাত্র। তিনি একজন তরুণ বাংলাদেশি লেখক এবং ৪টি বই লিখেছেন: 'আজ কেন নয়?', 'একটুকরো স্বপ্ন', 'অমানিশা', এবং 'প্রিটেন্ড' (তরুণদের সমস্যা নিয়ে লেখা উপন্যাস - যার অনলাইন কপি সবার জন্য ফ্রী)।"

5. **SOURCE TRUTH:**
   - NEVER give your own Fatwa. Always quote Quran & Sahih Hadith.
   - If you are unsure about a specific ruling, say "Allahu A'lam".
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
                model_name="gemini-1.5-flash", 
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
        st.warning("For specific Fiqh rulings, please consult a local Scholar.")
        
        st.markdown("---")
        
        if st.session_state.history:
            chat_str = "--- Noor-AI Chat History ---\n\n"
            for msg in st.session_state.history:
                role = "User" if msg["role"] == "user" else "Noor-AI"
                chat_str += f"{role}: {msg['content']}\n\n"
            
            st.download_button(
                label="📥 Download Chat",
                data=chat_str,
                file_name="noor_ai_chat.txt",
                mime="text/plain"
            )

# --- 7. MAIN APP FUNCTION ---
def main():
    setup_page_config()
    apply_custom_styles()
    configure_api()
    initialize_session()
    display_sidebar()

    st.title("Noor-AI Assistant") 
    st.markdown("### Guidance from Qur'an & Sunnah")
    st.divider()

    for message in st.session_state.history:
        role = message["role"]
        avatar_icon = "👤" if role == "user" else "🎓"
        with st.chat_message(role, avatar=avatar_icon):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask a question about Islam, life, or share your feelings...")

    if prompt:
        # Developer Logging
        print(f"📝 [User Question]: {prompt}")

        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.history.append({"role": "user", "content": prompt})

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
