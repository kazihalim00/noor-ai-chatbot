"""
Project Name: Noor-AI Islamic Assistant
Author: Kazi Abdul Halim Sunny
Date: December 2025
Description: PROFESSIONAL VERSION - Minimalist UI + Firebase Knowledge Retrieval (RAG).
"""

import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import firebase_admin
from firebase_admin import credentials, firestore
import os

# --- 1. SETUP PAGE CONFIGURATION ---
def setup_page_config():
    st.set_page_config(
        page_title="Noor-AI: Islamic Companion",
        page_icon="🌙",
        layout="centered"
    )

# --- 2. CSS: MINIMALIST & CLEAN (STRICTLY PRESERVED) ---
def apply_custom_styles():
    st.markdown("""
        <style>
        /* Import clean font for straight numbers & clear text */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

        /* General App Background - Dark but Neutral */
        .stApp { background-color: #0E1117; color: #E6E6E6; }
        
        /* Headers - Clean & Simple */
        h1 { 
            color: #E6E6E6 !important; 
            font-family: 'Inter', sans-serif; 
            text-align: center; 
            font-weight: 500; 
            letter-spacing: 0.5px;
            padding-bottom: 10px;
        }
        .stMarkdown h3 { 
            color: #A1A1AA !important; /* Neutral Grey */
            text-align: center; 
            font-weight: 400; 
        }
        
        /* Sidebar Styling - Minimalist Black */
        [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #27272A; }
        
        /* Input Field Styling */
        .stTextInput input { 
            background-color: #18181B !important; /* Zinc-900 */
            color: #FAFAFA !important; 
            border: 1px solid #3F3F46; 
            border-radius: 15px; 
            padding-left: 15px; 
            font-family: 'Inter', sans-serif;
        }
        
        /* --- CHAT INTERFACE STYLING --- */
        
        /* User Message (Odd) - Transparent/Minimal */
        div[data-testid="stChatMessage"]:nth-of-type(odd) {
            background-color: transparent !important;
            border: 1px solid #27272A !important;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            font-family: 'Inter', sans-serif;
        }

        /* AI Message (Even) - SUBTLE GREY BOX (NO HEAVY COLORS) */
        div[data-testid="stChatMessage"]:nth-of-type(even) {
            background-color: #1C1C1E !important; /* Very Light Charcoal */
            border: 1px solid #2C2C2E !important; /* Subtle border */
            border-left: 3px solid #D4AF37 !important; /* Thin Elegant Gold Accent Line */
            border-radius: 6px 10px 10px 6px;
            padding: 20px;
            margin-bottom: 15px;
        }
        
        /* Text Visibility inside AI Bubble - High Clarity */
        div[data-testid="stChatMessage"]:nth-of-type(even) p,
        div[data-testid="stChatMessage"]:nth-of-type(even) div,
        div[data-testid="stChatMessage"]:nth-of-type(even) li {
             color: #E6E6E6 !important; /* Off-White */
             line-height: 1.8; 
             font-family: 'Inter', sans-serif !important; 
             font-size: 16px;
        }

        /* Key Terms - Gold text only here */
        div[data-testid="stChatMessage"]:nth-of-type(even) strong { 
            color: #FCD34D !important; /* Soft Gold */
            font-weight: 600 !important; 
        }

        /* Hyperlinks - Subtle Blue */
        div[data-testid="stChatMessage"]:nth-of-type(even) a { 
            color: #60A5FA !important; /* Soft Blue */
            text-decoration: none !important; 
            border-bottom: 1px dotted #60A5FA;
        }
        
        /* Mobile Responsiveness */
        .stMarkdown table { display: block; overflow-x: auto; white-space: nowrap; width: 100%; }
        </style>
    """, unsafe_allow_html=True)

# --- 3. API CONFIGURATION ---
def configure_api():
    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
            genai.configure(api_key=api_key)
        else:
            st.error("⚠️ Configuration Error: GOOGLE_API_KEY not found in Secrets.")
            st.stop()
    except Exception as e:
        st.error(f"API Connection Failed: {e}")

# --- 4. FIREBASE INITIALIZATION (SMART HYBRID) ---
def init_firebase():
    # Check if app is already connected
    if firebase_admin._apps:
        return firestore.client()

    try:
        # 1. Use local 'service_account.json' if available (For Local PC)
        if os.path.exists("service_account.json"):
            cred = credentials.Certificate("service_account.json")
            firebase_admin.initialize_app(cred)
            return firestore.client()
            
        # 2. Use 'st.secrets' if running on Cloud
        elif "firebase" in st.secrets:
            firebase_creds = dict(st.secrets["firebase"])
            # Fix private key format for Streamlit Cloud
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

# --- 5. SMART KNOWLEDGE RETRIEVAL (NEW FEATURE) ---
def get_knowledge_from_firebase(query):
    if not db: return ""
    
    try:
        # Fetch documents from 'knowledge_base' collection
        docs = db.collection("knowledge_base").stream()
        context_data = ""
        query_words = query.lower().split()
        
        found_count = 0
        for doc in docs:
            data = doc.to_dict()
            content = data.get("content", "")
            title = data.get("title", "")
            
            # Simple keyword matching logic
            if any(word in content.lower() for word in query_words if len(word) > 3):
                context_data += f"SOURCE ARTICLE [{title}]:\n{content}\n\n"
                found_count += 1
                if found_count >= 2: break # Limit to top 2 relevant articles
                
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

# --- 7. SYSTEM INSTRUCTIONS (STRICTLY PRESERVED) ---
system_instruction = """
You are Noor-AI, a sophisticated and caring Islamic companion dedicated to providing accurate knowledge.

*** OPERATIONAL PROTOCOLS ***

1. **THEOLOGICAL INTEGRITY (AQEEDAH):**
   - **Creator:** Attribute creation SOLELY to Allah (SWT). Never imply human creation for your essence.
   - **Development:** If asked about your origin, state: "I was developed and programmed by **Kazi Abdul Halim Sunny**."

2. **SALAM RESPONSE PROTOCOL:**
   - Upon receiving "Salam" or "Assalamu Alaikum", you MUST respond with the COMPLETE reply: "**Wa 'alaykumu s-salam wa rahmatullahi wa barakatuh**".
   - Avoid abbreviated responses.

3. **CITATION & LINKS (MANDATORY FORMAT):**
   - **Quran:** Cite strictly as: **[Surah Name: Ayah](https://quran.com/SURAH_NUMBER/AYAH_NUMBER)**
   - **Hadith:** Provide direct, clickable links to **Sunnah.com** where applicable.
     - **Format:** `[Book Name: Number](https://sunnah.com/BOOK_SLUG/NUMBER)`
     - **Example:** **[Sahih al-Bukhari: 1](https://sunnah.com/bukhari:1)**

4. **IDENTITY & BIO (PRESERVE EXACT TEXT):**
   - **Developer Name:** Kazi Abdul Halim Sunny.
   - **Bangla Bio (Level 1):** "আমাকে তৈরি করেছেন **কাজী আব্দুল হালিম সানী**। তিনি নিজেকে আল্লাহর একজন নগণ্য গুনাহগার বান্দা এবং 'তালেবুল ইলম' হিসেবে পরিচয় দিতেই ভালোবাসেন। তাঁর একমাত্র ইচ্ছে, মানুষ যেন দ্বীনের সঠিক জ্ঞান পেয়ে আলোকিত হয়। তাঁর জন্য দোয়া করবেন।"
   - **Bangla Bio (Level 2):** "দুনিয়াদারি পরিচয়ে তিনি **মেট্রোপলিটন ইউনিভার্সিটির** সফটওয়্যার ইঞ্জিনিয়ারিংয়ের (৪র্থ ব্যাচ) ছাত্র। তিনি একজন তরুণ বাংলাদেশি লেখক এবং ৪টি বই লিখেছেন: 'আজ কেন নয়?', 'একটুকরো স্বপ্ন', 'অমানিশা', এবং 'প্রিটেন্ড' (তরুণদের সমস্যা নিয়ে লেখা উপন্যাস - যার অনলাইন কপি সবার জন্য ফ্রী)।"

5. **LINGUISTIC CONSISTENCY:**
   - Respond in **English** if the query is in English.
   - Respond in **Bangla** if the query is in Bangla.

6. **SCHOLARLY REFERENCE PRIORITY:**
   - Prioritize insights from **Ustaz Abu Sa'ada Muhammad Hammad Billaah** & **Esho Din Shikhi**.
   - If 'SOURCE ARTICLE' is provided in context, use it to answer and mention it.
   - **Visual Emphasis:** Use **Bold** formatting for significant Islamic terminology (e.g., **Tawhid**, **Taqwa**) to render them in **GOLD** color.
"""

# --- 8. SESSION MANAGEMENT ---
def initialize_session():
    if "history" not in st.session_state:
        st.session_state.history = []
        
    try:
        if "model" not in st.session_state:
            st.session_state.model = genai.GenerativeModel("gemini-flash-latest", system_instruction=system_instruction)
            st.session_state.chat = st.session_state.model.start_chat(history=[])
    except Exception as e:
        st.error(f"System Initialization Failure: {e}")

# --- 9. SIDEBAR INTERFACE ---
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
            st.markdown("---")
            st.download_button("📥 Export Conversation", chat_str, "noor_ai_session.txt")

# --- 10. MAIN APPLICATION LOOP ---
def main():
    setup_page_config()
    apply_custom_styles()
    configure_api()
    initialize_session()
    display_sidebar()

    st.title("Noor-AI: Islamic Companion") 
    st.markdown("### Authentic Guidance from Qur'an & Sunnah")
    st.divider()

    # --- RENDER CHAT HISTORY ---
    for message in st.session_state.history:
        role = message["role"]
        avatar = "👤" if role == "user" else "🎓"
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["content"])

    # --- USER INPUT SECTION ---
    prompt = st.chat_input("Inquire about Islam, History, or Spirituality...")

    if prompt:
        # 1. Capture User Input
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # 2. Generate AI Response
        with st.chat_message("assistant", avatar="🎓"):
            placeholder = st.empty()
            placeholder.markdown("Analyzing sources...") 
            try:
                # --- A. Check Database (RAG) ---
                retrieved_context = get_knowledge_from_firebase(prompt)
                
                # --- B. Construct Prompt ---
                if retrieved_context:
                    # If data found, inject into prompt
                    final_prompt = f"""
                    Use the following CONTEXT from our database to answer the user's question.
                    
                    CONTEXT:
                    {retrieved_context}
                    
                    USER QUESTION: {prompt}
                    """
                else:
                    # If no data found, use standard prompt
                    final_prompt = prompt

                # --- C. Call AI Model ---
                if hasattr(st.session_state, 'chat'):
                    response = st.session_state.chat.send_message(final_prompt)
                    placeholder.markdown(response.text)
                    
                    st.session_state.history.append({"role": "assistant", "content": response.text})
                    
                    # Log to Database
                    save_chat_to_db(prompt, response.text)
                    
            except Exception as e:
                placeholder.error(f"Processing Error: {e}")

if __name__ == "__main__":
    main()
