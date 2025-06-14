import streamlit as st
from utils.api import upload_pdfs_api, ask_question_api, clear_knowledge_api

def render_uploader():
    st.sidebar.header("Upload PDFs")
    uploaded_files = st.sidebar.file_uploader(
        "Upload Multiple PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )
    if st.sidebar.button("Upload"):
        if uploaded_files:
            response = upload_pdfs_api(uploaded_files)
            if response.status_code == 200:
                st.sidebar.success("Files uploaded successfully!")
            else:
                st.sidebar.error(f"Error uploading files: {response.text}")
        else:
            st.sidebar.warning("Please upload at least one PDF file.")

    # Manual clear history button
    if st.sidebar.button("Clear Chat History"):
        st.session_state.messages = []
        st.sidebar.success("Chat history cleared.")

    # if st.sidebar.button("Clear Knowledge Base"):
    #     response = clear_knowledge_api()
    #     if response.status_code == 200:
    #         st.sidebar.success("Knowledge base cleared!")
    #     else:
    #         st.sidebar.error("Failed to clear knowledge base.")