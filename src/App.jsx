import React from 'react';
import { BrowserRouter, Link, Route, Routes } from 'react-router';
import PDFExplainer from './pages/PDFExplainer';
import ImgGen from './pages/Imggen';
import Virtualassistant from './components/VirtualAssistant';
import Sidebar from './components/Sidebar';

function App() {
  return (
    <div>
     

      <BrowserRouter>
      <Sidebar />
       <Routes>
          <Route path="/" element={<PDFExplainer />} />
          <Route path="/imggen" element={<ImgGen />} />
        </Routes>
      </BrowserRouter>

      <Virtualassistant />
    </div>
  );
}

export default App;