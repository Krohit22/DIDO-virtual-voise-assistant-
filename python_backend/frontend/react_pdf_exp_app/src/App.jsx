import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router';
import Sidebar from '../components/Sidebar';
import Virtualassistant from '../components/VirtualAssistant';
import ChatWithPdf from '../pages/chatWithPdf';
import ImgGen from '../pages/Imggen';
function App() {

  return (
    <div>
      <BrowserRouter>
      <Sidebar />
       <Routes>
          <Route path="/" element={<ChatWithPdf />} />
          <Route path="/imggen" element={<ImgGen />} />
        </Routes>
      </BrowserRouter>

      <Virtualassistant />
    </div>
  )
}

export default App
