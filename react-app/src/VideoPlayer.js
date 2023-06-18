import React, { useState, useEffect } from "react";
import { useReactMediaRecorder } from "react-media-recorder";
import axios from "axios";
import { styled } from "@mui/system";
import {
  Box,
  Container,
  Grid,
  Typography,
  createTheme,
  Divider,
  ThemeProvider,
} from "@mui/material";

let counter = 0;

const TranscriptionBox = styled(Box)({
  border: "1px solid #c4c4c4",
  borderRadius: "8px",
  padding: "16px",
  height: "300px",
  overflow: "auto",
  whiteSpace: "pre-wrap",
});

function VideoPlayer() {
  const [videoSrc, setVideoSrc] = useState(null);
  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ video: true, mimeType: "video/webm" });

  useEffect(() => {
    axios.get("http://localhost:8000/getuploadedvideo/").then((res) => {
      const filename = res.data.filename;
      if (filename) {
        const encodedFilename = encodeURIComponent(filename);
        const videoUrl = `http://localhost:8000/videos/${encodedFilename}`;
        setVideoSrc(videoUrl);
      }
    });
    console.log("videoSrc:", videoSrc);
  }, []);

  const handlePlay = () => {
    startRecording();
  };

  const handlePause = async () => {
    stopRecording();
    let blob = await fetch(mediaBlobUrl).then((r) => r.blob());
    let data = new FormData();
    data.append("file", blob, `recording${counter++}.webm`);

    axios
      .post("http://localhost:8000/uploadrecording/", data)
      .then((res) => {
        console.log(res);
      })
      .catch((err) => console.error(err));
  };
  console.log(videoSrc);
  return (
    <Box sx={{ mt: 3, mb: 3 }}>
      <Typography variant="h6">Your video:</Typography>
      <Box sx={{ display: "flex", mt: 2 }}>
        <video
          style={{ width: "60%", height: "auto" }}
          src={videoSrc}
          onPlay={handlePlay}
          onPause={handlePause}
          controls
        />
        {!videoSrc && (
          <Typography variant="body1">No video uploaded yet.</Typography>
        )}
      </Box>
      <Divider sx={{ mt: 2, mb: 2 }} />
      <Typography variant="h6" sx={{ mt: 2 }}>
        Status: {status}
      </Typography>
    </Box>
  );
}

export default VideoPlayer;
