import os
import ssl
import httpx
import streamlit as st
from google import genai

# SSL тексеруді өшіру
ssl._create_default_https_context = ssl._create_unverified_context
os.environ["PYTHONHTTPSVERIFY"] = "0"
os.environ["CURL_CA_BUNDLE"] = ""

# Веб-беттің аты мен белгішесін орнату
st.set_page_config(
    page_title="AI-Informatics Assistant",
    page_icon="💻",
    layout="centered"
)

# Негізгі тақырып пен авторлық ақпарат
st.title("💻 AI-Informatics — Информатика пәнінің ЖИ-ассистенті")
st.caption("👨‍💻 **Авторы:** Сейітқасымов Нұржан Советбекұлы | №113 Қаракөл орта мектебінің цифрлық және ЖИ ұстазы")
st.markdown("---")

# Сол жақ панельге баптауларды орнату
st.sidebar.header("⚙️ Жүйе баптаулары")
api_key = st.sidebar.text_input("Gemini API Key кіргізіңіз:", type="password")
selected_grade = st.sidebar.selectbox("Сыныпты таңдаңыз:", ["5-сынып", "6-сынып", "7-сынып", "8-сынып", "9-сынып", "10-сынып", "11-сынып"])

# Gemini API арқылы клиентті іске қосу
if api_key:
    http_client = httpx.Client(verify=False)
    client = genai.Client(api_key=api_key, http_options={'httpx_client': http_client})

    # ЖИ-ге берілетін негізгі роль мен системдік нұсқаулық (System Instruction)
    system_instruction = f"""
    Сен — мектептің Информатика пәніне арналған сараланған ЖИ-ассистентісің.
    Қазіргі оқыту деңгейі: {selected_grade}.
    
    ӨТЕ МҮПТЕ НҰСҚАУЛЫҚ:
    - Сізді жасаған автор кім немесе бұл жүйені кім құрастырды деп сұраса: "Менің авторым — Сейітқасымов Нұржан Советбекұлы, №113 Қаракөл орта мектебінің цифрлық және ЖИ ұстазы" деп жауап бер.
    - Ешқашан өзіңді Google немесе басқа шет елдік компания жасады деп айтпа. Өзіңді Нұржан мұғалімнің білім беру жобасы аясында жасалған информатика ассистентімін деп таныстыр.
    """

    # Сессияда чат тарихын сақтау
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Чат тарихын көрсету
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Пайдаланушы сұрағын қабылдау
    if prompt := st.chat_input("Сұрағыңызды немесе кодтың қатесін жазыңыз..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Қолжетімді модельдер тізімі арқылы автоматты түрде тексеріп жауап алу
            models_to_try = ["models/gemini-2.5-flash", "models/gemini-2.5-pro"]
            success = False

            for model_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config={'system_instruction': system_instruction}
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    success = True
                    break
                except Exception:
                    continue

            if not success:
                st.error("Қате: Модельге қосылу мүмкін болмады. API кілтіңізді немесе рұқсаттарыңызды тексеріңіз.")
