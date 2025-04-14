import { useState, useRef, useEffect } from 'react';
import { CircularProgress } from '@mui/material';
import { CheckCircle, CloudUpload, Send, VolumeUp } from '@mui/icons-material';
import axios from 'axios';

export default function PDFExplainer() {
  const [file, setFile] = useState(null);
  const [fileUrl, setFileUrl] = useState('');
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadComplete, setUploadComplete] = useState(false);
  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  const API_URL = "http://localhost:8000";

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      const url = URL.createObjectURL(selectedFile);
      setFileUrl(url);
      setChatHistory([]);
      setUploadComplete(true);
    } else {
      alert('Please select a valid PDF file');
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

  const handleClearFile = () => {
    if (fileUrl) URL.revokeObjectURL(fileUrl);
    setFile(null);
    setFileUrl('');
    setChatHistory([]);
    setUploadComplete(false);
    fileInputRef.current.value = '';
  };

  const handleSubmitQuestion = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    if (!file) {
      alert('Please upload a PDF first');
      return;
    }
    if (!uploadComplete) {
      alert('Please upload the PDF to the server first');
      return;
    }

    const newChat = [...chatHistory, { sender: 'user', text: question }];
    setChatHistory(newChat);
    setQuestion('');
    setIsLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append('question', question);
      
      const response = await axios.post(`${API_URL}/ask-question`, formData.toString(), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      
      setChatHistory([...newChat, { sender: 'ai', text: response.data.answer }]);
    } catch (error) {
      console.error("Error:", error);
      setChatHistory([...newChat, { 
        sender: 'ai', 
        text: "Error: " + (error.response?.data?.detail || "Failed to get answer") 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const speakAnswer = async () => {
    if (chatHistory.length === 0) return;
    
    const lastAiMessage = [...chatHistory].reverse().find(msg => msg.sender === 'ai');
    if (!lastAiMessage) return;
    
    try {
      const formData = new URLSearchParams();
      formData.append('text', lastAiMessage.text);
      
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
    <div className="w-screen h-screen bg-[#222] text-[#fffce3] p-4 flex justify-center overflow-hidden">
      <div className="max-w-7xl w-full flex flex-col h-full">
        <h1 className="text-3xl font-bold my-4 text-center">PDF Explorer</h1>
        
        {/* Main content area with proper height constraints */}
        <div className="flex flex-1 gap-4" style={{ height: 'calc(100% - 80px)' }}>
          {/* Left panel - PDF controls */}
          <div className="w-64 flex flex-col">
            <div className="bg-[#1a1a1a] p-4 rounded-lg flex flex-col h-full">
              <div className="mb-4">
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={handleFileChange}
                  ref={fileInputRef}
                  className="hidden"
                  id="pdf-upload"
                />
                <label
                  htmlFor="pdf-upload"
                  className="block w-full bg-[#333] hover:bg-[#444] text-[#fffce3] py-2 px-4 rounded transition cursor-pointer text-center mb-2"
                >
                  {file ? 'Change PDF' : 'Select PDF'}
                </label>
                {file && (
                  <>
                    <button
                      onClick={handleUpload}
                      disabled={isUploading || uploadComplete}
                      className={`w-full mb-2 ${uploadComplete ? 'bg-[#4CAF50] hover:bg-[#45a049]' : 'bg-[#333] hover:bg-[#444]'} text-[#fffce3] py-2 px-4 rounded transition`}
                    >
                      {isUploading ? (
                        <span className="flex items-center justify-center">
                          <CircularProgress size={16} thickness={5} style={{ color: '#fffce3', marginRight: '8px' }} />
                          Uploading...
                        </span>
                      ) : uploadComplete ? (
                        <span className="flex items-center justify-center">
                          <CheckCircle style={{ fontSize: '1rem', marginRight: '8px' }} />
                          Uploaded
                        </span>
                      ) : (
                        'Upload PDF'
                      )}
                    </button>
                    <button
                      onClick={handleClearFile}
                      className="w-full bg-[#ff4444] hover:bg-[#ff5555] text-[#fffce3] py-2 px-4 rounded transition"
                    >
                      Clear PDF
                    </button>
                  </>
                )}
              </div>

              {file && (
                <div className="mt-auto">
                  <div className="p-3 bg-[#222] rounded mb-4">
                    <h3 className="font-medium mb-1">Current PDF:</h3>
                    <p className="text-sm text-[#fffce3]/80 truncate">{file.name}</p>
                    {uploadComplete && (
                      <div className="flex items-center mt-2 text-[#4CAF50] text-xs">
                        <CheckCircle style={{ fontSize: '1rem', marginRight: '4px' }} />
                        Ready for questions
                      </div>
                    )}
                  </div>
                  <div className="text-xs text-[#fffce3]/60">
                    <p>Ask questions about the PDF in the chat.</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Middle panel - PDF viewer */}
          <div className="flex-1 bg-[#1a1a1a] rounded-lg overflow-hidden flex flex-col">
            {fileUrl ? (
              <>
                <div className="p-2 bg-[#333] flex justify-between items-center">
                  <span className="text-sm font-medium truncate max-w-[70%]">
                    {file.name}
                  </span>
                  <span className="text-xs opacity-80">
                    Use Ctrl+F/Cmd+F to search
                  </span>
                </div>
                <div className="flex-1 overflow-auto">
                  <iframe
                    src={fileUrl}
                    title="PDF Viewer"
                    width="100%"
                    height="100%"
                    className="border-0"
                    style={{ minHeight: '100%' }}
                  />
                </div>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <div className="text-center p-8">
                  <svg
                    className="w-16 h-16 mx-auto mb-4 text-[#fffce3]/30"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1}
                      d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                    />
                  </svg>
                  <h3 className="text-lg font-medium mb-2">No PDF selected</h3>
                  <p className="text-[#fffce3]/60 mb-4">
                    Upload a PDF to start exploring its content
                  </p>
                  <label
                    htmlFor="pdf-upload"
                    className="inline-block bg-[#333] hover:bg-[#444] text-[#fffce3] py-2 px-6 rounded transition cursor-pointer"
                  >
                    Select PDF
                  </label>
                </div>
              </div>
            )}
          </div>

          {/* Right panel - Chat */}
          <div className="w-80 bg-[#1a1a1a] rounded-lg flex flex-col">
            <div className="p-3 bg-[#333] rounded-t-lg">
              <h3 className="font-medium">PDF Assistant</h3>
              <p className="text-xs text-[#fffce3]/60 mt-1">
                Ask questions about the document
              </p>
            </div>
            
            <div className="flex-1 overflow-y-auto p-3 space-y-3">
              {chatHistory.length === 0 ? (
                <div className="h-[97%] flex items-center justify-center">
                  <div className="text-center text-[#fffce3]/60 p-4">
                    <svg
                      className="w-10 h-10 mx-auto mb-3"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                      />
                    </svg>
                    <p>Ask your first question about the PDF</p>
                  </div>
                </div>
              ) : (
                chatHistory.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[90%] rounded-lg px-3 py-2 ${
                        message.sender === 'user'
                          ? 'bg-[#333] rounded-tr-none'
                          : 'bg-[#222] rounded-tl-none'
                      }`}
                    >
                      {message.text}
                    </div>
                  </div>
                ))
              )}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-[#222] rounded-lg rounded-tl-none px-3 py-2 max-w-[90%]">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 rounded-full bg-[#fffce3] animate-bounce"></div>
                      <div className="w-2 h-2 rounded-full bg-[#fffce3] animate-bounce delay-100"></div>
                      <div className="w-2 h-2 rounded-full bg-[#fffce3] animate-bounce delay-200"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            <form onSubmit={handleSubmitQuestion} className="p-3 border-t border-[#333]">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask about the PDF..."
                  className="flex-1 bg-[#333] text-[#fffce3] px-3 py-2 rounded focus:outline-none focus:ring-1 focus:ring-[#fffce3]/30"
                  disabled={!file || !uploadComplete}
                />
                <div className="flex">
                  <button
                    type="submit"
                    className="bg-[#333] hover:bg-[#444] text-[#fffce3] px-3 py-2 rounded transition disabled:opacity-50"
                    disabled={!file || !question.trim() || isLoading || !uploadComplete}
                  >
                    {isLoading ? (
                      <CircularProgress size={20} style={{ color: '#fffce3' }} />
                    ) : (
                      <Send style={{ fontSize: '1.25rem' }} />
                    )}
                  </button>
                  {chatHistory.some(msg => msg.sender === 'ai') && (
                    <button
                      type="button"
                      onClick={speakAnswer}
                      className="bg-[#333] hover:bg-[#444] text-[#fffce3] px-3 py-2 rounded transition ml-1"
                      title="Speak last answer"
                    >
                      <VolumeUp style={{ fontSize: '1.25rem' }} />
                    </button>
                  )}
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}