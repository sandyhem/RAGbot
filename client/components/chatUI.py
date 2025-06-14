import streamlit as st
from utils.api import ask_question_api

def render_chat():
    st.subheader("💬 Chat with your documents")

    # Add role selector
    role = st.selectbox("Select your role:", ["Python Developer", "Java Developer"])

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render existing chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # Input and response
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Pass role to API
        response = ask_question_api(user_input, role)
        if response.status_code == 200:
            data = response.json()
            answer = data["response"]
            sources = data.get("sources", [])
            st.chat_message("assistant").markdown(answer)
            if sources:
                st.markdown("📄 **Sources:**")
                for src in sources:
                    st.markdown(f"- `{src}`")
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Error: {response.text}")