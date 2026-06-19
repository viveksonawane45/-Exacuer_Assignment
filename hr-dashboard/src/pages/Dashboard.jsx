import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useDashboard } from "../hooks/useDashboard";
import { KPIWidget } from "../components/KPIWidget";
import { DepartmentChart } from "../components/DepartmentChart";
import { EmployeeTable } from "../components/EmployeeTable";
import { LoadingSpinner } from "../components/LoadingSpinner";

export const Dashboard = () => {
  const { user, logoutUser } = useContext(AuthContext);
  const { data, loading, error, refresh } = useDashboard();

  return (
    <div className="min-h-screen bg-gray-50/50">
      {/* Navigation Header */}
      <nav className="bg-white border-b border-gray-150 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-extrabold text-xl shadow-md">
                HR
              </div>
              <h1 className="text-xl font-extrabold text-gray-900 tracking-tight">Custom HR Pro Analytics</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm font-semibold text-gray-500 bg-gray-100 px-3 py-1.5 rounded-lg border border-gray-150">
                User: {user}
              </span>
              <button 
                onClick={refresh}
                className="bg-white text-gray-700 hover:bg-gray-50 border border-gray-200 px-4 py-2 rounded-lg text-sm font-bold shadow-sm transition"
              >
                Refresh
              </button>
              <button 
                onClick={logoutUser}
                className="bg-rose-600 hover:bg-rose-700 text-white px-4 py-2 rounded-lg text-sm font-bold shadow-sm transition"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <header className="mb-8">
          <h2 className="text-3xl font-extrabold text-gray-900 leading-tight">HR Operations & Executive Analytics Dashboard</h2>
          <p className="text-sm text-gray-500 mt-2">Real-time indicators, performance reviews, active headcounts, and organizational metrics.</p>
        </header>

        {error && (
          <div className="mb-8 bg-rose-50 border-l-4 border-rose-600 p-4 rounded-r-lg shadow-sm text-rose-800 flex justify-between items-center animate-shake">
            <div>
              <p className="font-bold text-sm">Operation Notification Alert</p>
              <p className="text-sm">{error}</p>
            </div>
            <button 
              onClick={refresh} 
              className="bg-rose-100 text-rose-800 hover:bg-rose-200 px-3 py-1.5 rounded text-xs font-bold transition"
            >
              Retry
            </button>
          </div>
        )}

        {loading ? (
          <LoadingSpinner />
        ) : (
          <div className="space-y-8 animate-fade-in">
            {/* KPI Cards Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <KPIWidget 
                title="Total Employees" 
                value={data.totalEmployees} 
                iconBg="bg-indigo-50" 
                textColor="text-indigo-600"
                desc="Sum of all profiles"
              />
              <KPIWidget 
                title="Active Employees" 
                value={data.activeEmployees} 
                iconBg="bg-emerald-50" 
                textColor="text-emerald-600"
                desc="Active payroll profiles"
              />
              <KPIWidget 
                title="On Leave Today" 
                value={data.employeesOnLeave} 
                iconBg="bg-amber-50" 
                textColor="text-amber-600"
                desc="Approved applications today"
              />
              <KPIWidget 
                title="Avg Performance" 
                value={data.avgPerformance} 
                iconBg="bg-purple-50" 
                textColor="text-purple-600"
                desc="Reviews score average"
              />
            </div>

            {/* Department Chart Row */}
            <div className="grid grid-cols-1 gap-8">
              <DepartmentChart data={data.departmentDistribution} />
            </div>

            {/* Tables Grid Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <EmployeeTable 
                title="Top Performers (Submitted)" 
                data={data.topPerformers} 
                type="performers" 
              />
              <EmployeeTable 
                title="High Absenteeism (> 5 Days Absent)" 
                data={data.highAbsenteeism} 
                type="absenteeism" 
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
