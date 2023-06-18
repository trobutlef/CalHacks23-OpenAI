from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from video_processing import process_video
from audio_processing import process_audio

import os

import credentials

app = FastAPI()

OPENAI_API_KEY = os.getenv(credentials.OPENAI_API_KEY)  # your OpenAI API Key

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
# @app.post("/uploadaudio")
# async def upload_audio(audio: UploadFile = File(...)):
#     # Get the filename before converting to an AudioSegment
#     filename = audio.filename

#     # read the uploaded file
#     audio_bytes = await audio.read()

#     # convert the bytes to a stream
#     audio_stream = io.BytesIO(audio_bytes)
    
#     # load the audio file
#     audio = AudioSegment.from_file(audio_stream)

#     # convert to mono and 8000 Hz sample rate
#     audio = audio.set_channels(1).set_frame_rate(8000)

#     # get the raw audio data as a bytestring
#     raw_data = audio.raw_data

#     # convert the raw audio data to Int16 format
#     audio_data = np.frombuffer(raw_data, dtype=np.int16)

#     # convert the audio data to little endian byte order
#     audio_data = audio_data.astype('<i2')

#     # convert back to bytes
#     audio_bytes = audio_data.tobytes()

#     # Save the audio file to the local filesystem
#     with open(f"test/{filename}", "wb") as f:
#         f.write(audio_bytes)

#     return {"filename": filename}


# @app.post("/transcribe")
# async def transcribe_audio(audio: UploadFile):
#     # read the uploaded file
#     audio_bytes = await audio.read()
    
#     async with ClientSession() as session:
#         response = await session.post(
#             "https://api.openai.com/v1/whisper/asr",
#             headers={
#                 "Authorization": f"Bearer {OPENAI_API_KEY}",
#                 "Openai-Organization": "org-tjIV1GRkqtPxOQkDXsPsm8J3",  # replace with your OpenAI org ID
#                 "Content-Type": "audio/wav",  # assuming the uploaded file is in wav format
#             },
#             data=audio_bytes,
#         )
#         response.raise_for_status()
#         result = await response.json()
#         print(result)
#     return {"transcription": result}

@app.post("/uploadaudio")
async def upload_audio(audio: UploadFile = File(...)):
    # Get the filename before converting to an AudioSegment
    filename = audio.filename

    # read the uploaded file
    audio_bytes = await audio.read()

    # convert the bytes to a stream
    audio_stream = io.BytesIO(audio_bytes)
    
    # load the audio file
    audio = AudioSegment.from_file(audio_stream)

    # convert to mono and 8000 Hz sample rate
    audio = audio.set_channels(1).set_frame_rate(8000)

    # get the raw audio data as a bytestring
    raw_data = audio.raw_data

    # convert the raw audio data to Int16 format
    audio_data = np.frombuffer(raw_data, dtype=np.int16)

    # convert the audio data to little endian byte order
    audio_data = audio_data.astype('<i2')

    # convert back to bytes
    audio_bytes = audio_data.tobytes()

    # Save the audio file to the local filesystem
    with open(f"test/{filename}", "wb") as f:
        f.write(audio_bytes)
        
    # Start a new ClientSession for making HTTP requests
    async with ClientSession() as session:
        # Send a POST request to the Whisper ASR API
        response = await session.post(
            "https://api.openai.com/v1/whisper/asr",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Openai-Organization": "org-tjIV1GRkqtPxOQkDXsPsm8J3",  # replace with your OpenAI org ID
                "Content-Type": "audio/wav",  # assuming the uploaded file is in wav format
            },
            data=audio_bytes,
        )
        # Raise an error if the request was not successful
        response.raise_for_status()
        # Get the response data as JSON
        result = await response.json()

    return {"filename": filename, "transcription": result}

@app.post("/uploadvideo/")
async def upload_video(file: UploadFile = File(...)):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    video_path = os.path.join(current_dir, "videos", file.filename)
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())
    audio_path = process_video(video_path)
    transcript = process_audio(audio_path)
    return {"filename": file.filename, "transcript": transcript}
