# main.py
import os.path
import os
from dotenv import load_dotenv

# Imports from Google's own libraries
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.readers.google import GmailReader

# Load environment variables for the GOOGLE_API_KEY
load_dotenv()

# --- NEW, STABLE AUTHENTICATION FUNCTION ---
def get_gmail_service():
    """Builds and returns an authenticated Gmail API service object."""
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return build("gmail", "v1", credentials=creds)


def main():
    """Main function to load emails, create an index, and query it."""
    # Configure the global LLM
    Settings.llm = GoogleGenAI(model="models/gemini-1.5-flash")

    # Get the Gmail service object using our new function
    print("Building Gmail service connection...")
    gmail_service = get_gmail_service()

    # Pass the created service object to the GmailReader
    print("Initializing Gmail reader...")
    loader = GmailReader(service=gmail_service, results_per_page=50)

    # Load emails
    print("Loading emails...")
    # New Code
    loader = GmailReader(
        service=gmail_service,
        query="in:inbox is:read",  # Pass the query here
        results_per_page=50
    )
    documents = loader.load_data() # Now called with no arguments
    print(f"Loaded {len(documents)} emails.")

    # Create the index
    print("Indexing emails... (this may take a moment)")
    index = VectorStoreIndex.from_documents(documents)

    # Create a query engine
    query_engine = index.as_query_engine()

    # Ask a question
    print("Querying index...")
    response = query_engine.query("What were the most recent topics discussed in my emails?")

    print("\n--- Response ---")
    print(response)
    print("----------------")

if __name__ == "__main__":
    main()