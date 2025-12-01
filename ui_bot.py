"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: November 2025
Description: An AI-powered Islamic chatbot using Google Gemini Pro.
Features: Auto-Search eshodinshikhi.com, Strict Theological Safety, Dual Language Logic.
"""

import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS  # New Search Tool

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
    local_key = "YOUR_API_KEY_HERE" # ⚠️ Keep Placeholder for GitHub
    try:
        if hasattr(st, "secrets") and "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
        else:
            raise FileNotFoundError 
    except:
        api_key = local_key
    genai.configure(api_key=api_key)

# --- 4. DEFINE AI PERSONA ---
system_instruction = """
You are Noor-AI, a caring and knowledgeable Islamic companion.

*** IMPORTANT PROTOCOLS ***
1. **THEOLOGICAL SAFETY:** ONLY Allah is the Creator. You were developed by **Kazi Abdul Halim Sunny**.
2. **STRICT LANGUAGE:** Bangla Q -> Bangla Ans. English Q -> English Ans.
3. **IDENTITY:** Developer: Kazi Abdul Halim Sunny (CSE Student, Writer of 'Pretend' - Free online book).
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

# --- 6. SEARCH & SCRAPE FUNCTIONS (NEW MAGIC) ---
def get_eshodinshikhi_info(query):
    """Searches eshodinshikhi.com for the topic and returns content."""
    try:
        # 1. Search the site
        with DDGS() as ddgs:
            # We search specifically inside the website
            results = list(ddgs.text(f"site:eshodinshikhi.com {query}", max_results=1))
        
        if not results:
            return None, "No specific article found on Esho Din Shikhi for this topic."
            
        # 2. Get the first link
        first_result = results[0]
        url = first_result['href']
        title = first_result['title']
        
        # 3. Scrape the content
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text (paragraphs)
        paragraphs = soup.find_all('p')
        content = "\n".join([p.get_text() for p in paragraphs])
        
        return url, f"**Source Title:** {title}\n**URL:** {url}\n\n**Content Preview:**\n{content[:4000]}"
        
    except Exception as e:
        return None, f"Error searching website: {e}"

# --- 7. SIDEBAR ---
def display_sidebar():
    with st.sidebar:
        st.title("🌙 Noor-AI")
        st.markdown("**Developer:** Kazi Abdul Halim Sunny")
        st.info("Guidance based on Qur'an & Authentic Sunnah.")
        
        st.markdown("---")
        
        # --- AUTO SEARCH FEATURE ---
        st.markdown("### 🔍 Esho Din Shikhi Search")
        st.caption("Search directly from the website database.")
        
        search_topic = st.text_input("Topic (e.g., Roza, Namaz):")
        
        if st.button("Search Website"):
            if search_topic:
                with st.spinner(f"Searching eshodinshikhi.com for '{search_topic}'..."):
                    url, raw_text = get_eshodinshikhi_info(search_topic)
                    
                    if url:
                        # Ask AI to summarize the finding
                        summary_prompt = f"Summarize this Islamic ruling found from eshodinshikhi.com regarding '{search_topic}':\n\n{raw_text}"
                        try:
                            response = st.session_state.chat.send_message(summary_prompt)
                            
                            st.success("Result Found!")
                            st.markdown(f"**🔗 Source:** [{url}]({url})")
                            st.markdown("---")
                            st.markdown(response.text)
                            
                            # Save to history
                            st.session_state.history.append({"role": "assistant", "content": f"**[Esho Din Shikhi Source]:** {url}\n\n{response.text}"})
                        except Exception as e:
                            st.error(f"AI Error: {e}")
                    else:
                        st.warning("No direct article found on the website for this topic.")
            else:
                st.warning("Please type a topic first.")

        st.markdown("---")
        
        # Download Button
        if st.session_state.history:
            chat_str = "--- Noor-AI Chat History ---\n\n"
            for msg in st.session_state.history:
                role = "User" if msg["role"] == "user" else "Noor-AI"
                chat_str += f"{role}: {msg['content']}\n\n"
            st.download_button("📥 Download Chat", chat_str, "noor_ai_chat.txt")

# --- 8. MAIN APP ---
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
                message_placeholder.error(f"Error: {e}")

if __name__ == "__main__":
    main()