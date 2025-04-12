import React, { useEffect, useRef } from 'react';

const AssistantIcon = ({isMicOpen}) => {

  const waveRef1 = useRef()
  const waveRef2 = useRef()
  const waveRef3 = useRef()

  useEffect(()=>{
    if(!isMicOpen){
      waveRef1.current.style.display = 'none'
      waveRef2.current.style.display = 'none'
      waveRef3.current.style.display = 'none'
    } else{
      waveRef1.current.style.display = 'block'
      waveRef2.current.style.display = 'block'
      waveRef3.current.style.display = 'block'
    }
  }, [isMicOpen])

  return (
    <div className="assistant-icon">
      <div ref={waveRef1} className="wave wave-1"></div>
      <div ref={waveRef2} className="wave wave-2"></div>
      <div ref={waveRef3} className="wave wave-3"></div>
      <div className="inner-circle"></div>
    </div>
  );
};

export default AssistantIcon;