import streamlit as st
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

def main():
    st.set_page_config(page_title="Chat with PDF", layout="wide")
    st.title("📄 Chat with your PDF using Gemini")

    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # User question input
    user_question = st.text_input("Ask a question about your documents:")
    if user_question and st.session_state.conversation:
        with st.spinner("Thinking..."):
            response = st.session_state.conversation.invoke({"question": user_question})
            answer = response["answer"] if isinstance(response, dict) and "answer" in response else str(response)
            st.session_state.chat_history.append(("You", user_question))
            st.session_state.chat_history.append(("Bot", answer))

    # Display chat history
    if st.session_state.chat_history:
        for sender, message in reversed(st.session_state.chat_history):
            st.write(f"**{sender}:** {message}")

    # Sidebar for PDF upload
    with st.sidebar:
        st.header("Upload PDFs")
        pdf_docs = st.file_uploader("Upload your PDF files", accept_multiple_files=True, type=["pdf"])
        if st.button("Process") and pdf_docs:
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                if not raw_text.strip():
                    st.error("No text could be extracted from the uploaded PDFs.")
                    return
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversational_chain(vector_store)
                st.session_state.chat_history = []

if __name__ == '__main__':
    main()
