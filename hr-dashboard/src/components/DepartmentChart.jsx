import React from "react";

export const DepartmentChart = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm text-center text-gray-400">
        No active department distribution data available.
      </div>
    );
  }

  const maxVal = Math.max(...data.map(d => d.total || 0), 1);
  const totalEmployees = data.reduce((acc, curr) => acc + (curr.total || 0), 0);

  return (
    <div className="bg-white p-6 rounded-xl border border-gray-150 shadow-sm">
      <h3 className="text-lg font-bold text-gray-800 mb-2">Department-wise Employee Distribution</h3>
      <p className="text-xs text-gray-400 mb-6">Total active headcount across {data.length} registered departments: {totalEmployees} active personnel</p>
      
      <div className="space-y-4">
        {data.map((dept, index) => {
          const count = dept.total || 0;
          const percentage = Math.round((count / totalEmployees) * 100);
          const barWidth = Math.max(5, Math.round((count / maxVal) * 100));

          // Harmonized color scheme cycling
          const colors = [
            "bg-indigo-500",
            "bg-emerald-500",
            "bg-blue-500",
            "bg-amber-500",
            "bg-rose-500",
            "bg-purple-500"
          ];
          const colorClass = colors[index % colors.length];

          return (
            <div key={dept.department || index} className="group">
              <div className="flex justify-between text-sm font-semibold text-gray-700 mb-1">
                <span>{dept.department || "General"}</span>
                <span className="text-gray-500">{count} ({percentage}%)</span>
              </div>
              <div className="w-full bg-gray-100 h-4 rounded-full overflow-hidden shadow-inner">
                <div 
                  className={`h-full ${colorClass} rounded-full transition-all duration-1000 ease-out`}
                  style={{ width: `${barWidth}%` }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DepartmentChart;
