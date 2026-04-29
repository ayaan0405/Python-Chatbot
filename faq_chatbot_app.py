import os, json, faiss, numpy as np, pdfplumber, streamlit as st
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

INDEX_PATH = "faq.index"
CHUNKS_PATH = "chunks.json"

st.set_page_config(page_title="PDF FAQ Chatbot", layout="centered")
st.title("PDF FAQ Chatbot")
st.markdown("Ask a question based on the PDF you upload.")
if os.path.exists("styles.css"):
    with open("styles.css") as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

api_key = st.sidebar.text_input("Gemini API Key", type="password") or os.getenv("GEMINI_API_KEY", "")
if not api_key:
    st.warning("Provide Gemini API key.")
    st.stop()

genai.configure(api_key=api_key)
model = SentenceTransformer("all-MiniLM-L6-v2")

pdf = st.file_uploader("Upload a PDF", type=["pdf"])
if pdf:
    if "current_pdf" not in st.session_state or st.session_state.current_pdf != pdf.name or not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
        with st.spinner("Processing PDF and building index..."):
            text = "".join(p.extract_text() or "" for p in pdfplumber.open(pdf).pages)
            chunks = [text[i:i+500] for i in range(0, len(text), 450) if text[i:i+500].strip()]
            vecs = model.encode(chunks, show_progress_bar=False)
            
            with open(CHUNKS_PATH, "w") as f:
                json.dump(chunks, f)
                
            idx = faiss.IndexFlatL2(vecs.shape[1])
            idx.add(np.array(vecs, dtype=np.float32))
            faiss.write_index(idx, INDEX_PATH)
            st.session_state.current_pdf = pdf.name
            
    q = st.text_input("Enter your question:")
    if q:
        with st.spinner("Generating answer..."):
            idx = faiss.read_index(INDEX_PATH)
            with open(CHUNKS_PATH, "r") as f:
                saved_chunks = json.load(f)
                
            _, I = idx.search(np.array(model.encode([q]), dtype=np.float32), 3)
            ctx = "\n\n".join(saved_chunks[int(i)] for i in I[0] if i >= 0)
            prompt = f"Answer strictly based on context:\n{ctx}\n\nQuestion: {q}\n\nAnswer:"
            ans = genai.GenerativeModel("models/gemini-flash-latest").generate_content(prompt).text.strip()
            st.markdown(f'<div class="answer-container"><h3>Answer</h3><hr/><p>{ans}</p></div>', unsafe_allow_html=True)
else:
    st.info("Please upload a PDF to begin.")
