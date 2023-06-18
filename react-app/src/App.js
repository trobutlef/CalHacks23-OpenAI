import React from 'react';
import VideoUpload from './VideoUpload';
import VideoPlayer from './VideoPlayer';
import GetTimeStamps from './GetTimeStamps';
import axios from 'axios';
import { useState, useEffect } from 'react';

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
    })
    .then(response => {
      if (response.data.validation.includes("correct")) {
        alert("Your answer is correct!");
      } else {
        alert("Your answer is incorrect. " + response.data.validation);
      }
    });
  };

  return (
    <div>
      <VideoUpload />
      <VideoPlayer />
      <GetTimeStamps/>
      <h1>{currentQuestion}</h1>
      <input type="text" value={answer} onChange={e => setAnswer(e.target.value)} />
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}

export default App;