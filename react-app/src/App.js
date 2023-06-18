import React from 'react';
import VideoUpload from './VideoUpload';
import VideoPlayer from './VideoPlayer';
import GetTimeStamps from './GetTimeStamps';

function App() {
  return (
    <div className="App">
      <VideoUpload />
      <VideoPlayer />
      <GetTimeStamps/>
    </div>
  );
}

export default App;
