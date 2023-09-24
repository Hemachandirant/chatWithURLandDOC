import streamlit as st
import openai
import pdfminer
from pdfminer.high_level import extract_text

# Set your OpenAI API key here
openai.api_key = "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"

# Function to have a chat-like conversation with the document
def chat_with_document(document_text, user_message):
    conversation = f"You: {user_message}\nDocument:\n{document_text}\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=conversation,
        max_tokens=50
    )
    return response.choices[0].text

# Streamlit UI
st.title("Chat with PDF Document")

# User uploads a document
document = st.file_uploader("Upload a PDF Document", type=["pdf"])

if document:
    # Handle PDF document using pdfminer
    text = extract_text(document)

    st.subheader("Document Content:")
    st.write(text)

    # Input question above the Send button below the document content
    user_question = st.text_input("Ask a question:", "")
    if st.button("Send"):
        if user_question:
            ai_response = chat_with_document(text, user_question)
            st.subheader("AI Response:")
            st.write(ai_response)

st.info("Upload a PDF document, and you can have a chat-like conversation with its content using AI.")
