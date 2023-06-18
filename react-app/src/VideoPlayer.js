import React, { useState, useEffect } from "react";
import { useReactMediaRecorder } from "react-media-recorder";
import axios from "axios";
//import { Box, Typography, Divider } from "@mui/material";
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
  const [filename, setFileName] = useState(null);
  const [transcription, setTranscription] = useState(null);
  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ video: true, mimeType: "video/webm" });

  useEffect(() => {
    axios.get("http://localhost:8000/uploadvideo/").then((res) => {
      console.log(res);
      setFileName(response.data.filename); // Assuming transcript is returned in response data
    });
    const videoUrl = `http://localhost:8000/videos/${filename}`;
    setVideoSrc(videoUrl);
  }, []);

  /*
  axios
    .post("http://localhost:8000/uploadvideo/", data)
    .then((res) => {
      console.log(res);
      setTranscription(res.data.transcript); // Assuming transcript is returned in response data
    })
    .catch((err) => console.error(err));
*/
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
        //setTranscription(res.data.transcript); // Assuming transcript is returned in response data
      })
      .catch((err) => console.error(err));
  };

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
      </Box>
      <Divider sx={{ mt: 2, mb: 2 }} />
      <Typography variant="h6" sx={{ mt: 2 }}>
        Status: {status}
      </Typography>
    </Box>
  );
}

export default VideoPlayer;
