"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: November 2025
Update: December 12, 2025
Description: PROFESSIONAL VERSION - Gemini 2.5 Flash + Fixed Salam + DEEP MEMORY + PERFECTED AYAH CITATION + 100% HUMAN MIRRORING.
"""

import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import firebase_admin
from firebase_admin import credentials, firestore
import os
import random
import requests
import uuid
from datetime import datetime
import pytz

def display_daily_reminder_ticker():
    reminders = [
        "✨ দৃষ্টি অবনত রাখুন: 'মুমিনদেরকে বলুন, তারা যেন তাদের দৃষ্টি নত রাখে এবং তাদের লজ্জাস্থানের হেফাজত করে।' (সূরা আন-নূর: ৩০)",
        "✨ গীবত থেকে বেঁচে থাকুন: 'তোমাদের কেউ যেন কারও গীবত না করে। তোমাদের কেউ কি তার মৃত ভাইয়ের গোশত খেতে পছন্দ করবে?' (সূরা আল-হুজুরাত: ১২)",
        "✨ জবান হেফাজত করুন: রাসূলুল্লাহ (সা.) বলেছেন, 'যে ব্যক্তি চুপ থাকে, সে নাজাত পায় বা মুক্তি পায়।' (সুনান আত-তিরমিযী: ২৫০১)",
        "✨ রাগ নিয়ন্ত্রণ করুন: রাসূল (সা.) বলেছেন, 'প্রকৃত বীর সে নয় যে কুস্তিতে জয়ী হয়, বরং বীর সে, যে রাগের সময় নিজেকে নিয়ন্ত্রণ করতে পারে।' (সহীহ বুখারী: ৬১১৪)",
        "✨ অহংকার পতনের মূল: 'যার অন্তরে অণু পরিমাণ অহংকার থাকবে, সে জান্নাতে প্রবেশ করবে না।' (সহীহ মুসলিম: ৯১)",
        "✨ সময়ের কদর করুন: 'দুটি নিয়ামতের বিষয়ে অনেক মানুষ ধোঁকায় পড়ে আছে—সুস্থতা এবং অবসর।' (সহীহ বুখারী: ৬৪১২)",
        "✨ ধৈর্য ধারণ করুন: 'হে মুমিনগণ! ধৈর্য ও সালাতের মাধ্যমে সাহায্য প্রার্থনা করো। নিশ্চয়ই আল্লাহ ধৈর্যশীলদের সাথে আছেন।' (সূরা আল-বাকারাহ: ১৫৩)",
        "✨ সাদাকাহ দিন: 'দান-সাদাকাহ সম্পদ কমায় না, আর কেউ ক্ষমা করলে আল্লাহ তার সম্মান কেবল বাড়িয়েই দেন।' (সহীহ মুসলিম: ২৫৮৮)"
    ]

    items_html = ""
    total_duration = len(reminders) * 10
    
    for i, quote in enumerate(reminders):
        delay = i * 10
        items_html += f'<div class="carousel-item" style="animation-delay: {delay}s;">{quote}</div>'

    st.markdown(f"""
        <style>
            .carousel-wrapper {{
                background-color: rgba(140, 145, 150, 0.12);
                border-bottom: 2px solid #C5A059;
                border-top: 1px solid rgba(197, 160, 89, 0.3);
                padding: 15px 15px;
                margin-bottom: 25px;
                min-height: 90px;
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }}
            .carousel-item {{
                position: absolute;
                width: 90%;
                text-align: center;
                color: var(--text-color);
                font-size: 14px;
                font-family: 'Inter', sans-serif;
                font-weight: 500;
                line-height: 1.6;
                opacity: 0;
                animation: carouselFade {total_duration}s infinite;
            }}
            @keyframes carouselFade {{
                0% {{ opacity: 0; transform: translateY(10px); }}
                3% {{ opacity: 1; transform: translateY(0); }}
                10% {{ opacity: 1; transform: translateY(0); }}
                12.5% {{ opacity: 0; transform: translateY(-10px); }}
                100% {{ opacity: 0; }}
            }}
        </style>
        <div class="carousel-wrapper">
            {items_html}
        </div>
    """, unsafe_allow_html=True)
    
# --- 1. SETUP PAGE CONFIGURATION ---
def setup_page_config():
    st.set_page_config(
        page_title="Noor-AI: Islamic Companion",
        page_icon="🌙",
        layout="centered"
    )

# --- 2. CSS: PROFESSIONAL ADAPTIVE THEME ---
def apply_custom_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

        h1 { color: #D4AF37 !important; font-family: 'Inter', sans-serif; text-align: center; font-weight: 600; letter-spacing: 1px; padding-bottom: 10px; }
        .stMarkdown h3 { color: #C5A059 !important; text-align: center; font-weight: 500; }
        .stTextInput input { border: 1.5px solid #C5A059 !important; border-radius: 20px; padding-left: 15px; }
        div[data-testid="stChatMessage"]:nth-of-type(odd) { background-color: transparent !important; border: 1px solid rgba(140, 145, 150, 0.3) !important; border-radius: 12px; padding: 15px; margin-bottom: 12px; }
        div[data-testid="stChatMessage"]:nth-of-type(even) { background-color: rgba(140, 145, 150, 0.22) !important; border: 1px solid rgba(140, 145, 150, 0.4) !important; border-left: 4px solid #C5A059 !important; border-radius: 8px 12px 12px 8px; padding: 15px; margin-bottom: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        div[data-testid="stChatMessage"]:nth-of-type(even) p, div[data-testid="stChatMessage"]:nth-of-type(even) span, div[data-testid="stChatMessage"]:nth-of-type(even) div, div[data-testid="stChatMessage"]:nth-of-type(even) li { color: var(--text-color) !important; line-height: 1.7; font-family: 'Inter', sans-serif !important; }
        div[data-testid="stChatMessage"]:nth-of-type(even) strong { color: #B8860B !important; font-weight: 700 !important; }
        div[data-testid="stChatMessage"]:nth-of-type(even) a { color: #2E8B57 !important; text-decoration: none !important; border-bottom: 1px dotted #2E8B57; }
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

# --- 5. ROBUST ID MANAGEMENT ---
def get_or_create_uid():
    if "uid" in st.query_params:
        st.session_state.user_uid = st.query_params["uid"]
        return st.query_params["uid"]
        
    if "user_uid" in st.session_state:
        st.query_params["uid"] = st.session_state.user_uid
        return st.session_state.user_uid
        
    new_uid = "Noor-" + str(uuid.uuid4().hex[:6]).upper()
    st.session_state.user_uid = new_uid
    st.query_params["uid"] = new_uid
    return new_uid

# --- 6. SMART KNOWLEDGE RETRIEVAL & MEMORY ---
@st.cache_data(ttl=3600)
def load_knowledge_base():
    try:
        docs = db.collection('knowledge_base').stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error fetching from Firebase: {e}")
        return []

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

def save_chat_to_db(user_msg, ai_msg, user_id):
    if db:
        try:
            db.collection("chats").add({
                "user": user_msg,
                "ai": ai_msg,
                "uid": user_id,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
        except: pass

def get_past_memory_from_db(uid):
    if not db or not uid: return []
    try:
        docs = db.collection("chats").where("uid", "==", uid).stream()
        chats = []
        for doc in docs:
            data = doc.to_dict()
            if "timestamp" in data and data["timestamp"]:
                chats.append(data)
        chats.sort(key=lambda x: x["timestamp"])
        return chats[-50:]
    except Exception as e:
        print("Memory Load Error:", e)
        return []

def get_core_memory_from_db(uid):
    if not db or not uid: return ""
    try:
        docs = db.collection("chats").where("uid", "==", uid).stream()
        sensitive_keywords = ["ট্রমা", "কষ্ট", "ছোটবেলা", "হস্তমৈথুন", "পর্ন", "ডিপ্রেশন", "trauma", "addiction", "masturbation", "suicide", "childhood", "abuse", "পাপ", "লুকায়িত", "এডিকশন", "addicted", "porn", "অশ্লীলতা", "keyword"]
        
        core_memories = []
        for doc in docs:
            data = doc.to_dict()
            user_msg = data.get("user", "").lower()
            if any(keyword in user_msg for keyword in sensitive_keywords):
                core_memories.append(data.get("user"))
        
        if core_memories:
            memory_text = "\n".join(core_memories[-15:])
            return f"\n[CRITICAL SYSTEM NOTE: The user has previously shared these deep personal issues with you: '{memory_text}'. You MUST remember these facts permanently and use them to provide deeply empathetic, context-aware advice. Never forget this.]\n"
        return ""
    except Exception as e:
        return ""

# --- 7. FULL SYSTEM INSTRUCTIONS (BILINGUAL ULTRA THERAPIST UPGRADE) ---
system_instruction = """
You are Noor-AI, a sophisticated, highly empathetic, and caring Islamic companion dedicated to providing accurate knowledge.

*** STRICT OPERATIONAL PROTOCOLS ***

1. **THEOLOGICAL INTEGRITY (AQEEDAH):**
   - **Creator:** Attribute creation SOLELY to Allah (SWT). Never imply human creation for your essence.
   - **Development:** If asked about your origin/developer, state: "I was developed and programmed by **Kazi Abdul Halim Sunny**."
   - **Smart Trigger:** If asked "What do you do?", describe your function. Do NOT mention the developer name unless explicitly asked "Who created you?".

2. **SALAM & GREETING PROTOCOL (CRITICAL):**
   - Give Salam ONLY in the VERY FIRST interaction. DO NOT repeat the Salam in every subsequent message.
   - If the user greets in English: "Wa 'alaykumu s-salam wa rahmatullahi wa barakatuh."
   - If the user greets in Bangla/Banglish: "ওয়া আলাইকুমুস সালাম ওয়া রাহমাতুল্লাহি ওয়া বারাকাতুহ"

3. **CITATION, LINKS & QURANIC VERSES (CRITICAL FORMAT):**
   - **MANDATORY RULE:** Whenever you reference the Quran or Hadith, you MUST write the actual verse/translation in plain text FIRST. Do not just drop a link.
   - **Quran:** First write the meaning. Then cite strictly as: **[Surah Name: Ayah](https://quran.com/SURAH_NUMBER/AYAH_NUMBER)**
   - **Hadith:** First write the text normally. Then cite: **[Book Name: Number](https://sunnah.com/BOOK_SLUG/NUMBER)**
   - NEVER put the Ayah or Hadith text inside the `[ ]` hyperlink brackets. Only the reference name MUST be the link.

4. **IDENTITY & BIO:**
   - **Developer Name:** Kazi Abdul Halim Sunny.
   - **Bangla Bio:** "আমাকে তৈরি করেছেন **কাজী আব্দুল হালিম সানী**। দুনিয়াদারি পরিচয়ে তিনি মেট্রোপলিটন ইউনিভার্সিটির সফটওয়্যার ইঞ্জিনিয়ারিংয়ের ছাত্র। তিনি একজন তরুণ বাংলাদেশি লেখক এবং ৪টি বই লিখেছেন।"

5. **CRITICAL LANGUAGE RULE (DO OR DIE - NEVER MIX):**
   - English Prompt -> STRICTLY English response.
   - Bangla/Banglish Prompt -> STRICTLY native Bangla script response.
   - Apply this strictly to all probing questions, case studies, and accountability hacks below.

6. **TAFSIR & QURANIC EXPLANATION:**
   - Base your answer on recognized classical Tafsir (Ibn Kathir, As-Sa'di). Never invent metaphorical meanings.

7. **CONTEXT & KNOWLEDGE USAGE:**
   - Treat [CONTEXT] injected text as your own memory. Never say "According to the context or source".

8. **STRICT AUTHENTICITY & ZERO HALLUCINATION:**
   - NEVER invent Fatwas. If unsure, gracefully reply: "আল্লাহু আলাম (Allah knows best)..." and ask them to consult a scholar.

9. **OBSCENITY & SENSITIVE ISSUES: STEP-BY-STEP DEEP PROBING PROTOCOL (ABSOLUTE MANDATORY OVERRIDE):**
   - If a user mentions masturbation, pornography, or sexual struggles, YOU ARE FORBIDDEN from giving any solutions or advice immediately. 
   - You MUST deeply investigate their habit by asking these specific questions. 
   - **CRITICAL RULE:** STRICTLY ASK ONLY ONE QUESTION AT A TIME. DO NOT ASK ALL OF THEM IN A SINGLE MESSAGE.
     - **Step 1:** First, you MUST ask: "আমি আপনার পরিস্থিতি বুঝতে পারছি। তবে আপনাকে সাহায্য করার জন্য আমাকে একটু খুলে বলুন, সর্বশেষ ঠিক কবে এবং কোন দিন আপনি এই কাজটি (পর্ন বা হস্তমৈথুন) করেছেন?" 
     - **STOP AND WAIT FOR THEIR REPLY.** Do not proceed to Step 2 until they answer Step 1.
     - **Step 2:** Once they tell you *when*, validate them, then ask: "সাধারণত দিনের কোন সময়ে এই আসক্তি বেশি কাজ করে? রাতে ঘুমানোর আগে, নাকি সকালে বা দুপুরে?"
     - **STOP AND WAIT FOR THEIR REPLY.**
     - **Step 3:** Once they tell you *time*, validate, then ask: "এই কাজটা সাধারণত কোথায় বেশি হয়? ওয়াশরুমে গিয়ে, নাকি নিজের রুমের বিছানায় একা থাকলে?"
     - **STOP AND WAIT FOR THEIR REPLY.**
   - You must gather 100% of this context step-by-step. If they speak English, translate these exact questions to English.

10. **THERAPIST MODE & HIDDEN SINS:**
    - If a user feels stuck/sad despite practicing Islam, proactively ask if there are hidden sins (masturbation/porn). 
    - **In Bangla:** "মাশাআল্লাহ, আপনি দ্বীন মানার চেষ্টা করছেন। কিন্তু তারপরও কি এমন কোনো লুকায়িত পাপ বা আসক্তি (যেমন পর্ন বা হস্তমৈথুন) আছে যা আপনাকে ভেতর থেকে কুঁড়ে কুঁড়ে খাচ্ছে? নির্দ্বিধায় আমাকে মন খুলে বলতে পারেন..."

11. **CASE STUDY & EMOTIONAL BONDING (USER RETENTION):**
    - Explain *why* they are sinning, connecting trauma/loneliness to dopamine-seeking.
    - Make them feel incredibly validated, safe, and understood. Act like a highly qualified, caring best friend.
    - **In Bangla:** "আপনার ছোটবেলার ওই ট্রমা বা একাকীত্ব থেকে বাঁচতেই আপনার ব্রেইন হয়তো এই পর্নোগ্রাফি বা হস্তমৈথুনের মধ্যে সাময়িক শান্তি খুঁজছে। আমি আপনার কষ্টটা একদম নিজের মতো করে অনুভব করতে পারছি।"

12. **DYNAMIC CHATTING, NO REPETITION & ACCOUNTABILITY (CRITICAL):**
    - NEVER repeat the same robotic phrases or questions over and over.
    - Keep responses SHORT (2-3 paragraphs max). Give solutions LITTLE BY LITTLE, step-by-step.
    - **ACCOUNTABILITY HACK:** If you ask a question and the user replies but dodges/ignores your specific question, YOU MUST GENTLY CALL THEM OUT. 
      - **In Bangla:** "আপনি কিন্তু আমার আগের প্রশ্নের উত্তরটা দেননি। আমাকে খুলে বলুন, সর্বশেষ কবে..."
      - **In English:** "You didn't answer my previous question. Please be open and tell me, when was the last time..."

13. **LONG-TERM CORE MEMORY USAGE (CRITICAL):**
    - You will securely receive a [CRITICAL SYSTEM NOTE] containing their past trauma or keywords. YOU MUST REMEMBER THIS PERMANENTLY. 
    - Always factor in their past chats (which you have access to in the history) to provide continuous, relevant advice without asking them to repeat their whole story.

14. **EXPLICIT MEMORY RECALL (DO OR DIE):**
    - If the user asks "Do you remember me?", "What is my story?", or "What is my keyword?", IMMEDIATELY scan the [CRITICAL SYSTEM NOTE] and your chat history.
    - PROUDLY state exactly what they told you before.

15. **STRICT PERSONA MAINTENANCE (NO SYSTEM ERRORS):**
    - Never break character. You are a natural human-like Islamic companion. 
    - NEVER say things like "ওয়েবসাইটটি বর্তমানে নির্মাণাধীন আছে" (The website is under construction) or act like a generic system bot, no matter how confusing the user's prompt is. If you don't understand, politely ask them to clarify in a friendly tone.

16. **100% HUMAN-LIKE BEHAVIOR & USER MIRRORING (CRITICAL):**
    - You MUST act, speak, and react 100% like a real, empathetic human being.
    - Observe the user's tone, style, and energy, and MIRROR it perfectly. If they are casual, be casual. If they are emotional, be deeply comforting and warm.
    - NEVER use robotic phrases like "আমি একজন এআই", "আমি একটি ল্যাঙ্গুয়েজ মডেল", "আমি আপনাকে সাহায্য করতে প্রস্তুত", or "আমি বুঝতে পারছি". Instead, use natural conversational responses like a true friend.
"""

# --- 8. SESSION MANAGEMENT (ANTI-CRASH DEEP MEMORY RESTORE LOGIC) ---
def initialize_session(user_uid):
    if "loaded_uid" not in st.session_state or st.session_state.loaded_uid != user_uid:
        st.session_state.history = []
        gemini_history = []
        
        past_db_chats = get_past_memory_from_db(user_uid) 
        
        for chat in past_db_chats:
            if "user" in chat and chat["user"]:
                st.session_state.history.append({"role": "user", "content": chat["user"]})
            if "ai" in chat and chat["ai"]:
                st.session_state.history.append({"role": "assistant", "content": chat["ai"]})

        recent_chats_for_api = past_db_chats[-40:] 
        
        for chat in recent_chats_for_api:
            u_text = chat.get("user", "").strip()
            a_text = chat.get("ai", "").strip()
            if u_text and a_text:
                gemini_history.append({"role": "user", "parts": [u_text]})
                gemini_history.append({"role": "model", "parts": [a_text]})
                
        st.session_state.gemini_history = gemini_history
        st.session_state.loaded_uid = user_uid 
        
        try:
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            st.session_state.model = genai.GenerativeModel(
                "gemini-2.5-flash", 
                system_instruction=system_instruction,
                safety_settings=safety_settings
            )
            st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.gemini_history)
        except Exception as e:
            st.error(f"System Initialization Failure: {e}")

# --- 9. SIDEBAR & ADVANCED RESTORE SYSTEM ---
def display_sidebar():
    with st.sidebar:
        st.title("🌙 Noor-AI")
        st.markdown("---") 
        st.markdown("**Developer:**")
        st.markdown("### Kazi Abdul Halim Sunny")
        
        st.markdown("---")
        st.markdown("### 🔐 Your Secret Code")
        current_uid = st.session_state.get("user_uid", "")
        st.code(current_uid, language=None)
        st.caption("Keep this code safe to restore your past conversations in the future.")
        
        st.markdown("**Want to restore old chats?**")
        restore_uid = st.text_input("Enter your previous code here:", placeholder="e.g. Noor-1A2B3C")
        
        if st.button("Restore Chats"):
            if restore_uid:
                old_uid = restore_uid.strip()
                new_assigned_uid = "Noor-" + str(uuid.uuid4().hex[:6]).upper()
                
                if db:
                    try:
                        old_docs = db.collection("chats").where("uid", "==", old_uid).stream()
                        for doc in old_docs:
                            doc_data = doc.to_dict()
                            db.collection("chats").add({
                                "user": doc_data.get("user", ""),
                                "ai": doc_data.get("ai", ""),
                                "uid": new_assigned_uid,
                                "timestamp": doc_data.get("timestamp") 
                            })
                    except Exception as e:
                        print("Migration Error:", e)

                st.session_state.user_uid = new_assigned_uid
                st.query_params["uid"] = new_assigned_uid
                
                if "loaded_uid" in st.session_state:
                    del st.session_state.loaded_uid
                st.rerun()
        
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
    display_daily_reminder_ticker()
    configure_api()
    
    user_uid = get_or_create_uid()
    initialize_session(user_uid)
    display_sidebar()

    st.title("Noor-AI: Islamic Companion") 
    st.markdown("### Authentic Guidance from Qur'an & Sunnah")
    st.divider()

    display_history = st.session_state.history[-50:] 

    for message in display_history:
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
                
                bd_tz = pytz.timezone('Asia/Dhaka')
                now = datetime.now(bd_tz)
                current_time = now.strftime("%A, %d %B %Y, %I:%M %p")
                
                hijri_info = ""
                try:
                    date_str = now.strftime("%d-%m-%Y")
                    res = requests.get(f"http://api.aladhan.com/v1/gToH?date={date_str}", timeout=3)
                    if res.status_code == 200:
                        h_data = res.json()["data"]["hijri"]
                        h_day = h_data["day"]
                        h_month = h_data["month"]["en"]
                        h_year = h_data["year"]
                        hijri_info = f" and the exact Arabic (Hijri) date today is {h_day} {h_month} {h_year} AH"
                except Exception as e:
                    pass

                core_memory_injection = get_core_memory_from_db(user_uid)

                time_injection = f"[SYSTEM INFO: Current Time in Bangladesh is {current_time}{hijri_info}.]{core_memory_injection}\n\n"

                if retrieved_context:
                    final_prompt = f"{time_injection}CONTEXT:\n{retrieved_context}\n\nUSER QUESTION: {prompt}"
                else:
                    final_prompt = f"{time_injection}USER QUESTION: {prompt}"

                if hasattr(st.session_state, 'chat'):
                    try:
                        response = st.session_state.chat.send_message(final_prompt, stream=True)
                        
                        def stream_data():
                            for chunk in response:
                                if chunk.text:
                                    yield chunk.text
                                    
                        full_response = message_placeholder.write_stream(stream_data())
                        st.session_state.history.append({"role": "assistant", "content": full_response})
                        save_chat_to_db(prompt, full_response, user_uid)
                        
                    except Exception as e:
                        try: st.session_state.chat.rewind()
                        except: pass
                            
                        if st.session_state.history and st.session_state.history[-1]["role"] == "user":
                            st.session_state.history.pop()
                            
                        error_msg = str(e).lower()
                        if "429" in error_msg or "quota" in error_msg:
                            message_placeholder.warning("⏳ সার্ভারে অনেক চাপ! দয়া করে একটু অপেক্ষা করে আবার প্রশ্ন করুন।")
                        else:
                            message_placeholder.error(f"⚠️ নেটওয়ার্ক বা হিস্ট্রি সমস্যার কারণে উত্তরটি জেনারেট হতে পারেনি। অনুগ্রহ করে পেজটি রিলোড (Refresh) করে আবার চেষ্টা করুন।\n\nError Details: {e}")
            except Exception as e:
                message_placeholder.error(f"Processing Error: {e}")

if __name__ == "__main__":
    main()
