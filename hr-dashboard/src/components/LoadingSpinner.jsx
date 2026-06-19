import React from "react";

export const LoadingSpinner = () => {
  return (
    <div className="flex flex-col justify-center items-center h-64 space-y-4">
      <div className="animate-spin rounded-full h-12 w-12 border-4 border-indigo-600 border-t-transparent"></div>
      <p className="text-gray-500 font-medium animate-pulse">Loading Executive HR Analytics...</p>
    </div>
  );
};

export default LoadingSpinner;
