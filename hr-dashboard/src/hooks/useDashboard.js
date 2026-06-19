import { useState, useEffect, useCallback, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import {
  getTotalEmployees,
  getActiveEmployees,
  getEmployeesOnLeave,
  getAveragePerformance,
  getDepartmentDistribution,
  getTopPerformers,
  getHighAbsenteeism
} from "../services/api";

export const useDashboard = () => {
  const { logoutUser } = useContext(AuthContext);
  const [data, setData] = useState({
    totalEmployees: 0,
    activeEmployees: 0,
    employeesOnLeave: 0,
    avgPerformance: 0,
    departmentDistribution: [],
    topPerformers: [],
    highAbsenteeism: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDashboard = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const [
        totalRes,
        activeRes,
        leaveRes,
        perfRes,
        deptRes,
        topRes,
        absentRes
      ] = await Promise.all([
        getTotalEmployees(),
        getActiveEmployees(),
        getEmployeesOnLeave(),
        getAveragePerformance(),
        getDepartmentDistribution(),
        getTopPerformers(),
        getHighAbsenteeism()
      ]);

      setData({
        totalEmployees: totalRes.data.message || 0,
        activeEmployees: activeRes.data.message || 0,
        employeesOnLeave: leaveRes.data.message || 0,
        avgPerformance: Number(perfRes.data.message || 0).toFixed(2),
        departmentDistribution: deptRes.data.message || [],
        topPerformers: topRes.data.message || [],
        highAbsenteeism: absentRes.data.message || []
      });
    } catch (err) {
      console.error("Dashboard API error:", err);
      // If unauthorized, redirect/trigger logout
      if (err.response?.status === 401 || err.response?.status === 403) {
        setError("Session expired. Please log in again.");
        logoutUser();
      } else {
        setError("Unable to load dashboard details. Please verify your connection.");
      }
    } finally {
      setLoading(false);
    }
  }, [logoutUser]);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  return { data, loading, error, refresh: loadDashboard };
};
