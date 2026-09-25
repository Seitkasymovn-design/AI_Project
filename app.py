import os
import ssl
import httpx
import streamlit as st
from google import genai

# Отключаем проверку SSL
ssl._create_default_https_context = ssl._create_unverified_context
os.environ["PYTHONHTTPSVERIFY"] = "0"
os.environ["CURL_CA_BUNDLE"] = ""

# Настройка страницы
st.set_page_config(
    page_title="AI-Informatics Assistant",
    page_icon="💻",
    layout="centered"
)

# Заголовок и информация об авторе
st.title("💻 AI-Informatics — Информатика пәнінің ЖИ-ассистенті")
st.caption("👨‍💻 **Авторы:** Сейітқасымов Нұржан Советбекұлы | №113 Қаракөл орта мектебінің цифрлық және ЖИ ұстазы")
st.markdown("---")

# Боковая панель
st.sidebar.header("⚙️ Жүйе баптаулары")
api_key = st.sidebar.text_input("Gemini API Key кіргізіңіз:", type="password")
selected_grade = st.sidebar.selectbox("Сыныпты таңдаңыз:", ["5-сынып", "6-сынып", "7-сынып", "8-сынып", "9-сынып", "10-сынып", "11-сынып"])

if api_key:
    http_client = httpx.Client(verify=False)
    client = genai.Client(api_key=api_key, http_options={'httpx_client': http_client})

    # Системная инструкция
    system_instruction = f"""
    Сен — мектептің Информатика пәніне арналған сараланған ЖИ-ассистентісің.
    Қазіргі оқыту деңгейі: {selected_grade}.
    
    ӨТЕ МҮПТЕ НҰСҚАУЛЫҚ:
    - Сізді жасаған автор кім немесе бұл жүйені кім құрастырды деп сұраса: "Менің авторым — Сейітқасымов Нұржан Советбекұлы, №113 Қаракөл орта мектебінің цифрлық және ЖИ ұстазы" деп жауап бер.
    - Ешқашан өзіңді Google немесе басқа шет елдік компания жасады деп айтпа. Өзіңді Нұржан мұғалімнің білім беру жобасы аясында жасалған информатика ассистентімін деп таныстыр.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Сұрағыңызды немесе кодтың қатесін жазыңыз..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={'system_instruction': system_instruction}
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Қате орын алды: {e}")
