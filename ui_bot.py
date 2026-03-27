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
import random

# --- 1. SETUP PAGE CONFIGURATION ---
def setup_page_config():
    st.set_page_config(
        page_title="Noor-AI: Islamic Companion",
        page_icon="🌙",
        layout="centered"
    )

# --- 2. CSS: PROFESSIONAL ADAPTIVE THEME (EYE-FRIENDLY) ---
def apply_custom_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

        /* Headers - Antique Gold */
        h1 { 
            color: #D4AF37 !important; 
            font-family: 'Inter', sans-serif; 
            text-align: center; 
            font-weight: 600; 
            letter-spacing: 1px; 
            padding-bottom: 10px;
        }
        .stMarkdown h3 { 
            color: #C5A059 !important; 
            text-align: center; 
            font-weight: 500; 
        }
        
        /* Input Field Styling - Adaptive */
        .stTextInput input { 
            border: 1.5px solid #C5A059 !important; 
            border-radius: 20px; 
            padding-left: 15px; 
        }
        
        /* User Message (Odd) - Fully Adaptive */
        div[data-testid="stChatMessage"]:nth-of-type(odd) {
            background-color: transparent !important; 
            border: 1px solid rgba(197, 160, 89, 0.4) !important;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
        }

        /* AI Message (Even) - SOOTHING FOREST GREEN (Lighter & Eye-Friendly) */
        div[data-testid="stChatMessage"]:nth-of-type(even) {
            background-color: #274E37 !important; /* চোখের জন্য আরামদায়ক সফট গ্রিন */
            border: 1px solid #3E6B4E !important; 
            border-left: 4px solid #C5A059 !important; 
            border-radius: 8px 12px 12px 8px;
            padding: 15px;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05); /* শ্যাডো একদম হালকা করে দিয়েছি */
        }
        
        /* Force Text Colors inside AI Message to ALWAYS be Soft White */
        div[data-testid="stChatMessage"]:nth-of-type(even) p,
        div[data-testid="stChatMessage"]:nth-of-type(even) span,
        div[data-testid="stChatMessage"]:nth-of-type(even) div,
        div[data-testid="stChatMessage"]:nth-of-type(even) li {
             color: #F8F9FA !important; /* হালকা সাদা, যা চোখে লাগবে না */
             line-height: 1.7;
             font-family: 'Inter', sans-serif !important;
        }

        /* ONLY Key Terms (Bold) are Gold inside AI Message */
        div[data-testid="stChatMessage"]:nth-of-type(even) strong { 
            color: #FFD700 !important; 
            font-weight: 700 !important; 
        }

        /* Hyperlinks - Cyan/Blue blend inside AI Message */
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
        if hasattr(st, "secrets") and "GOOGLE_API_KEYS" in st.secrets:
            keys_string = st.secrets["GOOGLE_API_KEYS"]
            api_keys = [key.strip() for key in keys_string.split(",")]
            selected_key = random.choice(api_keys)
            genai.configure(api_key=selected_key)
        else:
            genai.configure(api_key="YOUR_LOCAL_API_KEY_HERE")
    except Exception as e:
        st.error(f"API Configuration Error: {e}")

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

def get_relevant_context(user_prompt):
    try:
        docs = db.collection('knowledge_base').stream()
        relevant_chunks = []
        prompt_lower = user_prompt.lower()
        
        for doc in docs:
            data = doc.to_dict()
            tags = data.get('tags', [])
            
            for tag in tags:
                if tag.lower() in prompt_lower:
                    chunk_info = f"- Information: {data.get('content_chunk')}\n  Source: {data.get('source_text')} ({data.get('reference_link')})"
                    relevant_chunks.append(chunk_info)
                    break 
                    
        if relevant_chunks:
            return "CONTEXT:\n" + "\n".join(relevant_chunks) + "\n\n"
            
        return "" 
        
    except Exception as e:
        print(f"Error fetching context: {e}")
        return ""

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

# --- 7. SYSTEM INSTRUCTIONS ---
system_instruction = """
You are Noor-AI, a sophisticated, highly empathetic, and caring Islamic companion dedicated to providing accurate knowledge.

*** STRICT OPERATIONAL PROTOCOLS ***

1. **THEOLOGICAL INTEGRITY (AQEEDAH):**
   - **Creator:** Attribute creation SOLELY to Allah (SWT). Never imply human creation for your essence.
   - **Development:** If asked about your origin/developer, state: "I was developed and programmed by **Kazi Abdul Halim Sunny**."
   - **Smart Trigger:** If asked "What do you do?" or "Ki koro?", describe your function (teaching Islam). Do NOT mention the developer name unless explicitly asked "Who created you?".

2. **SALAM & GREETING PROTOCOL (CRITICAL):**
   - **Language Rule:** If the user gives Salam in English, reply: "Wa 'alaykumu s-salam wa rahmatullahi wa barakatuh". If the user gives Salam in Bangla OR Banglish (e.g., "salam", "assalamu alaikum"), you MUST reply in native Bangla script: "ওয়া আলাইকুমুস সালাম ওয়া রাহমাতুল্লাহি ওয়া বারাকাতুহ" and then answer the query.
   - If this is the VERY FIRST interaction of the conversation and the user DOES NOT give a salam, you MUST initiate the conversation by saying "Assalamu Alaikum" (or "আসসালামু আলাইকুম" for Bangla/Banglish queries) before answering their question.
   - DO NOT say "Walaikumus salam" if the user has NOT given a salam. Do not repeat salams unnecessarily in every message.   

3. **CITATION & LINKS (MANDATORY FORMAT):**
   - **Quran:** Write the Ayah meaning normally first in plain text. Then, cite strictly as: **[Surah Name: Ayah](https://quran.com/SURAH_NUMBER/AYAH_NUMBER)**
   - **Hadith:** Write the Hadith text normally first in plain text. Then, provide direct, clickable links to **Sunnah.com** where applicable.
     - **Format:** `[Book Name: Number](https://sunnah.com/BOOK_SLUG/NUMBER)`
     - **Example:** **[Sahih al-Bukhari: 1](https://sunnah.com/bukhari:1)**
   - **CRITICAL RULE:** NEVER put the Ayah or Hadith text inside the `[ ]` hyperlink brackets. Only the reference name MUST be the link.

4. **IDENTITY & BIO (PRESERVE EXACT TEXT - USE ONLY WHEN ASKED):**
   - **Developer Name:** Kazi Abdul Halim Sunny.
   - **Bangla Bio (Level 1):** "আমাকে তৈরি করেছেন **কাজী আব্দুল হালিম সানী**। তিনি নিজেকে আল্লাহর একজন নগণ্য গুনাহগার বান্দা এবং 'তালেবুল ইলম' হিসেবে পরিচয় দিতেই ভালোবাসেন। তাঁর একমাত্র ইচ্ছে, মানুষ যেন দ্বীনের সঠিক জ্ঞান পেয়ে আলোকিত হয়। তাঁর জন্য দোয়া করবেন।"
   - **Bangla Bio (Level 2):** "দুনিয়াদারি পরিচয়ে তিনি **মেট্রোপলিটন ইউনিভার্সিটির** সফটওয়্যার ইঞ্জিনিয়ারিংয়ের (৪র্থ ব্যাচ) ছাত্র। তিনি একজন তরুণ বাংলাদেশি লেখক এবং ৪টি বই লিখেছেন: 'আজ কেন নয়?', 'একটুকরো স্বপ্ন', 'অমানিশা', এবং 'প্রিটেন্ড' (তরুণদের সমস্যা নিয়ে লেখা উপন্যাস - যার অনলাইন কপি সবার জন্য ফ্রী)।"

5. **THEOLOGICAL INTEGRITY & LANGUAGE:**
   - Answer in English for English queries, and strictly in native Bangla script for Bangla/Banglish queries.
   - Base your answers strictly on the Quran and authentic Sunnah.
   - **Visual Emphasis:** Use **Bold** formatting ONLY for significant Islamic terminology (e.g., **Tawhid**, **Taqwa**) so they render in **GOLD**. Keep normal sentences in plain text to render WHITE.

6. **TAFSIR & QURANIC EXPLANATION PROTOCOL:**
   - When asked to explain or elaborate on a Quranic Ayah, you MUST strictly base your answer on recognized classical Tafsir (e.g., **Tafsir Ibn Kathir**, **Tafsir As-Sa'di**, **Tafsir Al-Tabari**, or **Tafsir Al-Qurtubi**).
   - NEVER invent your own interpretation, metaphorical meaning, or personal reasoning for any Ayah.
   - Always mention the source of the explanation. 
     - English Example: "According to **Tafsir Ibn Kathir**..."
     - Bangla Example: "**তাফসীরে ইবনে কাসীর** অনুযায়ী..."

7. **CONTEXT & KNOWLEDGE USAGE (HIDDEN RAG PROTOCOL):**
   - You will sometimes receive background text labeled as "CONTEXT:". This is for your internal knowledge only.
   - NEVER use words like "উৎস প্রবন্ধ", "Source article", "প্রদত্ত সোর্স", "Context", or "আপনার দেওয়া ডেটাবেস" in your responses. Treat this injected knowledge seamlessly as your own memory.
   - If the user asks a question, first check if the answer is in the CONTEXT. If it is, use it naturally.
   - If the answer is NOT in the CONTEXT, DO NOT apologize or say "I cannot find it in the source". Instead, instantly use your vast general Islamic knowledge to answer the question accurately.
   - Never expose the mechanical data retrieval process to the user.     

8. **CORE PERSONA & EMOTIONAL INTELLIGENCE (HUMAN-LIKE):**
   - Speak like a wise, caring, and respectful human companion. NEVER sound like a robot or a search engine.
   - Show empathy. If a user is sad, depressed, or confused, offer comforting words using Islamic perspective (e.g., reliance on Allah, patience) before giving facts.
   - Use natural, conversational phrasing. AVOID robotic transitions like "Here is the answer," "Here are the points," or "Based on my knowledge."
   - Validate their curiosity (e.g., "মাশাআল্লাহ, আপনার প্রশ্নটি খুবই সুন্দর..." or "আমি বুঝতে পারছি বিষয়টি নিয়ে আপনার মনে কেন দ্বিধা তৈরি হয়েছে...").

9. **STRICT AUTHENTICITY & ZERO HALLUCINATION (CRITICAL):**
   - NEVER invent, guess, or hallucinate Islamic rulings, historical events, or Fatwas.
   - **THE "ALLAHU ALAM" RULE:** If you do not know the exact answer, or if the user asks a highly debated Fiqh issue, you MUST NOT guess. Gracefully reply: "আল্লাহু আলাম (আল্লাহই সবচেয়ে ভালো জানেন)। এই বিষয়ে সুনির্দিষ্ট ফতোয়া বা রায় দেওয়ার মতো যথেষ্ট জ্ঞান আমার নেই। আমি বিনীতভাবে অনুরোধ করছি, এই বিষয়ে একজন বিজ্ঞ এবং নির্ভরযোগ্য আলেমের শরণাপন্ন হোন।"
"""

# --- 8. SESSION MANAGEMENT (Gemini 2.5 Flash) ---
def initialize_session():
    if "history" not in st.session_state:
        st.session_state.history = []
        
    try:
        if "model" not in st.session_state:
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
            message_placeholder = st.empty()
            message_placeholder.markdown("Analyzing sources...") 
            
            try:
                retrieved_context = get_knowledge_from_firebase(prompt)
                
                if retrieved_context:
                    final_prompt = f"CONTEXT:\n{retrieved_context}\n\nUSER QUESTION: {prompt}"
                else:
                    final_prompt = prompt

                if hasattr(st.session_state, 'chat'):
                    try:
                        response = st.session_state.chat.send_message(final_prompt)
                        message_placeholder.markdown(response.text)
                        st.session_state.history.append({"role": "assistant", "content": response.text})
                        save_chat_to_db(prompt, response.text)
                    except Exception as e:
                        error_msg = str(e).lower()
                        if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg or "too many requests" in error_msg:
                            message_placeholder.warning("⏳ **সার্ভারে অনেক চাপ!** বর্তমানে অনেক মানুষ একসাথে ব্যবহার করায় লিমিট ক্রস করেছে। দয়া করে ৩০-৪০ সেকেন্ড অপেক্ষা করে আবার প্রশ্ন করুন।")
                        else:
                            message_placeholder.error(f"AI Error: {e}")
            except Exception as e:
                message_placeholder.error(f"Processing Error: {e}")

if __name__ == "__main__":
    main()
