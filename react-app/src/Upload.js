import React, { useState } from "react";
import { Button, Form } from "react-bootstrap";
import axios from "axios";

function Upload() {
  const [file, setFile] = useState(null);

  const onFileChange = (e) => {
    console.log(e);
    setFile(e.target.files[0]);
  };

  const onUpload = async () => {
    if (!file) {
      console.log("No file selected");
      return;
    }

    const formData = new FormData();
    formData.append("audio", file);
    console.log(formData, file);
    const headers = { "Content-Type": "multipart/form-data" };
    // Replace with your backend API endpoint
    await axios
      .post("http://localhost:8000/uploadaudio", formData, { headers: headers })
      .then((response) => {
        console.log(response); // Here you get the response from your backend
      })
      .catch((error) => {
        console.error("Error uploading file: ", error);
      });
  };

  return (
    <div className="upload-section">
      <Form>
        <Form.Group>
          <Form.Label>Select an audio file</Form.Label>
          <Form.Control type="file" onChange={onFileChange} />
        </Form.Group>
        <Button variant="primary" onClick={onUpload}>
          Upload
        </Button>
      </Form>
    </div>
  );
}

export default Upload;
