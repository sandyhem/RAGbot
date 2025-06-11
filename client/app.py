import streamlit as st
from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat






st.set_page_config(
    page_title="RAGBOT-Hem",
    page_icon=":robot:",
    layout="wide"
)
st.title("Chat with RAGBOT")

render_uploader()
render_chat()
render_history_download()