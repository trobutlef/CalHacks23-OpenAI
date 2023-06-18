#import os
#os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
from moviepy.editor import VideoFileClip

def process_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".wav")
    video.audio.write_audiofile(audio_path)
    return audio_path
