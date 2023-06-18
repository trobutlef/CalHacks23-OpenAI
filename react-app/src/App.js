import React from "react";
import VideoUpload from "./VideoUpload";
import VideoPlayer from "./VideoPlayer";
import GetTimeStamps from "./GetTimeStamps";
import {
  Box,
  Container,
  Grid,
  Typography,
  createTheme,
  ThemeProvider,
} from "@mui/material";

import axios from 'axios';
import { useState, useEffect } from 'react';

const theme = createTheme({
  palette: {
    background: {
      default: "#f0f0f0", // You can set your desired color here.
    },
  },
});

function App() {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [answer, setAnswer] = useState("");

  useEffect(() => {
    axios.get('http://localhost:8000/generate_questions')
      .then(response => {
        setQuestions(response.data.questions.split('\n'));
        setCurrentQuestion(response.data.questions.split('\n')[0]);
      });
  }, []);

  const handleSubmit = () => {
    axios.post('http://localhost:8000/validate_answer', {
      question: currentQuestion,
      answer: answer
    }, {
      withCredentials: true,
    })
    .then(response => {
      console.log(response.data.validation)
      if (response.data.validation.includes("correct")) {
        alert("Your answer is correct!");
      } else {
        alert("Your answer is incorrect. " + response.data.validation);
      }
    });
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="lg">
        <Typography variant="h2" align="center" gutterBottom>
          Video Analysis to Text with OpenAI
        </Typography>
        <Box my={4}>
          <Grid container spacing={4} direction="column" alignItems="center">
            <Grid item xs={12} sm={8}>
              <VideoUpload />
            </Grid>
            <Grid item xs={12} sm={8}>
              <GetTimeStamps />
            </Grid>
          </Grid>
          <h1>{currentQuestion}</h1>
          <input type="text" value={answer} onChange={e => setAnswer(e.target.value)} />
          <button onClick={handleSubmit}>Submit</button>
        </Box>
        
      </Container>
    </ThemeProvider>
    
  );
}

export default App;

