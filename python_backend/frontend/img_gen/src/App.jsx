import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [width, setWidth] = useState(1024);
  const [height, setHeight] = useState(1024);
  const [steps, setSteps] = useState(20);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generatePoster = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('http://localhost:8000/generate-poster', {
        prompt,
        width,
        height,
        steps
      });
      
      setResult({
        imageUrl: `http://localhost:8000${response.data.image_url}`,
        prompt: response.data.prompt
      });
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Dido image Generator</h1>
        <p>Using consistent generation (fixed seed)</p>
      </header>

      <div className="controls-container">
        <div className="input-group">
          <label>Prompt:</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={3}
          />
        </div>

        <div className="params-grid">
          <div className="input-group">
            <label>Width:</label>
            <input
              type="number"
              value={width}
              onChange={(e) => setWidth(Number(e.target.value))}
            />
          </div>

          <div className="input-group">
            <label>Height:</label>
            <input
              type="number"
              value={height}
              onChange={(e) => setHeight(Number(e.target.value))}
            />
          </div>

          <div className="input-group">
            <label>Steps:</label>
            <input
              type="number"
              value={steps}
              onChange={(e) => setSteps(Number(e.target.value))}
            />
          </div>
        </div>

        <button 
          onClick={generatePoster}
          disabled={loading}
          className="generate-button"
        >
          {loading ? 'Generating...' : 'Generate Poster'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}

      {result && (
        <div className="result-container">
          <h2>Your image</h2>
          <div className="image-container">
            <img 
              src={result.imageUrl} 
              alt="Generated image" 
              className="generated-image"
            />
          </div>
          <div className="result-meta">
            <p><strong>Prompt:</strong> {result.prompt}</p>
            <a 
              href={result.imageUrl} 
              download="your_image.png"
              className="download-button"
            >
              Download Poster
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;