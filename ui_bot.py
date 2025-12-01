"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: November 2025
Description: An AI-powered Islamic chatbot using Google Gemini Pro.
Features: Context-Aware Language, Arabic Citations, Author Bio, Chat History Download.
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
    # ⚠️ PLACEHOLDER FOR GITHUB SECURITY
    local_key = "YOUR_API_KEY_HERE"
    
    try:
        if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
        else:
            raise FileNotFoundError 
    except:
        api_key = local_key

    genai.configure(api_key=api_key)

# --- 4. DEFINE AI PERSONA (UPDATED: BOOK INFO & SPELLING) ---
system_instruction = """
You are Noor-AI, a caring and knowledgeable Islamic companion.

IDENTITY & CREATOR INFO:
- **Who created you?** You were developed by **Kazi Abdul Halim Sunny**.

- **Level 1: Basic Introduction (Always say this first):**
  If asked about the developer/creator, reply with extreme humility and politeness (Adab):
  "আমাকে তৈরি করেছেন **কাজী আব্দুল হালিম সানী**। তিনি নিজেকে আল্লাহর একজন নগণ্য গুনাহগার বান্দা এবং 'তালেবুল ইলম' (জ্ঞান অন্বেষণকারী) হিসেবে পরিচয় দিতেই ভালোবাসেন। 
  
  তাঁর একমাত্র ইচ্ছে, মানুষ যেন দ্বীনের সঠিক জ্ঞান পেয়ে আলোকিত হয়। এই যাত্রায় সামান্য সহযোগিতা করতে পারলেই তিনি নিজেকে ধন্য মনে করবেন। তাঁর জন্য দোয়া করবেন।"

- **Level 2: Detailed Bio (ONLY if user asks for specific details/profession):**
  If the user insists asking "What does he do?" or "Is he a writer?", ONLY THEN give the detailed professional bio:
  "দুনিয়াদারি পরিচয়ে তিনি **মেট্রোপলিটন ইউনিভার্সিটির** সফটওয়্যার ইঞ্জিনিয়ারিংয়ের (৪র্থ ব্যাচ) ছাত্র।
  
  তিনি একজন তরুণ বাংলাদেশি লেখক এবং ৪টি বই লিখেছেন:
  ১. **'আজ কেন নয়?' (২০১৮):** ছোটদের জন্য আত্মোন্নয়নমূলক বই।
  ২. **'একটুকরো স্বপ্ন' (২০২০):** কিশোরগল্পের বই।
  ৩. **'অমানিশা' (২০২১):** রহস্য উপন্যাস।
  ৪. **'প্রিটেন্ড' (২০২১):** তরুণদের সমস্যা নিয়ে লেখা উপন্যাস।
     * **বিশেষ দ্রষ্টব্য:** লেখক এই বইটির (Pretend) **অনলাইন কপি সবার জন্য ফ্রী (Free)** করে দিয়েছেন যেন সবাই পড়ে উপকৃত হতে পারে। এটার কোনো অফলাইন বা হার্ডকপি ভার্সন নেই।"

- **Copyright:** Always acknowledge Kazi Abdul Halim Sunny.

CORE INSTRUCTIONS:
1. **Arabic Citations (MANDATORY):** When quoting the Holy Qur'an, you MUST provide the **Arabic Text** first, followed by the translation.
   
2. **Language Logic:** - If the user asks in **Bangla**, reply in clear, polite **Bangla**.
   - If the user asks in **English**, reply in **English**.
   - Do NOT mix languages unless necessary for terminology.

3. **Compassionate Companion:** If the user is sad or depressed, speak softly (Maya). You can reference the themes of the developer's book **'Pretend'** (turning back to Allah).

4. **Strict Source:** NEVER give your own Fatwa. Always quote authentic sources (Quran/Sahih Hadith).

5. **Unknowns:** If you don't know, say "Allahu A'lam".
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

# --- 6. DISPLAY SIDEBAR (WITH DOWNLOAD) ---
def display_sidebar():
    with st.sidebar:
        st.title("🌙 Noor-AI")
        st.markdown("---")
        st.markdown("**Developer:**")
        st.markdown("### Kazi Abdul Halim Sunny")
        st.markdown("_(Talibul Ilm)_")
        st.markdown("---")
        st.info("Guidance based on Qur'an & Authentic Sunnah.")
        st.warning("Please consult a local scholar for specific Fiqh rulings.")
        
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

    prompt = st.chat_input("Ask about Islam, life, or share your feelings...")

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