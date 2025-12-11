import streamlit as st
import requests

st.set_page_config(page_title="ClaimsAI", page_icon="🛡️")
st.title("ClaimsAI - Auditoria")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua dúvida sobre a apólice..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analisando apólice e regras..."):
            try:
                res = requests.post("http://127.0.0.1:8000/api/chat", json={"pergunta": prompt})
                
                if res.status_code == 200:
                    resposta = res.json()["resposta"]
                    st.markdown(resposta)
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                else:
                    st.error(f"Erro na API: {res.text}")
            except Exception as e:
                st.error(f"Backend desligado ou inacessível: {e}")