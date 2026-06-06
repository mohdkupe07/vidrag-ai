import os, uuid, subprocess, threading
import numpy as np
import pandas as pd
import whisper
import requests

from flask import Flask, render_template, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# ── CONFIG ─────────────────────────────
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".mp3"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── STATE ───────────────────────────────
session_df = None
uploaded_videos = []
job_status = {}
whisper_model = None

# ⚡ SPEED CACHE
embedding_matrix = None

# ── EMBEDDING ──────────────────────────
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embedding(text_list):
    if not text_list:
        return np.array([])
    return embed_model.encode(text_list, batch_size=16, show_progress_bar=False)

# ── WHISPER ─────────────────────────────
def get_whisper():
    global whisper_model
    if whisper_model is None:
        whisper_model = whisper.load_model("base")
    return whisper_model

# ── LLM ────────────────────────────────
def llm_inference(prompt):
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3.2", "prompt": prompt, "stream": False},
            timeout=180,
        )
        return r.json()["response"]
    except Exception as e:
        return f"LLM error: {str(e)}"

# ── PIPELINE ───────────────────────────
def process_video(job_id, video_path, video_title, video_number):
    global session_df, embedding_matrix

    mp3_path = None

    def update(status, message):
        job_status[job_id] = {
            "status": status,
            "message": message,
            "title": video_title
        }

    try:
        update("processing", "🎬 Extracting audio...")

        mp3_path = video_path.rsplit(".", 1)[0] + ".mp3"

        subprocess.run(
            ["ffmpeg", "-y", "-i", video_path, "-q:a", "0", "-map", "a", mp3_path],
            capture_output=True
        )

        if not os.path.exists(mp3_path):
            mp3_path = video_path

        update("processing", "🎙️ Transcribing...")

        model = get_whisper()
        result = model.transcribe(mp3_path)

        chunks = []

        for seg in result.get("segments", []):
            text = seg.get("text", "").strip()

            if len(text.split()) < 3:
                continue

            chunks.append({
                "number": str(video_number),
                "title": video_title,
                "start": float(seg["start"]),
                "end": float(seg["end"]),
                "text": text
            })

        if not chunks:
            update("error", "No speech detected")
            return

        update("processing", "🔢 Embedding...")

        texts = [c["text"] for c in chunks]
        embeddings = create_embedding(texts)

        for i in range(len(chunks)):
            chunks[i]["embedding"] = embeddings[i]

        new_df = pd.DataFrame(chunks)

        if session_df is None:
            session_df = new_df
        else:
            session_df = pd.concat([session_df, new_df], ignore_index=True)

        # ⚡ CACHE UPDATE (FAST SEARCH ENABLE)
        embedding_matrix = np.vstack(session_df["embedding"])

        for v in uploaded_videos:
            if v["job_id"] == job_id:
                v["status"] = "done"
                v["chunks"] = len(chunks)

        update("done", "✅ Ready")

    except Exception as e:
        update("error", str(e))

# ── ROUTES ─────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["video"]

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTS:
        return jsonify({"error": "Unsupported format"}), 400

    job_id = str(uuid.uuid4())[:8]
    safe = secure_filename(file.filename)

    path = os.path.join(UPLOAD_FOLDER, f"{job_id}_{safe}")
    file.save(path)

    video_number = len(uploaded_videos) + 1
    title = os.path.splitext(safe)[0]

    uploaded_videos.append({
        "job_id": job_id,
        "title": title,
        "number": video_number,
        "status": "queued",
        "chunks": 0
    })

    job_status[job_id] = {"status": "queued", "message": "Starting..."}

    threading.Thread(
        target=process_video,
        args=(job_id, path, title, video_number),
        daemon=True
    ).start()

    return jsonify({"job_id": job_id, "title": title})

@app.route("/status/<job_id>")
def status(job_id):
    return jsonify(job_status.get(job_id, {}))

@app.route("/videos")
def videos():
    total = len(session_df) if session_df is not None else 0
    return jsonify({
        "videos": uploaded_videos,
        "total_chunks": total
    })

# ── ⚡ FAST ASK (MAIN FIX) ─────────────────
@app.route("/ask", methods=["POST"])
def ask():
    global session_df, embedding_matrix

    if session_df is None:
        return jsonify({"error": "No data"}), 400

    query = request.json.get("query", "")

    q_emb = create_embedding([query])[0]

    # ⚡ FAST PATH
    if embedding_matrix is None:
        embedding_matrix = np.vstack(session_df["embedding"])

    # 🚀 FASTEST SEARCH (DOT PRODUCT)
    sims = embedding_matrix @ q_emb

    top_idx = np.argsort(sims)[::-1][:6]
    top = session_df.iloc[top_idx]

    chunk_json = top[["title", "number", "start", "end", "text"]].to_dict("records")

    prompt = f"""
Answer from transcript only:

Question: {query}

Data:
{chunk_json}
"""

    answer = llm_inference(prompt)

    return jsonify({"answer": answer})

# ── RUN ───────────────────────────────
if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)