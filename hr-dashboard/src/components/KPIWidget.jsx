import React from "react";

export const KPIWidget = ({ title, value, iconBg = "bg-indigo-100", textColor = "text-indigo-600", desc }) => {
  return (
    <div className="bg-white p-6 rounded-xl border border-gray-150 shadow-sm hover:shadow-md transition duration-300 transform hover:-translate-y-1">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold text-gray-500 uppercase tracking-wider">{title}</p>
          <p className="text-3xl font-extrabold text-gray-800 mt-2">{value}</p>
          {desc && <p className="text-xs text-gray-400 mt-1">{desc}</p>}
        </div>
        <div className={`p-4 rounded-xl ${iconBg} ${textColor} flex items-center justify-center`}>
          <span className="font-bold text-lg">{title.slice(0, 2).toUpperCase()}</span>
        </div>
      </div>
    </div>
  );
};

export default KPIWidget;
