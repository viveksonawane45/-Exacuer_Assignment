import React from 'react';
import { useFrappeGetCall } from 'frappe-react-sdk';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface DepartmentSummary {
  department: string;
  headcount: number;
  avg_review_score: number;
}

export const HRDashboard: React.FC = () => {
  const { data, error, isLoading } = useFrappeGetCall<DepartmentSummary[]>(
    'custom_hr_pro.api.get_department_summary'
  );

  if (isLoading) return <div className="p-8 text-center font-medium text-gray-500">Loading Enterprise Analytics Matrix Data Engine...</div>;
  if (error) return <div className="p-8 text-red-500 font-bold bg-red-50 rounded">Error: {error.message}</div>;

  return (
    <div className="p-6 max-w-7xl mx-auto bg-gray-50 min-h-screen">
      <header className="mb-8 border-b pb-4">
        <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight">HR Operations & Executive Analytics Dashboard</h1>
      </header>

      {/* Metrics Grid Data Component Rows */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {data?.map((dept) => (
          <div key={dept.department} className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition">
            <h3 className="text-lg font-bold text-gray-800 mb-2">{dept.department}</h3>
            <div className="flex justify-between text-sm text-gray-600">
              <span>Active Headcount: <strong>{dept.headcount}</strong></span>
              <span>Avg Review Score: <strong className="text-indigo-600">{Number(dept.avg_review_score).toFixed(2)}</strong></span>
            </div>
          </div>
        ))}
      </div>

      {/* Graphical Optimization Framework Layer Block */}
      <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Cross-Department Comparative Performance Matrix</h2>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
              <XAxis dataKey="department" stroke="#6B7280" />
              <YAxis stroke="#6B7280" />
              <Tooltip cursor={{ fill: '#F9FAFB' }} />
              <Legend />
              <Bar dataKey="avg_review_score" name="Average Evaluation Metric Score" fill="#4F46E5" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
