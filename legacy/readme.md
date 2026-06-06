
These are the original standalone scripts written before the web application was built.
Each script was a manual step in the pipeline that is now fully automated by app.py.

How It Worked Before (Manual Pipeline)
Step 1 → python process_video.py      # video → mp3
Step 2 → python mp3_to_text.py        # mp3 → json transcripts
Step 3 → python process_incoming.py   # ask a question in terminal

Files
FileWhat it didprocess_video.pyConverted video files to MP3 using ffmpegmp3_to_text.pyTranscribed MP3 to JSON with timestamps using Whisperprocess_incoming.pyCLI tool to ask questions and get answers in terminalread_chunks.pyDebug tool to print saved chunks from embeddings.joblibprompt.txtSample prompt used during testingresponse.txtSample LLM response during testing


All of this is now handled automatically by app.py when a video is uploaded through the web interface.