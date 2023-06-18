from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware



from video_processing import process_video
from audio_processing import process_audio

from hume import HumeBatchClient
from hume.models.config import FaceConfig

from datetime import timedelta

import os
import json
import credentials

import itertools

import re
import ffmpeg

import openai

from fastapi import Body


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # React app
    "http://localhost:8000",  # FastAPI server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

@app.get("/getuploadedvideo/")  # Add a get endpoint for uploadvideo
async def get_upload_video():
    global last_uploaded_filename
    return {"filename": last_uploaded_filename}
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

    # Get transcript
    with open("transcript.txt") as file:
        data = file.read().split('\n')

    # Filter out random integers and blank spaces:
    data[:] = [x for x in data if (x != '' and len(x)>10)]

    # Split into timestamps and content:
    t1,t2 = itertools.tee(data)
    even = itertools.islice(t1,0,None,2)
    odd = itertools.islice(t2,1,None,2)
    timestamps = list(even)
    content = list(odd)
    # Handle weird exception:
    last_timestamps = timestamps.pop()
    last_content = content.pop()
    content.append(last_timestamps)
    timestamps.append(last_content)

    print("list of timestamps: ", timestamps)

    print("list of content: ", content)

    # regex pattern for transcript's timestamps:
    pattern = r'(\d{2}:\d{2}:\d{2},\d{3})\s-->\s(\d{2}:\d{2}:\d{2},\d{3})'

    # start of timestamps''00:00:00,000'
    init_timestr = re.search(pattern, timestamps[0]).group(1)[:-4]
    h, m, s = init_timestr.split(':')
    init_timesec = int(h) * 3600 + int(m) * 60 + int(s)
    timestamps_edited = [init_timesec]

    # Convert timestamps into seconds
    for i in range(1,len(timestamps)):
        match = re.search(pattern, timestamps[i])

        start_time = match.group(1)[:-4]
        sh, sm, ss = start_time.split(':')
        start_timesec = int(sh) * 3600 + int(sm) * 60 + int(ss)
        
        end_time = match.group(2)[:-4]
        eh, em, es = end_time.split(':')
        end_timesec = int(eh) * 3600 + int(em) * 60 + int(es)

        time_diffsec = end_timesec - start_timesec

        prev_time = timestamps_edited[i-1]
        timestamps_edited.append(time_diffsec+ prev_time)

    print(timestamps_edited)

    # Combine timestamps list and content list into a dictionary:
    initial_dict = dict(zip(timestamps_edited, content))

    print(initial_dict)

    # Get final dictionary for shortened transcript:
    result_dict = {}
    for time in timestamp_list:
        go_on = True
        i=0
        while go_on:
            keys = list(initial_dict.keys())
            if time >= keys[i]:
                i+=1

            else:
                result_dict[keys[i-1]] = initial_dict[keys[i-1]]
                result_dict[keys[i]] = initial_dict[keys[i]]
                result_dict[keys[i+1]] = initial_dict[keys[i+1]]
                go_on = False

    print(result_dict)

    # Write to a txt file and save it
    with open('transcript_short.txt', 'w') as f:
        for key, value in result_dict.items():
            # create timedelta and convert it into string
            td_str = str(timedelta(seconds=key)) + ":"
            f.write('\n')
            f.write(td_str)
            f.write('\n')
            f.write(value)
    
    f.close()

    return timestamp_list


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
    return {"filename": file.filename}

#, "transcript": transcript}

#, "transcript": transcript}
    #current_dir = os.path.dirname(os.path.realpath(__file__))
    #video_path = os.path.join(current_dir, "recording", file.filename)
    #with open(video_path, "wb") as buffer:
    #    buffer.write(await file.read())
    #audio_path = process_video(video_path)
    #transcript = process_audio(audio_path)
    #return {"filename": file.filename, "transcript": transcript}

openai.api_key = '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'

@app.get("/generate_questions")
async def generate_questions():
    with open('transcript_reduced.txt', 'r') as file:
        transcript = file.read().replace('\n', '')
    
    # message = "\n\nHere is a document, based on its content, generate 3 thought provoking questions to reflect on the article: (answer in the language of the document)\n" + text

    # Generate a response using ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are a knowledgable scholar."},
            {"role": "user", "content": f"\n\nHere are parts of a transcript for video, the student seem to have difficulty understanding it, based on its content, generate a set of True/False questions to test his knowledge)\n{transcript}"},
        ],
    )
    
    questions = response.choices[0].message['content']
    
    return {"questions": questions}


@app.post("/validate_answer")
async def validate_answer(question: str = Body(...), answer: str = Body(...)):
    prompt = f"{question}\nAnswer: {answer}\nIs this answer correct?"
    response = openai.ChatCompletion.create(
      model="gpt-4-0613",
      messages=[
            {"role": "system", "content": "You are a knowledgable scholar."},
            {"role": "user", "content": f"\n\nIs this answer correct?\n{prompt}"},
        ],
    )
    
    validation = response.choices[0].message['content']
    
    return {"validation": validation}
