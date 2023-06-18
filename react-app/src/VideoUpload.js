import React from 'react';
import axios from 'axios';

function VideoUpload() {
  const uploadVideo = (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);
    axios.post('http://localhost:8000/uploadvideo/', formData)
    .then((response) => {
        console.log(response); // Here you get the response from your backend
      })
      .catch((error) => {
        console.error("Error uploading file: ", error);
      });
  };

  return (
    <div>
      <input type="file" onChange={uploadVideo} />
    </div>
  );
}

export default VideoUpload;
