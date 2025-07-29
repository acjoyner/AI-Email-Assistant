# app.py
import streamlit as st
st.set_page_config(
    page_title="My Email Assistant",
    page_icon="📧"
)

import os
from dotenv import load_dotenv

# Imports for ChromaDB
import chromadb
from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

# Imports from Google's own libraries
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from llama_index.llms.google_genai import GoogleGenAI
from llama_index.readers.google import GmailReader

# Load environment variables for the GOOGLE_API_KEY
load_dotenv()

# --- Authentication Function (same as before) ---
def get_gmail_service():
    """Builds and returns an authenticated Gmail API service object."""
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

# --- Caching the query engine ---
@st.cache_resource
def load_and_index_data():
    """Loads emails and builds the LlamaIndex query engine using ChromaDB for persistence."""
    # Configure the LLM
    Settings.llm = GoogleGenAI(model="models/gemini-1.5-flash")

    # Initialize ChromaDB client and a collection
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection("gmail_emails")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Check if the collection is empty. If it is, load data from Gmail.
    if chroma_collection.count() == 0:
        with st.spinner("Connecting to your Gmail account..."):
            service = get_gmail_service()

        with st.spinner("First time setup: Loading and indexing recent emails... This may take a moment."):
            loader = GmailReader(
                service=service,
                query="in:inbox is:read",
                results_per_page=100
            )
            documents = loader.load_data()
            # This will load the documents into ChromaDB
            index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    else:
        # If the collection is not empty, load the index directly from ChromaDB
        with st.spinner("Loading index from database..."):
            index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)

    return index.as_query_engine()

# --- Streamlit App UI (same as before) ---
st.title("✉️ Anthony's Assistant")
st.info("Ask any question about your recent emails!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Load the query engine
query_engine = load_and_index_data()

if prompt := st.chat_input("What would you like to know?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        response = query_engine.query(prompt)

    with st.chat_message("assistant"):
        st.markdown(response.response)
    st.session_state.messages.append({"role": "assistant", "content": response.response})