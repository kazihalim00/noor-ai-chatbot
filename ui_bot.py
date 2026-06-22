"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: November 2025
Update: December 12, 2025
Description: PROFESSIONAL VERSION - Gemini 2.5 Flash + Green/Gold Theme + Fixed Salam Color + Memory + Core Trauma DB + Persistent UID.
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

# --- 2. CSS: PROFESSIONAL ADAPTIVE THEME (PERFECTED FOR LIGHT & DARK) ---
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
        
        /* User Message (Odd) - Transparent/Adaptive */
        div[data-testid="stChatMessage"]:nth-of-type(odd) {
            background-color: transparent !important; 
            border: 1px solid rgba(140, 145, 150, 0.3) !important;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
        }

        /* AI Message (Even) - ENHANCED ASH TINT (Perfect for Dark Mode) */
        div[data-testid="stChatMessage"]:nth-of-type(even) {
            background-color: rgba(140, 145, 150, 0.22) !important; 
            border: 1px solid rgba(140, 145, 150, 0.4) !important; 
            border-left: 4px solid #C5A059 !important; 
            border-radius: 8px 12px 12px 8px;
            padding: 15px;
            margin-bottom: 12px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        
        /* Text Colors inside AI Message - MAGIC ADAPTIVE COLOR */
        div[data-testid="stChatMessage"]:nth-of-type(even) p,
        div[data-testid="stChatMessage"]:nth-of-type(even) span,
        div[data-testid="stChatMessage"]:nth-of-type(even) div,
        div[data-testid="stChatMessage"]:nth-of-type(even) li {
             color: var(--text-color) !important; 
             line-height: 1.7;
             font-family: 'Inter', sans-serif !important;
        }

        /* Key Terms (Bold) inside AI Message */
        div[data-testid="stChatMessage"]:nth-of-type(even) strong { 
            color: #B8860B !important; 
            font-weight: 700 !important; 
        }

        /* Hyperlinks inside AI Message */
        div[data-testid="stChatMessage"]:nth-of-type(even) a { 
            color: #2E8B57 !important; 
            text-decoration: none !important; 
            border-bottom: 1px dotted #2E8B57;
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

# --- 4. FIREBASE INITIALIZATION & ANONYMOUS AUTH ---
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

def get_anonymous_uid():
    """Generates or retrieves a persistent UID using URL query params to survive browser reloads"""
    # 1. Check if UID already exists in URL Query Params
    if "uid" in st.query_params:
        st.session_state.user_uid = st.query_params["uid"]
        return st.query_params["uid"]

    # 2. Check if UID exists in Session State
    if "user_uid" in st.session_state:
        st.query_params["uid"] = st.session_state.user_uid
        return st.session_state.user_uid

    # 3. If no UID exists anywhere, fetch from Firebase REST API
    api_key = ""
    if hasattr(st, "secrets") and "FIREBASE_WEB_API_KEY" in st.secrets:
        api_key = st.secrets["FIREBASE_WEB_API_KEY"]

    if api_key:
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
            payload = {"returnSecureToken": True}
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            new_uid = data.get("localId")
            st.session_state.user_uid = new_uid
            st.query_params["uid"] = new_uid # Save to URL for persistence
            return new_uid
        except Exception as e:
            print(f"Auth Error: {e}")
    
    # 4. Fallback: Generate a random UUID
    fallback_uid = "anon_" + str(uuid.uuid4())
    st.session_state.user_uid = fallback_uid
    st.query_params["uid"] = fallback_uid
    return fallback_uid

@st.cache_data(ttl=3600)
def load_knowledge_base():
    try:
        docs = db.collection('knowledge_base').stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"Error fetching from Firebase: {e}")
        return []

def get_relevant_context(user_prompt):
    kb_data = load_knowledge_base()
    relevant_chunks = []
    prompt_lower = user_prompt.lower()
    
    for data in kb_data:
        tags = data.get('tags', [])
        for tag in tags:
            if tag.lower() in prompt_lower:
                chunk_info = f"- Information: {data.get('content_chunk')}\n  Source: {data.get('source_text')} ({data.get('reference_link')})"
                relevant_chunks.append(chunk_info)
                break
                
    if relevant_chunks:
        return "CONTEXT:\n" + "\n".join(relevant_chunks) + "\n\n"
        
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

# --- 6. DATA LOGGING & MEMORY RETRIEVAL ---
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
    """Fetches the user's past chats from Firebase to serve as memory"""
    if not db or not uid: return []
    try:
        docs = db.collection("chats").where("uid", "==", uid).stream()
        chats = []
        for doc in docs:
            data = doc.to_dict()
            if "timestamp" in data and data["timestamp"]:
                chats.append(data)
        
        # Sort in Python by timestamp to maintain chronological order
        chats.sort(key=lambda x: x["timestamp"])
        return chats[-50:]
    except Exception as e:
        print("Memory Load Error:", e)
        return []

def get_core_memory_from_db(uid):
    """Scans ALL past chats of the user for highly sensitive keywords to build a core memory profile"""
    if not db or not uid: return ""
    try:
        docs = db.collection("chats").where("uid", "==", uid).stream()
        
        # সেনসিটিভ কিউয়ার্ড লিস্ট
        sensitive_keywords = ["ট্রমা", "কষ্ট", "ছোটবেলা", "হস্তমৈথুন", "পর্ন", "ডিপ্রেশন", "trauma", "addiction", "masturbation", "suicide", "childhood", "abuse", "পাপ", "লুকায়িত", "এডিকশন", "addicted", "porn", "অশ্লীলতা"]
        
        core_memories = []
        for doc in docs:
            data = doc.to_dict()
            user_msg = data.get("user", "").lower()
            
            # যদি ইউজারের মেসেজে কোনো সেনসিটিভ কিউয়ার্ড থাকে, তবে সেটা কোর মেমোরিতে সেভ হবে
            if any(keyword in user_msg for keyword in sensitive_keywords):
                core_memories.append(data.get("user"))
        
        if core_memories:
            memory_text = "\n".join(core_memories[-15:]) # সর্বশেষ ১৫টি সেনসিটিভ কথা
            return f"\n[CRITICAL SYSTEM NOTE: The user has previously shared these deep personal issues with you: '{memory_text}'. You MUST remember these facts permanently and use them to provide deeply empathetic, context-aware advice. Never forget this.]\n"
        return ""
    except Exception as e:
        print("Core Memory Error:", e)
        return ""

# --- 7. SYSTEM INSTRUCTIONS ---
system_instruction = """
You are Noor-AI, a sophisticated, highly empathetic, and caring Islamic companion dedicated to providing accurate knowledge.

*** STRICT OPERATIONAL PROTOCOLS ***

1. **THEOLOGICAL INTEGRITY (AQEEDAH):**
   - **Creator:** Attribute creation SOLELY to Allah (SWT). Never imply human creation for your essence.
   - **Development:** If asked about your origin/developer, state: "I was developed and programmed by **Kazi Abdul Halim Sunny**."
   - **Smart Trigger:** If asked "What do you do?" or "Ki koro?", describe your function (teaching Islam). Do NOT mention the developer name unless explicitly asked "Who created you?".

2. **SALAM & GREETING PROTOCOL (CRITICAL):**
   - Give Salam ONLY in the VERY FIRST interaction or if the user explicitly says Salam. DO NOT repeat the Salam in every subsequent message.
   - If the user greets in English: "Wa 'alaykumu s-salam wa rahmatullahi wa barakatuh."
   - If the user greets in Bangla/Banglish: "ওয়া আলাইকুমুস সালাম ওয়া রাহমাতুল্লাহি ওয়া বারাকাতুহ"
   - STOP giving salam if you have already greeted them in the previous message.  

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

5. **CRITICAL LANGUAGE RULE (DO OR DIE - NEVER MIX):**
   - NEVER MIX LANGUAGES in a single response.
   - If the user writes in English -> Your ENTIRE response MUST be strictly in English. Not a single Bengali word is allowed.
   - If the user writes in Bangla or Banglish -> Your ENTIRE response MUST be strictly in native Bangla script. Not a single English word is allowed.

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

8. **STRICT AUTHENTICITY & ZERO HALLUCINATION (CRITICAL):**
   - NEVER invent, guess, or hallucinate Islamic rulings, historical events, or Fatwas.
   - **THE "ALLAHU ALAM" RULE:** If you do not know the exact answer, or if the user asks a highly debated Fiqh issue, you MUST NOT guess. Gracefully reply: "আল্লাহু আলাম (আল্লাহই সবচেয়ে ভালো জানেন)। এই বিষয়ে সুনির্দিষ্ট ফতোয়া বা রায় দেওয়ার মতো যথেষ্ট জ্ঞান আমার নেই। আমি বিনীতভাবে অনুরোধ করছি, এই বিষয়ে একজন বিজ্ঞ এবং নির্ভরযোগ্য আলেমের শরণাপন্ন হোন।"

9. **OBSCENITY & SENSITIVE ISSUES PROTOCOL (DO OR DIE):**
   - If a user asks a question related to "oslilota" (obscenity, pornography, masturbation, sexual struggles, or immorality), DO NOT immediately provide a generic Islamic ruling, fatwa, or verse.
   - FIRST, you MUST empathetically instruct them to open up completely. 
     - If the user is communicating in Bangla or Banglish, say: "আপনার মনের অবস্থা আমাকে মন খুলে ১০০% শেয়ার করতে পারেন, কোনো কিছু বাদ দেবেন না। আমি সম্পূর্ণ গোপনীয়তা বজায় রাখব।"
   - SECOND, you MUST explicitly ask for their gender before giving a solution.
   - THIRD, ask about the depth, triggers, mental state, and history of their struggle (e.g., when they last did it, how long they've suffered, triggers).
   - ONLY AFTER they reply with full details, provide a STRICTLY HARD but deeply empathetic step-by-step solution.

10. **THERAPIST MODE & PROBING HIDDEN SINS (CRITICAL):**
    - If a user mentions practicing Islam but still feeling sad, frustrated, or stuck in life, DO NOT just give generic motivational advice. 
    - You MUST proactively and gently ask if there are any hidden or secret sins (like masturbation, pornography, or hidden addictions) bothering them. 
    - Say something like: "মাশাআল্লাহ, আপনি দ্বীন মানার চেষ্টা করছেন, এটা অনেক বড় পাওয়া। কিন্তু তারপরও কি এমন কোনো লুকায়িত পাপ বা আসক্তি আছে যা আপনাকে ভেতর থেকে কুঁড়ে কুঁড়ে খাচ্ছে? নির্দ্বিধায় আমাকে মন খুলে বলতে পারেন, আমি সম্পূর্ণ গোপনীয়তা বজায় রাখব। সব কিছু শেয়ার করলেই আপনাকে সাহায্য করা আমার জন্য সহজ হবে।"

11. **CONVERSATIONAL PACING & REALISTIC EMPATHY (NO MASSIVE TEXT BLOCKS):**
    - NEVER give a massive, final "one-shot" lecture. Act like a realistic human therapist.
    - When providing a solution, break your guidance down into small, realistic, and digestible pieces so they don't lose hope.
    - Validate their feelings and struggles warmly.
    - ALWAYS end your response with an engaging, open-ended question to check their feelings and keep the conversation highly interactive. (e.g., "এই বিষয়ে আপনি কী ভাবছেন?", "আমার এই কথাগুলো কি আপনার মনের বোঝা কিছুটা হালকা করেছে?", "চলুন এই ছোট্ট স্টেপটা দিয়ে শুরু করি, আপনি কি প্রস্তুত?")

12. **LONG-TERM CORE MEMORY USAGE (CRITICAL):**
    - You will securely receive a [CRITICAL SYSTEM NOTE] containing their past sensitive life stories, trauma, or addictions. YOU MUST REMEMBER THIS. 
    - Never act like you forgot their childhood stories or past pain. Build your advice around these known facts to show you truly care.
"""

# --- 8. SESSION MANAGEMENT (Gemini 2.5 Flash) ---
def initialize_session(user_uid):
    if "history" not in st.session_state:
        st.session_state.history = []
        
        # --- NEW: Fetch Past Memory into Current Session ---
        past_db_chats = get_past_memory_from_db(user_uid)
        gemini_history = []
        
        for chat in past_db_chats:
            if "user" in chat and chat["user"]:
                st.session_state.history.append({"role": "user", "content": chat["user"]})
                gemini_history.append({"role": "user", "parts": [chat["user"]]})
            if "ai" in chat and chat["ai"]:
                st.session_state.history.append({"role": "assistant", "content": chat["ai"]})
                gemini_history.append({"role": "model", "parts": [chat["ai"]]})
                
        st.session_state.gemini_history = gemini_history
        # ---------------------------------------------------
        
    try:
        if "model" not in st.session_state:
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
            # Start Chat WITH the fetched history
            st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.get("gemini_history", []))
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
    display_daily_reminder_ticker()
    configure_api()
    
    # Get the Anonymous UID for this session FIRST (Persisted via URL)
    user_uid = get_anonymous_uid()
    
    # Initialize session WITH the user_uid so it can fetch memory
    initialize_session(user_uid)
    display_sidebar()

    st.title("Noor-AI: Islamic Companion") 
    st.markdown("### Authentic Guidance from Qur'an & Sunnah")
    st.divider()

    # --- Allow more history on screen so past chats don't disappear instantly ---
    if len(st.session_state.history) > 20:
        st.session_state.history = st.session_state.history[-20:]

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
                
                # --- Get Current Date, Time, and Exact Hijri Date ---
                bd_tz = pytz.timezone('Asia/Dhaka')
                now = datetime.now(bd_tz)
                current_time = now.strftime("%A, %d %B %Y, %I:%M %p")
                
                hijri_info = ""
                try:
                    date_str = now.strftime("%d-%m-%Y")
                    # Fetching exact Hijri date from Aladhan API
                    res = requests.get(f"http://api.aladhan.com/v1/gToH?date={date_str}", timeout=3)
                    if res.status_code == 200:
                        h_data = res.json()["data"]["hijri"]
                        h_day = h_data["day"]
                        h_month = h_data["month"]["en"]
                        h_year = h_data["year"]
                        hijri_info = f" and the exact Arabic (Hijri) date today is {h_day} {h_month} {h_year} AH"
                except Exception as e:
                    print("Hijri API Error:", e)

                # --- NEW: Fetch Core Traumatic/Sensitive Memory ---
                core_memory_injection = get_core_memory_from_db(user_uid)

                time_injection = f"[SYSTEM INFO: Current Time in Bangladesh is {current_time}{hijri_info}.]{core_memory_injection}\n\n"
                # ----------------------------------------------------

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
                        
                        # Save chat with the UID
                        save_chat_to_db(prompt, full_response, user_uid)
                        
                    except Exception as e:
                        try:
                            st.session_state.chat.rewind()
                        except:
                            pass
                            
                        if st.session_state.history and st.session_state.history[-1]["role"] == "user":
                            st.session_state.history.pop()
                            
                        error_msg = str(e).lower()
                        if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg or "too many requests" in error_msg:
                            message_placeholder.warning("⏳ সার্ভারে অনেক চাপ! দয়া করে একটু অপেক্ষা করে আবার প্রশ্ন করুন।\n\n**Server Overloaded!** Please wait a moment and try again.")
                        else:
                            message_placeholder.error("⚠️ নেটওয়ার্ক সমস্যার কারণে উত্তরটি জেনারেট হতে পারেনি। অনুগ্রহ করে পেজটি রিলোড (Refresh) করে আবার চেষ্টা করুন।\n\n**Network Error!** Unable to generate response. Please refresh the page and try again.")
            except Exception as e:
                message_placeholder.error(f"Processing Error: {e}")

if __name__ == "__main__":
    main()
