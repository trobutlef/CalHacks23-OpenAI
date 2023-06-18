import React from "react";
import "./AppStyles.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Cards from "./components/Cards";
import Upload from "./Upload";
import "./App.css";

export default function App() {
  return (
    /*<div>
      <Cards />
    </div>*/
    <div className="App">
      <header className="App-header">
        {<h1>OpenAI video transcription analysis</h1>}
        <Upload />
      </header>
    </div>
  );
}
