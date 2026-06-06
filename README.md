# 🎬 VidRAG

An AI-powered video understanding system that allows users to upload videos and ask natural language questions to get accurate answers with timestamps.

The system converts video content into searchable knowledge using a Retrieval-Augmented Generation (RAG) pipeline powered by local AI models.

---

## 🧠 Key Idea

Instead of manually watching long videos, VidRAG lets you:

- Upload a video
- Ask questions about its content
- Get precise answers with exact timestamps

---

## ⚙️ How It Works

Video Input  
→ Audio Extraction (ffmpeg)  
→ Speech-to-Text (Whisper)  
→ Text Chunking  
→ Embedding Generation (bge-m3 via Ollama)  
→ Vector Storage  
→ Similarity Search (Cosine Similarity)  
→ Response Generation (Llama 3.2 via Ollama)  
→ Final Answer with Timestamp  

---

## 🛠️ Project Tech Stack

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Speech-to-Text: Whisper
- Embeddings: bge-m3 (Ollama)
- LLM: Llama 3.2 (Ollama)
- Vector Search: Cosine Similarity (scikit-learn)
- Media Processing: ffmpeg
- Data Handling: Pandas / In-memory storage

---

## 🚀 Features

- Upload any video format
- Ask questions in natural language
- Get timestamp-based answers
- Semantic search over video content
- Fully local AI (no API required)
- Multiple video support

---

## ⚙️ Requirements

- Python 3.8+
- ffmpeg installed
- Ollama installed and running

### Required Models

- ollama pull bge-m3
- ollama pull llama3.2
  

▶️ **Run Project**

- git clone <your-repo-link> cd vidrag
- pip install -r requirements.txt
- python app.py

🌐 **Open in Browser**

http://localhost:5000

💡 Why This Project

VidRAG demonstrates:

- Real-world AI application of RAG
- Video + NLP integration
- Local AI deployment without APIs
- Practical semantic search system

📌 Future Improvements
- Database storage instead of RAM
- Faster indexing system
- Multi-language support
- Cloud deployment

👨‍💻 Author
-Mohammed Kupe
