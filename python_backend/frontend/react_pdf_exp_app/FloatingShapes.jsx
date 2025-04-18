import React, { useEffect, useRef } from 'react';

const FloatingShapes = ({ isActive }) => {

  return (
    <div className={`floating-shapes ${isActive ? 'active' : ''}`}>
      <div  className="shape shape-1"></div>
      <div className="shape shape-2"></div>
      <div className="shape shape-3"></div>
      <div className="shape shape-4"></div>
    </div>
  );
};

export default FloatingShapes;