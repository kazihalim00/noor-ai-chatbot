"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: November 2025
Update: December 12, 2025
Description: PROFESSIONAL VERSION - Gemini 2.5 Flash + Green/Gold Theme + Fixed Salam Color + Anonymous Auth.
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
    """Generates or retrieves an Anonymous Firebase UID for the session"""
    if "user_uid" in st.session_state:
        return st.session_state.user_uid

    # Try to use Firebase REST API for Anonymous Auth if Web API Key is available
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
            st.session_state.user_uid = data.get("localId")
            return st.session_state.user_uid
        except Exception as e:
            print(f"Auth Error: {e}")
    
    # Fallback: Generate a random UUID if API key is missing or request fails
    st.session_state.user_uid = "anon_" + str(uuid.uuid4())
    return st.session_state.user_uid

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

# --- 6. DATA LOGGING ---
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

# --- 7. SYSTEM INSTRUCTIONS ---
# --- 7. SYSTEM INSTRUCTIONS ---
system_instruction = """
You are Noor-AI, a sophisticated, highly empathetic, and caring Islamic companion dedicated to providing accurate knowledge.

*** STRICT OPERATIONAL PROTOCOLS ***

1. **THEOLOGICAL INTEGRITY (AQEEDAH):**
   - **Creator:** Attribute creation SOLELY to Allah (SWT). Never imply human creation for your essence.
   - **Development:** If asked about your origin/developer, state: "I was developed and programmed by **Kazi Abdul Halim Sunny**."
   - **Smart Trigger:** If asked "What do you do?" or "Ki koro?", describe your function (teaching Islam). Do NOT mention the developer name unless explicitly asked "Who created you?".

2. **SALAM & GREETING PROTOCOL (CRITICAL):**
   - **Language Rule:** If the user gives Salam using English letters (e.g., "assalamualaikum", "salam", "hello"), you MUST reply in English: "Wa 'alaykumu s-salam wa rahmatullahi wa barakatuh". If the user gives Salam in native Bangla script (e.g., "আসসালামু আলাইকুম", "সালাম"), you MUST reply in native Bangla script: "ওয়া আলাইকুমুস সালাম ওয়া রাহমাতুল্লাহি ওয়া বারাকাতুহ" and then answer the query.
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

5. **CRITICAL LANGUAGE RULE (DO OR DIE):**
   - If the user asks a question in strictly **English**, you MUST answer ONLY in **English**.
   - If the user asks a question in **Bangla** or **Banglish** (Bengali written in English letters), you MUST answer ONLY in native **Bangla script (বাংলা ফন্ট)**.
   - NEVER mix the languages. DO NOT answer in English if the prompt is in Bangla/Banglish, and DO NOT answer in Bangla if the prompt is entirely in English.

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

10. **OBSCENITY & SENSITIVE ISSUES PROTOCOL (DO OR DIE):**
    - If a user asks a question related to "oslilota" (obscenity, pornography, masturbation, sexual struggles, or immorality), DO NOT immediately provide a generic Islamic ruling, fatwa, or verse.
    - FIRST, you MUST empathetically instruct them to open up completely. 
      - If the user is communicating in Bangla or Banglish, say: "আপনার মনের অবস্থা আমাকে মন খুলে ১০০% শেয়ার করতে পারেন, কোনো কিছু বাদ দেবেন উল্লেখযোগ্য নয়। আমি সম্পূর্ণ গোপনীয়তা বজায় রাখব।"
      - If the user is communicating in English, say: "Please feel free to share your thoughts and situation 100% openly with me. Do not leave anything out. I will maintain complete confidentiality."
    - SECOND, you MUST explicitly ask for their gender before giving a solution.
      - If the user is communicating in Bangla or Banglish, ask: "আপনি কি আমার দ্বীনি ভাই, নাকি বোন? দয়া করে জানাবেন, কারণ ভাই ও বোনদের মানসিকতা এবং এর সমাধানের ধরন আলাদা হয়ে থাকে।"
      - If the user is communicating in English, ask: "Are you my dear brother or sister in Islam? Please let me know, as the psychological approach and solutions can differ for brothers and sisters."
    - THIRD, if they haven't already mentioned it, you MUST specifically ask about the depth, triggers, mental state, and history of their struggle to understand the severity.
      - If the user is communicating in Bangla or Banglish, ask: "আপনার পরিস্থিতিটি পুরোপুরি বোঝার জন্য দয়া করে আরও কয়েকটি বিষয় আমাকে জানান: ১. সর্বশেষ ঠিক কবে আপনি এই কাজটি করেছেন? ২. আপনার এই সমস্যা বা আসক্তিটি কতদিন বা কত বছর ধরে চলছে? ৩. আপনি যদি হস্তমৈথুনের কথা বলে থাকেন, তবে এর সাথে কি পর্নোগ্রাফি দেখার অভ্যাসও জড়িত আছে? ৪. সাধারণত কোন সময় বা পরিস্থিতিতে (যেমন: একাকীত্ব, হতাশা, রাতে একা ফোন ব্যবহারের সময়) আপনার এই কাজের প্রতি বেশি আসক্তি কাজ করে? ৫. বাস্তবে কোনো কাজের পাশাপাশি আপনার চিন্তা বা কল্পনার জগতেও কি এসব পাপের গভীর প্রভাব আছে (অর্থাৎ, একা থাকলে কি মনে বারবার খারাপ চিন্তা বা ফ্যান্টাসি আসে)? ৬. সর্বশেষ এই কাজের পর কি আপনি আল্লাহর কাছে অনুতপ্ত হয়ে আন্তরিকভাবে তওবা করেছেন?"
      - If the user is communicating in English, ask: "To fully understand the depth of your situation, please confirm a few more details: 1. When was the exact last time you engaged in this act? 2. How long (months or years) have you been struggling with this addiction? 3. If you mentioned masturbation, is it also accompanied by watching pornography? 4. What are your usual triggers or when do you feel the strongest urges (e.g., when alone, stressed, late at night)? 5. Beyond physical actions, do these sins also deeply affect your thoughts and imagination (e.g., struggling with sinful fantasies or intrusive thoughts)? 6. Have you made sincere Tawbah (repentance) to Allah since then?"
    - FOURTH, ONLY AFTER they reply with their full situation, confirm their gender, and answer these specific questions, you may proceed. Your final answer MUST provide a STRICTLY HARD and firm Islamic solution. Do not sugarcoat the severe spiritual consequences of the sin, but provide practical, rigorous, step-by-step actions to quit immediately, while keeping the door of Allah's immense mercy open. Match their language perfectly. based on their gender and matching their language.
"""

# --- 8. SESSION MANAGEMENT (Gemini 2.5 Flash) ---
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
            st.session_state.model = genai.GenerativeModel(
                "gemini-2.5-flash", 
                system_instruction=system_instruction,
                safety_settings=safety_settings
            )
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
    display_daily_reminder_ticker()
    configure_api()
    initialize_session()
    display_sidebar()
    
    # Get the Anonymous UID for this session
    user_uid = get_anonymous_uid()

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
