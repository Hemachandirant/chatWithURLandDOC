import streamlit as st
import openai
from PyPDF2 import PdfReader

# Function to read the API key from apikey.txt
def get_openai_api_key():
    with open("apikey.txt", "r") as file:
        api_key = file.read().strip()
    return api_key

# Load the OpenAI API key
openai.api_key = get_openai_api_key()

# Initialize chat history
chat_history = []

# Function to have a chat-like conversation with the document
def chat_with_document(document_text, user_message, chat_history):
    conversation = ""

    for message in chat_history:
        conversation += f"You: {message['user_message']}\nDocument:\n{document_text}\n"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=conversation,
            max_tokens=50
        )
        ai_responses.append(response.choices[0].text)
    
    # Add the new user message to the chat history
    conversation += f"You: {user_message}\nDocument:\n{document_text}\n"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=conversation,
        max_tokens=50
    )
    ai_response = response.choices[0].text  # Get the AI response for the new message
    
    # Add the new user message to the chat history
    chat_history.append({"user_message": user_message})

    return ai_response

# Streamlit UI
st.title("Chat with PDF Document")

# Sidebar for PDF upload
st.sidebar.title("Upload PDF Document")
document = st.sidebar.file_uploader("Select a PDF Document", type=["pdf"])

if document:
    # Handle PDF document
    pdf_reader = PdfReader(document)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

# Initialize AI responses
ai_responses = []
ai_response = ""  # Initialize ai_response with a default empty string

# Main window for chat
st.subheader("Chat Interface")
user_message = st.text_input("Type your message:", "")

if st.button("Send"):
    if user_message and document:
        ai_response = chat_with_document(text, user_message, chat_history)  # Update ai_response with the chat response
        ai_responses.append(ai_response)

# Display AI responses in a separate text area
st.subheader("AI Response:")
ai_response_text = "\n".join(ai_responses)  # Combine AI responses into a single string
st.text_area("", ai_response_text, height=200)  # Create a text area for AI responses
