import streamlit as st
import requests
import streamlit as st
import openai
from PyPDF2 import PdfReader

# Azure OpenAI API URL and key
azure_api_url = "https://dwspoc.openai.azure.com/openai/deployments/GPTDavinci/completions?api-version=2022-12-01"
azure_api_key = "bd38ee31e244408cacab3e1dd4c32221"   # Replace with your Azure OpenAI API key

# Function to have a chat-like conversation with the document
def chat_with_document(document_text, user_message):
    conversation = f"You: {user_message}\nDocument:\n{document_text}\n"
    
    headers = {
        "Authorization": f"Bearer {azure_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": conversation,
       "max_tokens": 400,
        "temperature": 0.7,
        "top_p": 1,
        "stop": None,
    }

    # Make the API call to Azure OpenAI
    response = requests.post(azure_api_url, headers=headers, json=data)
    
    # Debugging information
    print("API Response Status Code:", response.status_code)
    print("API Response JSON:", response.json())

    response_data = response.json()

    # Extract and return the response text
    response_text = response_data.get("choices", [{}])[0].get("text", "").strip()

    return response_text

# Streamlit UI
st.title("Chat with PDF Document")

# User uploads a document
document = st.file_uploader("Upload a PDF Document", type=["pdf"])

if document:
    # Handle PDF document
    pdf_reader = PdfReader(document)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    st.subheader("Document Content:")
    st.write(text)

    # Input question above the Send button below the document content
    user_question = st.text_input("Ask a question:", "")
    if st.button("Send"):
        if user_question:
            ai_response = chat_with_document(text, user_question)

            # Debugging information
            print("AI Response:", ai_response)

            st.subheader("AI Response:")
            st.write(ai_response)

st.info("Upload a PDF document, and you can have a chat-like conversation with its content using AI.")
