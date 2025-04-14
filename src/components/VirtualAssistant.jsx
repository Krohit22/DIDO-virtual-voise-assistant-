import { AiFillRobot } from "react-icons/ai";
import { useState } from "react";
import Voice from "../pages/Voice";

function Virtualassistant() {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleAssistant = () => {
    setIsExpanded((event) => !event); 
  };

  return (
    <div>
      {/* Floating Toggle Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={toggleAssistant}
          className="bg-[#333] p-4 rounded-full text-4xl cursor-pointer text-[#fffce3] hover:rotate-12 hover:scale-108 transition-all duration-300"
        >
          <AiFillRobot />
        </button>
      </div>

      {/* Virtual Assistant Panel */}
      {isExpanded && (
        <div className="fixed inset-0 bg-[#00000047] backdrop-blur-[3px] flex items-center justify-center p-4 z-40">
          <div className="sm:w-[60%] sm:h-[80%]  rounded-2xl shadow-md overflow-hidden">
            {/* Header */}
            <div className="bg-[#222] px-6 py-4 border-b border-[#444] text-[#fffce3]">
              <div className="flex items-center gap-3 text-xl font-semibold">
                <AiFillRobot className="text-2xl" />
                <p>DiDo</p>
              </div>
              <p className="text-sm text-[#ccc] mt-1">
                Today I am your Virtual Assistant
              </p>
            </div>

            {/* Body */}
            <div className="bg-[#333] px-6 py-4 h-full text-[#fffce3] overflow-y-auto w-full ">
              <Voice />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Virtualassistant;
