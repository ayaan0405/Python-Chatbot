# AI PDF FAQ Chatbot 🤖📄

A clean, fast, and self-contained web application that allows you to upload any PDF document and ask questions about its content. It uses Retrieval-Augmented Generation (RAG) powered by Google's Gemini AI to provide accurate, context-aware answers.

## ✨ Features
- **PDF Processing**: Upload any PDF and automatically extract text.
- **Local Vector Database**: Uses FAISS to create and search through text embeddings entirely locally (no bulky database required!).
- **Gemini AI Integration**: Uses Google's `gemini-flash-latest` model for fast, accurate answers.
- **Modern UI**: Styled with a sleek, custom dark theme.

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ayaan0405/Python-Chatbot.git
   cd Python-Chatbot
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

1. **Run the app:**
   ```bash
   streamlit run faq_chatbot_app.py
   ```

2. **Add your API Key:**
   Open the app in your browser (usually `http://localhost:8501`), and paste your Google Gemini API key into the sidebar.

3. **Upload and Ask:**
   Upload a PDF using the file browser, wait for the index to build, and start asking questions!
