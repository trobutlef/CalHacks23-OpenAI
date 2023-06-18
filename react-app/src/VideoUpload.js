import React, { useState } from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import { styled } from "@mui/system";
import VideoPlayer from "./VideoPlayer";
import {
  Box,
  Container,
  Grid,
  Typography,
  createTheme,
  ThemeProvider,
} from "@mui/material";

const Input = styled("input")({
  display: "none",
});

const TranscriptionBox = styled(Box)({
  border: "1px solid #c4c4c4",
  borderRadius: "8px",
  padding: "16px",
  height: "300px",
  overflow: "auto",
  whiteSpace: "pre-wrap",
  marginTop: "16px",
});

function VideoUpload() {
  const [transcription, setTranscription] = useState(null);
  const [uploadCounter, setUploadCounter] = useState(0);

  const uploadVideo = (event) => {
    const file = event.target.files[0];

    const formData = new FormData();
    formData.append("file", file);
    axios
      .post("http://localhost:8000/uploadvideo/", formData, {
        withCredentials: true,
      })
      .then((response) => {
        console.log(response);
        setTranscription(response.data.transcript);
        setUploadCounter(uploadCounter + 1); // Increment the uploadCounter state
      })
      .catch((error) => {
        console.error("Error uploading file: ", error);
      });
  };

  return (
    <Stack
      direction="column"
      alignItems="center"
      justifyContent="center"
      spacing={2}
    >
      <label htmlFor="contained-button-file">
        <Input
          accept="video/*"
          id="contained-button-file"
          type="file"
          onChange={uploadVideo}
        />
        <Button variant="contained" component="span">
          Upload
        </Button>
      </label>

      <Grid item xs={12} sm={8}>
        <VideoPlayer uploadCounter={uploadCounter} />
      </Grid>

      <Typography variant="subtitle1">Transcription:</Typography>
      <TranscriptionBox>
        {transcription
          ? transcription
          : "Upload the video to see the transcription."}
      </TranscriptionBox>
    </Stack>
  );
}

export default VideoUpload;
