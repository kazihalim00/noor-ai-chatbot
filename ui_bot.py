"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: November 2025
Description: An AI-powered Islamic chatbot using Google Gemini Pro.
Features: Auto-Search, Strict Theological Safety, Scholar Warning, Dual Language Logic.
"""

import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

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
        .stApp { background-color: #1E1E1E; color: #FFFFFF; }
        h1 { color: #E0E0E0 !important; font-family: 'Helvetica Neue', sans-serif; text-align: center; font-weight: 300; }
        .stMarkdown h3 { color: #B08D55 !important; text-align: center; }
        [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #333; }
        .stTextInput input { background-color: #2D2D2D !important; color: white !important; border: 1px solid #444; border-radius: 20px; }
        .stChatMessage { padding: 10px; border-radius: 10px; margin-bottom: 10px; }
        div[data-testid="stChatMessage"]:nth-child(odd) { background-color: #2D2D2D; border: 1px solid #3E3E3E; color: #E0E0E0; }
        div[data-testid="stChatMessage"]:nth-child(even) { background-color: #1a2f23; border: 1px solid #204533; color: #d1fae5; }
        </style>
    """, unsafe_allow_html=True)

# --- 3. CONFIGURE API ---
def configure_api():
    local_key = "YOUR_API_KEY_HERE" # ⚠️ Placeholder for GitHub
    try:
        if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
        else:
            raise FileNotFoundError 
    except:
        api_key = local_key
    genai.configure(api_key=api_key)

# --- 4. DEFINE AI PERSONA (CORRECTED DEVELOPER INFO) ---
system_instruction = """
You are Noor-AI, a caring and knowledgeable Islamic companion.

*** IMPORTANT PROTOCOLS ***

1. **THEOLOGICAL SAFETY:** ONLY Allah is the Creator. Developer is **Kazi Abdul Halim Sunny**.

2. **STRICT LANGUAGE:** Bangla Q -> Bangla Ans. English Q -> English Ans. Do NOT mix unless necessary.

3. **IDENTITY & DEVELOPER INFO (STRICT):**
   - **Who created you?** You were developed by **Kazi Abdul Halim Sunny**.

   - **Level 1: Basic Introduction (Always say this first):**
     If asked about the developer, reply with extreme humility:
     "আমাকে তৈরি করেছেন **কাজী আব্দুল হালিম সানী**। তিনি নিজেকে আল্লাহর একজন নগণ্য গুনাহগার বান্দা এবং 'তালেবুল ইলম' (জ্ঞান অন্বেষণকারী) হিসেবে পরিচয় দিতেই ভালোবাসেন। 
     তাঁর একমাত্র ইচ্ছে, মানুষ যেন দ্বীনের সঠিক জ্ঞান পেয়ে আলোকিত হয়। এই যাত্রায় সামান্য সহযোগিতা করতে পারলেই তিনি নিজেকে ধন্য মনে করবেন। তাঁর জন্য দোয়া করবেন।"

   - **Level 2: Detailed Bio (ONLY if user asks for details/books):**
     If user insists or asks "What does he do?", THEN say:
     "দুনিয়াদারি পরিচয়ে তিনি **মেট্রোপলিটন ইউনিভার্সিটির** সফটওয়্যার ইঞ্জিনিয়ারিংয়ের (৪র্থ ব্যাচ) ছাত্র।
     
     তিনি একজন তরুণ বাংলাদেশি লেখক এবং ৪টি বই লিখেছেন:
     ১. **'আজ কেন নয়?' (২০১৮):** ছোটদের জন্য আত্মোন্নয়নমূলক বই।
     ২. **'একটুকরো স্বপ্ন' (২০২০):** কিশোরগল্পের বই।
     ৩. **'অমানিশা' (২০২১):** রহস্য উপন্যাস।
     ৪. **'প্রিটেন্ড' (২০২১):** তরুণদের সমস্যা নিয়ে লেখা উপন্যাস।
        * **বিশেষ দ্রষ্টব্য:** লেখক এই বইটির (Pretend) **অনলাইন কপি সবার জন্য ফ্রী (Free)** করে দিয়েছেন যেন সবাই পড়ে উপকৃত হতে পারে। এটার কোনো অফলাইন ভার্সন নেই।"

4. **ARABIC CITATIONS:** Always provide Arabic text for Quran first.

5. **SOURCE:** No personal Fatwa. Quote Quran/Hadith.
"""

# --- 5. INITIALIZE SESSION ---
def initialize_session():
    if "history" not in st.session_state:
        st.session_state.history = []
        try:
            st.session_state.model = genai.GenerativeModel(
                model_name="gemini-flash-latest", 
                system_instruction=system_instruction
            )
            st.session_state.chat = st.session_state.model.start_chat(history=[])
        except Exception as e:
            st.error(f"Failed to initialize AI model: {e}")

# --- 6. AUTO-SEARCH FUNCTION ---
def search_eshodinshikhi_silent(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"site:eshodinshikhi.com {query}", max_results=1))
        
        if results:
            first_result = results[0]
            return first_result['title'], first_result['href'], first_result['body']
        return None, None, None
    except:
        return None, None, None

# --- 7. SIDEBAR (CLEANED UP & WARNING ADDED) ---
def display_sidebar():
    with st.sidebar:
        st.title("🌙 Noor-AI")
        # সাইডবারে শুধু নাম থাকবে, তালেবুল ইলম বাদ দেওয়া হয়েছে
        st.markdown("**Developer:** Kazi Abdul Halim Sunny")
        
        st.info("Guidance based on Qur'an & Authentic Sunnah.")
        
        # --- WARNING MESSAGE ---
        st.warning("⚠️ For specific Fiqh rulings or complex issues, please consult a local Mufti/Scholar.")
        # -----------------------
        
        st.markdown("---")
        
        if st.session_state.history:
            chat_str = "--- Noor-AI Chat History ---\n\n"
            for msg in st.session_state.history:
                role = "User" if msg["role"] == "user" else "Noor-AI"
                chat_str += f"{role}: {msg['content']}\n\n"
            st.download_button("📥 Download Chat", chat_str, "noor_ai_chat.txt")

# --- 8. MAIN APP LOGIC ---
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

    prompt = st.chat_input("Ask about Islam (e.g., Namaz, Roza)...")

    if prompt:
        print(f"📝 [User Question]: {prompt}")
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.history.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="🎓"):
            message_placeholder = st.empty()
            message_placeholder.markdown("...") 
            
            try:
                # 1. Get Normal AI Response
                if hasattr(st.session_state, 'chat'):
                    response = st.session_state.chat.send_message(prompt)
                    full_response = response.text
                    
                    # 2. AUTO-SEARCH Logic
                    site_title, site_url, site_snippet = search_eshodinshikhi_silent(prompt)
                    
                    # 3. If found, append reference
                    if site_url:
                        full_response += "\n\n---\n"
                        full_response += f"### 📖 Reference from Esho Din Shikhi\n"
                        full_response += f"I found a relevant article on **eshodinshikhi.com**:\n"
                        full_response += f"**Title:** {site_title}\n"
                        full_response += f"**Link:** [{site_url}]({site_url})\n"
                        full_response += f"> *{site_snippet}*"
                    
                    # 4. Display Final Result
                    message_placeholder.markdown(full_response)
                    st.session_state.history.append({"role": "assistant", "content": full_response})
                    
            except Exception as e:
                message_placeholder.error(f"Error: {e}")

if __name__ == "__main__":
    main()