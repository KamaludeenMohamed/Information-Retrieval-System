import streamlit as st
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

def main():
    st.set_page_config(page_title="Chat with PDF", layout="wide")
    st.title("📄 Chat with your PDF using Gemini")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    user_question = st.text_input("Ask a question about your documents:")
    if user_question and st.session_state.conversation:
        response = st.session_state.conversation.run(user_question)
        st.session_state.chat_history.append(("You", user_question))
        st.session_state.chat_history.append(("Bot", response))

    if st.session_state.chat_history:
        for sender, message in reversed(st.session_state.chat_history):
            st.write(f"**{sender}:** {message}")

    with st.sidebar:
        st.header("Upload PDFs")
        pdf_docs = st.file_uploader("Upload your PDF files", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversational_chain(vector_store)
                st.session_state.chat_history = []

if __name__ == '__main__':
    main()
