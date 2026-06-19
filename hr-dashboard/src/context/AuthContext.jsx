import React, { createContext, useState, useEffect } from "react";
import { login as apiLogin, logout as apiLogout } from "../services/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem("hr_dashboard_auth") === "true";
  });
  const [user, setUser] = useState(() => {
    return localStorage.getItem("hr_dashboard_user") || "";
  });

  const loginUser = async (usr, pwd) => {
    try {
      const response = await apiLogin(usr, pwd);
      if (response.data.message === "Logged in") {
        setIsAuthenticated(true);
        setUser(usr);
        localStorage.setItem("hr_dashboard_auth", "true");
        localStorage.setItem("hr_dashboard_user", usr);
        return { success: true };
      }
      return { success: false, message: response.data.message || "Invalid credentials" };
    } catch (error) {
      console.error("Login failed:", error);
      return {
        success: false,
        message: error.response?.data?.message || "Server connection error"
      };
    }
  };

  const logoutUser = async () => {
    try {
      await apiLogout();
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      setIsAuthenticated(false);
      setUser("");
      localStorage.removeItem("hr_dashboard_auth");
      localStorage.removeItem("hr_dashboard_user");
    }
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, loginUser, logoutUser, setIsAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};
