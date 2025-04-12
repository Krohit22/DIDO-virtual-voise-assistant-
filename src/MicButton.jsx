import React from 'react';
import { IoMdMic } from "react-icons/io";
import { IoMdMicOff } from "react-icons/io";

const MicButton = ({ isMicOpen, toggleMic }) => {
  return (
    <button className={`mic-button ${isMicOpen ? 'active' : ''}`} onClick={toggleMic}>
      <span className="mic-icon mic-open"><IoMdMic /></span>
      <span className="mic-icon mic-closed"><IoMdMicOff /></span>
    </button>
  );
};

export default MicButton;