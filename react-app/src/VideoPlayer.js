import React, { useState, useEffect } from "react";
import { useReactMediaRecorder } from "react-media-recorder";
import axios from "axios";

function VideoPlayer() {
  const [videoSrc, setVideoSrc] = useState(null);
  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ video: true, mimeType: "video/webm" }); // Ensure the mimeType is set to mp4

  useEffect(() => {
    const videoUrl =
      "http://localhost:8000/videos/Distributed Systems - Fast Tech Skills.mp4";
    setVideoSrc(videoUrl);
  }, []);

  const handlePlay = () => {
    startRecording();
  };

  const handlePause = async () => {
    stopRecording();
    // Now we want to send the videoBlob to the backend
    let blob = await fetch(mediaBlobUrl).then((r) => r.blob());

    // Use form data to build up the file
    let data = new FormData();
    data.append("file", blob, "recording.webm");

    axios
      .post("http://localhost:8000/uploadrecording/", data)
      .then((res) => console.log(res))
      .catch((err) => console.error(err));
  };

  console.log(status, mediaBlobUrl);

  return (
    <div>
      <video
        src={videoSrc}
        onPlay={handlePlay}
        onPause={handlePause}
        controls
      />
    </div>
  );
}

export default VideoPlayer;