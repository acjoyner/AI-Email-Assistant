<<<<<<< HEAD
# AI Email Assistant ✉️

This is a personal AI assistant that securely connects to your Gmail account. It reads and understands your recent emails, allowing you to ask questions, summarize topics, and find information using a simple chat interface built with Streamlit.

## ✨ Key Features

* **Conversational Search:** Ask natural language questions about your email content.
* **Information Extraction:** Create to-do lists, find action items, or pull specific information from messages.
* **Persistent Memory:** Uses a local ChromaDB database to save your indexed emails, so it only has to scan your inbox once. Subsequent startups are much faster.
* **Secure & Private:** Your credentials, tokens, and email data are all stored locally on your machine and are never shared.

## 🛠️ Technology Stack

* **Frontend:** Streamlit
* **AI/Indexing:** LlamaIndex
* **Language Model:** Google Gemini
* **Vector Database:** ChromaDB
* **Authentication:** Google API Client & OAuth

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

* Python 3.8+
* A Google Cloud Platform project.
* A Google API Key for the Gemini model.

### ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/acjoyner/AI-Email-Assistant.git](https://github.com/acjoyner/AI-Email-Assistant.git)
    cd YOUR_REPOSITORY
    ```

2.  **Set Up Google Credentials**
    * Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a project.
    * Enable the **Gmail API**.
    * Go to "Credentials," create an "OAuth 2.0 Client ID" for a **Desktop app**, and download the JSON file.
    * Rename the downloaded file to `credentials.json` and place it in the root of your project directory.

3.  **Create a Virtual Environment**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4.  **Create a `requirements.txt` File**
    Create a file named `requirements.txt` and paste the following lines into it:
    ```
    streamlit
    python-dotenv
    llama-index
    llama-index-llms-google-genai
    llama-index-readers-google
    llama-index-vector-stores-chroma
    chromadb
    google-api-python-client
    google-auth-httplib2
    google-auth-oauthlib
    ```

5.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

6.  **Create the Environment File**
    * Create a file named `.env`.
    * Add your Google API key for Gemini to this file:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

---

## ▶️ How to Run

1.  Make sure your virtual environment is active.
    ```bash
    source .venv/bin/activate
    ```
2.  Run the Streamlit app.
    ```bash
    streamlit run app.py
    ```
A new tab will open in your browser with the application.

**Note:** The very first time you run the app, a browser window will open asking you to authenticate with your Google account. After you approve, a `token.json` file will be created, and you won't need to log in again. The app will also take some time to index your emails and create the `chroma_db` folder. Subsequent runs will be much faster.

---

## 🔒 Security & Privacy

* Your Google `credentials.json` and `token.json` are stored locally and are not committed to Git (thanks to the `.gitignore` file).
* Your email data is indexed and stored locally in the `chroma_db` folder, which is also ignored by Git.
* Your API key is stored locally in the `.env` file, also ignored by Git.
=======
# AI-Email-Assistant
This is a personal AI Email Assistant that securely connects to your Gmail account. It reads and understands your recent emails, allowing you to ask questions, summarize topics, and find information using a simple chat interface.
>>>>>>> 3de7b0a276bef229befa5adfacd905ebccd92919
