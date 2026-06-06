# 🎬 VidRAG

> An AI-powered system that lets you upload any video and ask questions about it — getting answers with **exact timestamps** of where the topic is discussed.

Built as a personal project using **Retrieval-Augmented Generation (RAG)** with fully local AI models — no API keys, no cloud, runs 100% on your machine.

---


## 🧠 How It Works

This project converts videos into a searchable knowledge base using a 4-stage pipeline:

```
Video File
    │
    ▼
[ ffmpeg ]  ──────────────────  Extract audio → MP3
    │
    ▼
[ Whisper large-v2 ]  ────────  Transcribe + Translate (Hindi → English)
    │                           Output: text segments with timestamps
    ▼
[ bge-m3 via Ollama ]  ───────  Convert each segment into a vector embedding
    │                           Output: stored in memory (pandas DataFrame)
    ▼
[ User asks a question ]
    │
    ▼
[ bge-m3 ]  ──────────────────  Embed the question into a vector
    │
    ▼
[ Cosine Similarity ]  ───────  Find top 5 most relevant segments
    │
    ▼
[ Llama 3.2 via Ollama ]  ────  Generate a human answer with timestamps
    │
    ▼
"Go to Video 3 at 08:24 for the box model explanation"
```

This approach is called **RAG (Retrieval-Augmented Generation)** — instead of the LLM memorizing content, it reads the relevant segments fresh every time, making answers accurate and grounded.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Audio Extraction | ffmpeg |
| Speech-to-Text | OpenAI Whisper large-v2 |
| Translation | Whisper `task="translate"` (Hindi → English) |
| Embeddings Model | bge-m3 (via Ollama) |
| LLM | Llama 3.2 (via Ollama) |
| Vector Search | Cosine Similarity (scikit-learn) |
| Data Storage | pandas + RAM (session-based) |
| Web Framework | Flask (Python) |
| Frontend | HTML, CSS, Vanilla JavaScript|

---

---

## ⚙️ Prerequisites

Make sure you have these installed before running:

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/download.html)
- [Ollama](https://ollama.com/download)

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/nikhilsai2005/VidRAG.git
cd video-rag-assistant
```

### 2. Install Python dependencies

```bash
pip install flask werkzeug openai-whisper numpy pandas scikit-learn joblib requests
```

### 3. Install ffmpeg

**Windows:**
```bash
winget install ffmpeg
```


### 4. Install and start Ollama

Download from [ollama.com](https://ollama.com/download), then pull the required models:

```bash
ollama pull bge-m3
ollama pull llama3.2
```

### 5. Start Ollama server

```bash
ollama serve
```

> Keep this running in a separate terminal while using the app.

---

## ▶️ Running the App

```bash
python app.py
```

Then open your browser and go to:

```
http://localhost:5000
```

---

## 🖥️ Using the Web Interface

**Step 1 — Upload a video**
Drag and drop any video file MP4, MKV, AVI, MOV, WEBMor MP3 onto the upload zone. The app will show a live 4-step progress tracker:

```
Uploading → Converting → Transcribing → Embedding
```

**Step 2 — Wait for processing**
Whisper transcribes the audio in the background. This may take time depending on video length and your gpu/cpu.

**Step 3 — Ask questions**
Once processing is done, the chat panel unlocks. Type any question about the video content and get an answer with the exact timestamp.

**Upload more videos**
You can keep uploading more videos. Each new video's content is added to the knowledge base — queries search across **all uploaded videos** at once.


---

## 🔬 Key Concepts Used

**RAG (Retrieval-Augmented Generation)**
Instead of fine-tuning a model on video content, we retrieve the most relevant text chunks at query time and pass them as context to the LLM. This keeps answers accurate and up to date.

**Vector Embeddings**
Text is converted into high-dimensional vectors (numbers) that capture semantic meaning. Similar meanings = similar vectors = high cosine similarity score.

**Cosine Similarity**
A mathematical measure of how similar two vectors are, regardless of their size. Used to find the top 5 most relevant video segments for any query.

**Whisper Translation**
By using `task="translate"` instead of `task="transcribe"`, Whisper converts Hindi speech directly to English text — making the embeddings work in English space without a separate translation step.

---

👨‍💻 Author
-Mohammed Asif Kupe

---
