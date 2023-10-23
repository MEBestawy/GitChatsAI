import React, { useState } from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import HomePage from "./HomePage";
import MyModel from "./MyModel";
import 'tailwindcss/tailwind.css';

function App() {
  const [repoUrl, setRepoUrl] = useState('');

  const handleRepoUrlChange = (event) => {
    setRepoUrl(event.target.value);
  };

  const handleTrainModel = () => {
    // You can add logic here to send the repo URL to the server for training the model.
  };

  return (
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/models" element={<MyModel />} />
        </Routes>
      </Router>
  );
}

export default App;
