🎬 **VidRAG**

An AI-powered video understanding system that allows users to upload videos and ask natural language questions to get accurate answers with timestamps.

The system converts video content into searchable knowledge using a Retrieval-Augmented Generation (RAG) pipeline powered by local AI models.

🧠 **Key Idea**

Instead of manually watching long videos, VidRAG lets you:

Upload a video
Ask questions about its content
Get precise answers with exact timestamps
⚙️ **How It Works**

Video Input
→ Audio Extraction (ffmpeg)
→ Speech-to-Text (Whisper)
→ Text Chunking
→ Embedding Generation (bge-m3 via Ollama)
→ Vector Storage
→ Similarity Search (Cosine Similarity)
→ Response Generation (Llama 3.2 via Ollama)
→ Final Answer with Timestamp

🔄 **Pipeline Overview**

Video Processing
Extract audio from uploaded video using ffmpeg

Transcription
Convert speech to text using Whisper

Embedding Creation
Convert text segments into vector embeddings

Search Mechanism
Compare query embedding with stored embeddings using cosine similarity

Answer Generation
LLM generates final response using most relevant segments

🛠️ **Project Tech Stack Architecture**
Backend: Flask (Python) — Handles server-side logic and API requests
Frontend: HTML, CSS, JavaScript — Builds user interface and interactions
Speech-to-Text: Whisper — Transcribes audio into text
Embeddings: bge-m3 (Ollama) — Creates vector representations
LLM: Llama 3.2 (Ollama) — Generates intelligent responses
Vector Search: Cosine Similarity (scikit-learn) — Finds semantic matches
Media Processing: ffmpeg — Handles audio/video processing
Data Handling: Pandas / In-memory storage — Manages processed data

🚀 **Features**
🎥 Upload any video format
🧠 Ask questions in natural language
⏱️ Get timestamp-based answers
🔍 Semantic search over video content
⚡ Fully local AI (no API required)
📂 Multiple video support

⚙️ **Requirements**
Python 3.8+
ffmpeg installed
Ollama installed and running
Required Models:
ollama pull bge-m3
ollama pull llama3.2

▶️ **Run Project**
git clone <your-repo-link>
cd vidrag
pip install -r requirements.txt
python app.py

🌐 **Open in Browser**
http://localhost:5000

💡 **Why This Project**

VidRAG demonstrates:

Real-world AI application of RAG
Video + NLP integration
Local AI deployment without APIs
Practical semantic search system

📌 **Future Improvements**
Database storage instead of RAM
Faster indexing system
Multi-language support

Cloud deployment
👨‍💻 **Author**

Mohammed Kupe
