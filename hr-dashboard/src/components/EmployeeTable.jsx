import React from "react";

export const EmployeeTable = ({ title, data, type = "performers" }) => {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white p-6 rounded-xl border border-gray-150 shadow-sm">
        <h3 className="text-lg font-bold text-gray-800 mb-4">{title}</h3>
        <div className="text-center py-6 text-gray-400 text-sm">
          No records matching this matrix criteria found.
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-xl border border-gray-150 shadow-sm">
      <h3 className="text-lg font-bold text-gray-800 mb-4">{title}</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-gray-100 text-xs font-bold text-gray-400 uppercase tracking-wider">
              <th className="pb-3 pr-4">Employee ID</th>
              {type === "performers" && <th className="pb-3 pr-4">Employee Name</th>}
              <th className="pb-3 text-right">
                {type === "performers" ? "Overall Score" : "Absent Days"}
              </th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr 
                key={row.employee || index} 
                className="border-b border-gray-50 hover:bg-gray-50/50 transition duration-150 text-sm text-gray-700"
              >
                <td className="py-3 pr-4 font-semibold text-gray-800">{row.employee}</td>
                {type === "performers" && (
                  <td className="py-3 pr-4">{row.employee_name || "N/A"}</td>
                )}
                <td className="py-3 text-right font-bold">
                  {type === "performers" ? (
                    <span className="inline-block bg-indigo-50 text-indigo-700 px-2.5 py-0.5 rounded-full text-xs font-semibold">
                      {Number(row.overall_score || 0).toFixed(2)}
                    </span>
                  ) : (
                    <span className="inline-block bg-rose-50 text-rose-700 px-2.5 py-0.5 rounded-full text-xs font-semibold">
                      {row.absent_days} Days
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default EmployeeTable;
