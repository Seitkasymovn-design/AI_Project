import streamlit as st
from google import genai

import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
os.environ["PYTHONHTTPSVERIFY"] = "0"
os.environ["CURL_CA_BUNDLE"] = ""

# Веб-беттің аты мен белгішесін орнату
st.set_page_config(
    page_title="AI-Informatics Assistant",
    page_icon="💻",
    layout="centered"
)
import os
import ssl
import httpx
import streamlit as st
from google import genai

# Отключаем глобальную проверку SSL
ssl._create_default_https_context = ssl._create_unverified_context
os.environ["PYTHONHTTPSVERIFY"] = "0"
os.environ["CURL_CA_BUNDLE"] = ""

# Веб-беттің аты мен белгішесін орнату
st.set_page_config(
    page_title="AI-Informatics Assistant",
    page_icon="💻",
    layout="centered"
)

st.title("💻 AI-Informatics — Информатика пәнінің ЖИ-ассистенті")
st.markdown("---")

# Сол жақ панельге баптауларды орнату
st.sidebar.header("⚙️ Жүйе баптаулары")
api_key = st.sidebar.text_input("Gemini API Key кіргізіңіз:", type="password")
selected_grade = st.sidebar.selectbox("Сыныпты таңдаңыз:", ["5-сынып", "6-сынып", "7-сынып", "8-сынып", "9-сынып", "10-сынып", "11-сынып"])

# Gemini API арқылы клиентті іске қосу
if api_key:
    # HTTP-клиентте SSL тексеруді өшіру
    http_client = httpx.Client(verify=False)
    client = genai.Client(api_key=api_key, http_options={'httpx_client': http_client})

    # ЖИ-ге берілетін негізгі рол мен нұсқаулық (System Instruction)
    system_instruction = f"""
    Сен — мектептің Информатика пәніне арналған сараланған ЖИ-ассистентісің.
    Қазіргі оқыту деңгейі: {selected_grade}.
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
            try:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                    config={'system_instruction': system_instruction}
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Қате орын алды: {e}")