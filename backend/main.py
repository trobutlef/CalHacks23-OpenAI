from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles

from video_processing import process_video
from audio_processing import process_audio

import os
import ffmpeg

app = FastAPI()

app.mount("/videos", StaticFiles(directory="videos"), name="videos")

@app.post("/uploadvideo/")
async def upload_video(file: UploadFile = File(...)):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    video_path = os.path.join(current_dir, "videos", file.filename)
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())
    audio_path = process_video(video_path)
    transcript = process_audio(audio_path)
    return {"filename": file.filename, "transcript": transcript}

@app.post("/uploadrecording/")
async def upload_recording(file: UploadFile = File(...)):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    recording_path = os.path.join(current_dir, "recordings", file.filename)

    # Save the webm file
    webm_path = recording_path + ".webm"
    with open(webm_path, "wb") as buffer:
        buffer.write(await file.read())

    # Convert to mp4
    mp4_path = recording_path + ".mp4"
    ffmpeg.input(webm_path).output(mp4_path).run()

    # Process the mp4 file
    #audio_path = process_video(mp4_path)
    #transcript = process_audio(audio_path)
    return {"filename": file.filename}#, "transcript": transcript}
    #current_dir = os.path.dirname(os.path.realpath(__file__))
    #video_path = os.path.join(current_dir, "recording", file.filename)
    #with open(video_path, "wb") as buffer:
    #    buffer.write(await file.read())
    #audio_path = process_video(video_path)
    #transcript = process_audio(audio_path)
    #return {"filename": file.filename, "transcript": transcript}