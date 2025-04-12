import React, { useEffect, useState } from 'react';

const ResponseBox = ({ isMicOpen }) => {
  const [response, setResponse] = useState('');

  useEffect(() => {
    if (isMicOpen) {
      setTimeout(() => {
        setResponse('Listening...');
      }, 500);
    } else {
      setResponse('');
    }
  }, [isMicOpen]);

  return (
    <div className={`response-box ${isMicOpen ? 'visible' : ''}`}>
      <p className="response-text">{response}</p>
    </div>
  );
};

export default ResponseBox;