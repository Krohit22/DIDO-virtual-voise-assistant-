import React from 'react';

function ImgGen() {
  return (
    <div className="w-screen h-screen bg-[#222] flex flex-col">
      {/* Top heading */}
      <div className="flex justify-center pt-12">
        <h1 className="text-4xl font-bold text-[#fffce3] text-center my-1">Image Generator</h1>
      </div>

      {/* Bottom input form */}
      <div className="flex-1 flex items-end justify-center pb-6">
        <div className="w-full max-w-2xl px-4">
          <form className="relative">
            <input 
              type="text" 
              placeholder="Enter your prompt" 
              className="w-full px-4 py-5 rounded-xl border-2 border-[#fffce3] bg-transparent text-[#fffce3] placeholder-[#fffce3]/80 focus:outline-none focus:ring-2 focus:ring-[#fffce3] focus:border-transparent"
            />
            <button 
              type="submit"
              className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-[#fffce3] hover:bg-[#fffce3]/90 text-[#222] px-4 py-2 rounded-lg font-medium transition-all duration-200"
            >
              GENERATE
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ImgGen;