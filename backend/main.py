from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles

from video_processing import process_video
from audio_processing import process_audio

from hume import HumeBatchClient
from hume.models.config import FaceConfig

import os
import json
import credentials

import re
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

@app.post("/getTimestamps/")
async def get_timestamps():

    print("getting timestamps...")

    # call Hume's Facial Recognition API with a local video file, to get a json file downloaded
    '''
    client = HumeBatchClient(credentials.HUME_API_KEY)
    urls = []
    config = FaceConfig()
    job = client.submit_job(urls, [config], files=["/Users/zztee/CalHacks23-OpenAI/backend/videos/hume_test.mov"])

    print(job)
    print("Running...")

    details = job.await_complete()
    job.download_predictions("predictions.json")
    print("Predictions downloaded to predictions.json")

    '''
    # read downloaded JSON file
    with open('predictions.json') as user_file:
        hume_json = user_file.read()

    # transform JSON into Python object
    a_list = json.loads(hume_json)

    print("a_list created")

    # Parse to get inner JSONs that we need to filter through
    b_list = a_list[0]["results"]["predictions"][0]["models"]["face"]["grouped_predictions"][0]["predictions"]

    print("b_list created!")

    # Filtering through to get relevant frames based on emotion name and score:

    def filter_func(predictions_json):
        result = False 

        for i in range(len(predictions_json["emotions"])):
            if predictions_json["emotions"][i]["name"] in ["Anxiety","Confusion","Disappointment","Distress","Doubt","Surprise (negative)"] and predictions_json["emotions"][i]["score"] >= 0.8:
                result = True
        
        return result

    filtered_list = list(
        filter(
            filter_func,
            # lambda dictionary: (dictionary['emotions']['name'] in ["Anxiety","Confusion","Disappointment","Distress","Doubt","Surprise (negative)"] and dictionary['emotions']['score'] > 0.8),
            b_list
        )
    )
    # filtered_list is a list of JSON objects for each corresponding frame

    timestamp_list = []

    for obj in filtered_list:
        timestamp_list.append(obj["time"])

    print("timestamp_list: ", timestamp_list)

    return timestamp_list

    # Get transcript


    # Get timestamp_list

    
@app.post("/uploadrecording/")
async def upload_recording(file: UploadFile = File(...)):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    recording_path = os.path.join(current_dir, "recording", file.filename)

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
