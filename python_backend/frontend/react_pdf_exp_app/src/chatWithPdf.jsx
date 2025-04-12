import React, { useState, useRef, useEffect } from 'react';
import { CircularProgress } from '@mui/material';
import { CheckCircle, CloudUpload, Send, VolumeUp } from '@mui/icons-material';
import './chatWithPdf.css';
import axios from 'axios';

function ChatWithPDF() {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadComplete, setUploadComplete] = useState(false);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [isAnswerLoading, setIsAnswerLoading] = useState(false);
  const fileInputRef = useRef(null);
  const speechSynth = useRef(window.speechSynthesis);

  const API_URL = "http://localhost:8000";

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setUploadComplete(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setIsUploading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await axios.post(`${API_URL}/upload-pdf`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      if (response.data.status === 'success') {
        setUploadComplete(true);
      } else {
        alert('Upload failed: ' + response.data.message);
      }
    } catch (error) {
      alert('Error uploading file: ' + error.message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleQuestionSubmit = async () => {
    if (!question.trim()) {
      alert("Please enter a question");
      return;
    }
  
    setIsAnswerLoading(true);
    setAnswer('');
    
    try {
      // Create URL-encoded form data
      const formData = new URLSearchParams();
      formData.append('question', question);
      
      const response = await axios.post(`${API_URL}/ask-question`, formData.toString(), { // Note .toString()
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      
      setAnswer(response.data.answer);
    } catch (error) {
      console.error("Full error details:", {
        error: error.message,
        request: error.config,
        response: error.response?.data
      });
      setAnswer("Error: " + (error.response?.data?.detail || "Failed to get answer"));
    } finally {
      setIsAnswerLoading(false);
    }
  };
  const speakAnswer = async () => {
    if (!answer) return;
    
    try {
      const formData = new URLSearchParams();
      formData.append('text', answer);
      
      await axios.post(`${API_URL}/speak-text`, formData.toString(), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
    } catch (error) {
      console.error("Speech error:", error);
      alert("Failed to speak: " + (error.response?.data?.detail || error.message));
    }
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <h1 className="app-title">PDF Chat Assistant</h1>
        
        <div className="upload-section">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".pdf"
            style={{ display: 'none' }}
          />
          
          <button
            className="upload-btn"
            onClick={() => fileInputRef.current.click()}
          >
            <CloudUpload className="icon" />
            {file ? file.name : 'Choose PDF File'}
          </button>
          
          <button
            className={`submit-btn ${!file ? 'disabled' : ''}`}
            onClick={handleUpload}
            disabled={!file}
          >
            Upload File
          </button>
          
          <div className="status-indicator">
            {isUploading && (
              <>
                <CircularProgress size={24} thickness={5} />
                <span>Uploading...</span>
              </>
            )}
            {uploadComplete && !isUploading && (
              <>
                <CheckCircle className="success-icon" />
                <span>Ready for questions</span>
              </>
            )}
          </div>
        </div>
        
        <div className="chat-section">
          <div className="question-input">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question about the document..."
              disabled={!uploadComplete}
            />
            <button
              className="ask-btn"
              onClick={handleQuestionSubmit}
              disabled={!uploadComplete || !question.trim() || isAnswerLoading}
            >
              {isAnswerLoading ? <CircularProgress size={20} /> : <Send className="icon" />}
            </button>
          </div>
          
          {answer && (
            <div className="answer-container">
              <div className="answer-content">
                {answer}
              </div>
              <button className="speak-btn" onClick={speakAnswer}>
                <VolumeUp className="icon" />
                Speak Answer
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ChatWithPDF;