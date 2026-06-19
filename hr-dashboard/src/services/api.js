import axios from "axios";

// Dynamically set base URL to prevent port/host issues
const baseURL = `${window.location.origin}/api/method/`;

const api = axios.create({
  baseURL,
  withCredentials: true
});

export const login = (usr, pwd) => {
  return api.post("login", { usr, pwd });
};

export const logout = () => {
  return api.post("logout");
};

export const getTotalEmployees = () => {
  return api.get("custom_hr_pro.api.dashboard.get_total_employees");
};

export const getActiveEmployees = () => {
  return api.get("custom_hr_pro.api.dashboard.get_active_employees");
};

export const getEmployeesOnLeave = () => {
  return api.get("custom_hr_pro.api.dashboard.get_employees_on_leave");
};

export const getAveragePerformance = () => {
  return api.get("custom_hr_pro.api.dashboard.get_average_performance");
};

export const getDepartmentDistribution = () => {
  return api.get("custom_hr_pro.api.dashboard.get_department_distribution");
};

export const getTopPerformers = () => {
  return api.get("custom_hr_pro.api.dashboard.get_top_performers");
};

export const getHighAbsenteeism = () => {
  return api.get("custom_hr_pro.api.dashboard.get_high_absenteeism");
};

export default api;
