import React from 'react';
import axios from 'axios';
import { Button } from 'react-bootstrap';

function GetTimeStamps() {
  const handleClick = async () => {
    // Make a GET request to the FastAPI endpoint that runs the script
    axios.post('http://localhost:8000/getTimestamps/')
    .then((response) => {
        console.log(response); // Here you get the response from your backend
      })
      .catch((error) => {
        console.error("Error uploading file: ", error);
      });
    }

  return (
    <div>
      <h2>Get timestamps</h2>
      <Button onClick={handleClick}> Click me </Button>
    </div>
  );
}

export default GetTimeStamps;