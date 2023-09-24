import os
import streamlit as st
import pickle
import time
import openai
from PyPDF2 import PdfReader
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to read the OpenAI API key from apikey.txt
def get_openai_api_key():
    with open("apikey.txt", "r") as file:
        api_key = file.read().strip()
    return api_key

# Initialize OpenAI
openai.api_key = get_openai_api_key()

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
st.title("DocBot: Chat with PDF and URL 📈")
st.sidebar.title("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_openai.pkl"

main_placeholder = st.empty()
llm = OpenAI(temperature=0.9, max_tokens=500)

# Chat history for the document chat
chat_history = []

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
user_message = st.text_input("Type your message:", "")

if st.button("Send"):
    if user_message and document:
        ai_response = chat_with_document(text, user_message, chat_history)  # Update ai_response with the chat response
        ai_responses.append(ai_response)

# Display AI responses in a separate text area
st.subheader("AI Response:")
ai_response_text = "\n".join(ai_responses)  # Combine AI responses into a single string
st.text_area("", ai_response_text, height=200)  # Create a text area for AI responses

if process_url_clicked:
    # Your data loading and processing code here...
    # load data
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Data Loading...Started...✅✅✅")
    data = loader.load()
    # split data
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    main_placeholder.text("Text Splitter...Started...✅✅✅")
    docs = text_splitter.split_documents(data)
    # create embeddings and save it to FAISS index
    embeddings = OpenAIEmbeddings()
    vectorstore_openai = FAISS.from_documents(docs, embeddings)
    main_placeholder.text("Embedding Vector Started Building...✅✅✅")
    time.sleep(2)

    # Save the FAISS index to a pickle file
    with open(file_path, "wb") as f:
        pickle.dump(vectorstore_openai, f)




query = st.text_input("Question: ")
if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain({"question": query}, return_only_outputs=True)
            # result will be a dictionary of this format --> {"answer": "", "sources": [] }
            st.header("Answer")
            st.write(result["answer"])

            # Display sources, if available
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")  # Split the sources by newline
                for source in sources_list:
                    st.write(source)
