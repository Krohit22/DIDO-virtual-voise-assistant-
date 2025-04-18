import React, { useState } from 'react';
import axios from 'axios';

function ImgGen() {
  const [width, setWidth] = useState(1024);
  const [height, setHeight] = useState(1024);
  const [steps, setSteps] = useState(20);
  
  const [prompt, setPrompt] = useState('');
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

  // New function to handle download
  const handleDownload = async () => {
    try {
      const response = await fetch(result.imageUrl);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = 'generated_image.png'; // You can make this dynamic if you want
      document.body.appendChild(a);
      a.click();
      
      // Cleanup
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('Failed to download image');
    }
  };

  return (
    <div className="w-screen h-screen bg-[#222] flex flex-col overflow-auto">
      {/* Top heading */}
      <div className="flex justify-center pt-12">
        <h1 className="text-4xl font-bold text-[#fffce3] text-center my-1">Image Generator</h1>
      </div>
      {result && (
          <>
              <img 
                src={result.imageUrl} 
                alt="Generated image" 
                className="w-[30%] mx-auto rounded-lg shadow-sm mt-8"
                />
            <div className="mt-4 mx-auto">
              <button
                onClick={handleDownload}
                className="cursor-pointer inline-flex items-center px-4 py-2 text-sm rounded-md shadow-sm text-[#fffce3] bg-[#222] focus:outline-none font-semibold border border-[#fffce3] hover:text-[#222] hover:bg-[#fffce3] transition-colors duration-200"
              >
                Download Image
              </button>
            </div>
          </>
        )}

        {error && (
          <div className="border-l-4 border-red-400 p-4 mb-8 mx-auto mt-8">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">Error: {error}</p>
              </div>
            </div>
          </div>
        )}

      {/* Bottom input form */}
      <div className="flex-1 flex items-end justify-center pb-6">
        <div className="w-full max-w-2xl px-4">
          <form className="relative">
            <input 
              disabled={loading}
              type="text" 
              onChange={(e)=>{setPrompt(e.target.value)}}
              placeholder="Enter your prompt" 
              className={`${loading ? 'cursor-not-allowed opacity-30' : ''} w-full px-4 py-5 rounded-xl border-2 border-[#fffce3] bg-transparent text-[#fffce3] placeholder-[#fffce3]/80 focus:outline-none focus:ring-2 focus:ring-[#fffce3] focus:border-transparent`}
            />
            <button 
              type="submit"
              disabled={loading}
              onClick={(e)=>{
                e.preventDefault()
                generatePoster()
              }}
              className={`${loading ? 'cursor-not-allowed opacity-30' : ''} absolute right-3 top-1/2 transform -translate-y-1/2 bg-[#fffce3] hover:bg-[#fffce3]/90 text-[#222] px-4 py-2 rounded-lg transition-all duration-200`}
            >
              {loading ? 'Generating...' : 'Generate'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ImgGen;