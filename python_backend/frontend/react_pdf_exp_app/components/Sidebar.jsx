// import { Link, useLocation } from "react-router-dom";
import { useState } from "react";
import {Link, useLocation} from 'react-router'

const Sidebar = () => {
  const [isHovered, setIsHovered] = useState(false);
  const location = useLocation();

  // Check if current route matches the link
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <div 
      className={`fixed top-0 left-0 h-full bg-[#111] text-[#fffce3] transition-all duration-300 z-40
        ${isHovered ? "w-56" : "w-20"} overflow-hidden `}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <nav className="flex flex-col p-4 space-y-2 mt-14">
        <Link 
          to="/" 
          className={`flex items-center p-3 rounded-md transition-colors duration-200 group
            ${isActive("/") ? "bg-[#fffce3] text-[#222]" : "hover:bg-[#333]"}`}
        >
          <div className="flex items-center">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            <span className={`ml-4 ${isHovered ? "opacity-100" : "opacity-0 w-0"} transition-all duration-200 whitespace-nowrap overflow-hidden`}>
              PDF Explainer
            </span>
          </div>
        </Link>
        
        <Link 
          to="/imggen" 
          className={`flex items-center p-3 rounded-md transition-colors duration-200 group
            ${isActive("/imggen") ? "bg-[#fffce3] text-[#222]" : "hover:bg-[#333]"}`}
        >
          <div className="flex items-center">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span className={`ml-4 ${isHovered ? "opacity-100" : "opacity-0 w-0"} transition-all duration-200 whitespace-nowrap overflow-hidden`}>
              Image Generation
            </span>
          </div>
        </Link>
      </nav>
    </div>
  );
};

export default Sidebar;