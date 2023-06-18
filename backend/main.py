from fastapi import FastAPI, UploadFile, File
from aiohttp import ClientSession
from fastapi.middleware.cors import CORSMiddleware
import io
import moviepy.editor as mp


import numpy as np
from pydub import AudioSegment

import os

app = FastAPI()
#OPENAI_API_KEY = os.getenv("isk-O0pMhXMushdl6VZ4OqpLT3BlbkFJNIhHxeivBY1qakf2DwiF")  # your OpenAI API Key

origins = [
    "http://localhost:3000",  # React app address
    # other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/uploadvideo")
async def upload_video(video: UploadFile):

    print(video.filename)

    # CONVERT VIDEO TO AUDIO:
    my_clip = mp.VideoFileClip(video)
    my_clip.audio.write_audiofile(r"video_transcript.wav")

    # LOCATE SAVED AUDIO

    # USE WHISPER TO GET TRANSCRIPT OF AUDIO

    # SAVE TRANSCRIPT
    
    return {"filename": video.filename}
'''
@app.post("/transcribe/")
async def transcribe_audio(audio: UploadFile = File(...)):
    # read the uploaded file
    audio_bytes = await audio.read()
    
    async with ClientSession() as session:
        response = await session.post(
            "https://api.openai.com/v1/whisper/asr",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Openai-Organization": "org-tjIV1GRkqtPxOQkDXsPsm8J3",  # replace with your OpenAI org ID
                "Content-Type": "audio/wav",  # assuming the uploaded file is in wav format
            },
            data=audio_bytes,
        )
        response.raise_for_status()
        result = await response.json()

    return {"transcription": result}
'''

