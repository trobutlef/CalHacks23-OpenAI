from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


from video_processing import process_video
from audio_processing import process_audio

import os
import ffmpeg

app = FastAPI()

# CORS middleware settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/videos", StaticFiles(directory="videos"), name="videos")
# Assume last_uploaded_filename is a global variable to store the last uploaded file name
last_uploaded_filename = None

@app.post("/uploadvideo/")
async def upload_video(file: UploadFile = File(...)):
    global last_uploaded_filename
    current_dir = os.path.dirname(os.path.realpath(__file__))
    video_path = os.path.join(current_dir, "videos", file.filename)
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())
    audio_path = process_video(video_path)
    transcript = process_audio(audio_path)
    last_uploaded_filename = file.filename  # Update last uploaded file name
    return {"filename": file.filename, "transcript": transcript}

@app.get("/uploadvideo/")  # Add a get endpoint for uploadvideo
async def get_upload_video():
    global last_uploaded_filename
    return {"filename": last_uploaded_filename}

@app.post("/uploadrecording/")
async def upload_recording(file: UploadFile = File(...)):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    recording_path = os.path.join(current_dir, "recording", file.filename)
    #print(file.filename)
    # Save the webm file
    webm_path = recording_path
    with open(webm_path, "wb") as buffer:
        buffer.write(await file.read())

    # Convert to mp4
    recording_path = recording_path.rstrip(".webm")
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