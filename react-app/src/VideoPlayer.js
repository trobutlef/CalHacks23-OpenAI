import React, { useRef, useState, useEffect } from 'react';
import Webcam from 'react-webcam';

function VideoPlayer() {
  const webcamRef = useRef(null);
  const [recording, setRecording] = useState(false);
  const [videoSrc, setVideoSrc] = useState(null);

  useEffect(() => {
    // Replace this with the URL of your backend endpoint that serves the video file
    const videoUrl = 'http://localhost:8000/videos/Distributed Systems - Fast Tech Skills.mp4';
    setVideoSrc(videoUrl);
  }, []);

  const handlePlay = () => {
    webcamRef.current.startRecording();
    setRecording(true);
  };

  const handlePause = () => {
    webcamRef.current.stopRecording();
    setRecording(false);
    const videoBlob = webcamRef.current.getRecording();
    console.log(videoBlob);
    // Can send the videoBlob to your backend for further processing
  };

  console.log(webcamRef);

  return (
    <div>
      <Webcam audio={false} ref={webcamRef} />
      {videoSrc && <video src={videoSrc} onPlay={handlePlay} onPause={handlePause} controls />}
    </div>
  );
}

export default VideoPlayer;
