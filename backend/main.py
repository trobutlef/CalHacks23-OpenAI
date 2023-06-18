from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from video_processing import process_video
from audio_processing import process_audio

import os
import json

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

@app.post("/getTimestamps/")
async def get_timestamps(hume_json): #takes in a JSON object: output from Hume Batch API

    # Parse to get inner JSONs that we need to filter through
    a_list = json.loads(hume_json["results"]["predictions"][0]["models"]["face"]["grouped_predictions"][0]["predictions"])

    # Filtering through to get relevant frames based on emotion name and score:
    filtered_list = list(
        filter(
            lambda dictionary: (dictionary['emotions']['name'] in ["Anxiety","Confusion","Disappointment","Distress","Doubt","Surprise (negative)"] and dictionary['emotions']['score'] > 0.8),
            a_list
        )
    )
    # filtered_list is a list of JSON objects for each corresponding frame

    timestamp_list = []

    for obj in filtered_list:
        timestamp_list.append(obj["time"])
