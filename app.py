import os
import ssl
import streamlit as st
import google.generativeai as genai

# SSL сертификат мәселесін шешу
ssl._create_default_https_context = ssl._create_unverified_context
os.environ["PYTHONHTTPSVERIFY"] = "0"
os.environ["CURL_CA_BUNDLE"] = ""

# Беттің негізгі баптаулары
st.set_page_config(
    page_title="AI-Informatics Assistant",
    page_icon="💻",
    layout="centered"
)

# Заголовок және автор туралы мәлімет
st.title("💻 AI-Informatics — Информатика пәнінің ЖИ-ассистенті")
st.caption("👨‍💻 **Авторы:** Сейітқасымов Нұржан Советбекұлы | №113 Қаракөл орта мектебінің цифрлық және ЖИ ұстазы")
st.markdown("---")

# Навигациялық панель (Sidebar)
st.sidebar.header("⚙️ Жүйе баптаулары")
api_key = st.sidebar.text_input("Gemini API Key кіргізіңіз:", type="password")
selected_grade = st.sidebar.selectbox(
    "Сыныпты таңдаңыз:", 
    ["5-сынып", "6-сынып", "7-сынып", "8-сынып", "9-сынып", "10-сынып", "11-сынып"]
)

if api_key:
    # API кілтті баптау
    genai.configure(api_key=api_key)

    # Негізгі жүйелік нұсқаулық (System Prompt)
    system_instruction = f"""
    Сен — мектептің Информатика пәніне арналған сараланған ЖИ-ассистентісің.
    Қазіргі оқыту деңгейі: {selected_grade}.
    
    ӨТЕ МҮПТЕ НҰСҚАУЛЫҚ:
    - Сізді жасаған автор кім немесе бұл жүйені кім құрастырды деп сұраса: "Менің авторым — Сейітқасымов Нұржан Советбекұлы, №113 Қаракөл орта мектебінің цифрлық және ЖИ ұстазы" деп жауап бер.
    - Ешқашан өзіңді Google немесе басқа шет елдік компания жасады деп айтпа. Өзіңді Нұржан мұғалімнің білім беру жобасы аясында жасалған информатика ассистентімін деп таныстыр.
    """

    # Чат тарихын сақтау
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Чат тарихын экранында көрсету
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Пайдаланушы енгізетін сұрақ
    if prompt := st.chat_input("Сұрағыңызды немесе кодтың қатесін жазыңыз..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Ең тұрақты модельдер тізімі арқылы кезекпен жіберу
            candidate_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            response_text = None
            last_error = None

            for model_name in candidate_models:
                try:
                    model = genai.GenerativeModel(
                        model_name=model_name,
                        system_instruction=system_instruction
                    )
                    response = model.generate_content(prompt)
                    response_text = response.text
                    break
                except Exception as e:
                    last_error = e
                    continue

            if response_text:
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
                st.error(f"Қате орын алды: {last_error}")
else:
    st.info("Жұмысты бастау үшін сол жақтағы панельге Gemini API Key кіргізіңіз.")
