from fastapi import FastAPI, UploadFile, File

from video_processing import process_video
from audio_processing import process_audio

import os

app = FastAPI()

@app.post("/uploadvideo/")
async def upload_video(file: UploadFile = File(...)):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    video_path = os.path.join(current_dir, "videos", file.filename)
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())
    audio_path = process_video(video_path)
    transcript = process_audio(audio_path)
    return {"filename": file.filename, "transcript": transcript}
