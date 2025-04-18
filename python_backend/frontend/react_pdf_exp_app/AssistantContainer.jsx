import React, { useEffect, useState } from 'react';
import FloatingShapes from './FloatingShapes';
import AssistantIcon from './AssistantIcon';
import MicButton from './MicButton';
import ResponseBox from './ResponseBox';

const AssistantContainer = () => {
  const [isMicOpen, setIsMicOpen] = useState(true);

  const toggleMic = () => {
    setIsMicOpen((prev) => !prev);
  };

  useEffect(()=>{
    if(isMicOpen){
      electronAPI.launchDIDO()
    } else {
      electronAPI.closeDIDO()
    }
  }, [isMicOpen])

  return (
    <div className="assistant-container">
      <FloatingShapes isActive={isMicOpen} />
      <AssistantIcon isMicOpen={isMicOpen} />
      <MicButton isMicOpen={isMicOpen} toggleMic={toggleMic} />
      <ResponseBox isMicOpen={isMicOpen} />
    </div>
  );
};

export default AssistantContainer;