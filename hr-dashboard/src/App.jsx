import React, { useContext, useState } from "react";
import { AuthProvider, AuthContext } from "./context/AuthContext";
import { Dashboard } from "./pages/Dashboard";

const LoginScreen = () => {
  const { loginUser } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setErrorMsg("Please fill in all fields.");
      return;
    }

    try {
      setLoading(true);
      setErrorMsg("");
      const result = await loginUser(username, password);
      if (!result.success) {
        setErrorMsg(result.message || "Invalid username or password.");
      }
    } catch (err) {
      setErrorMsg("Connection failure. Unable to contact server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-slate-900 to-indigo-950 flex items-center justify-center p-4">
      <div className="bg-white/95 backdrop-blur-md w-full max-w-md p-8 rounded-2xl border border-white/10 shadow-2xl animate-fade-in">
        {/* Branding Title */}
        <div className="text-center mb-8">
          <div className="inline-flex h-14 w-14 rounded-2xl bg-indigo-600 items-center justify-center text-white font-extrabold text-2xl shadow-lg mb-4">
            HR
          </div>
          <h2 className="text-2xl font-extrabold text-gray-900 tracking-tight">Executive HR Portal</h2>
          <p className="text-sm text-gray-500 mt-2">Sign in to unlock operational insights</p>
        </div>

        {errorMsg && (
          <div className="mb-6 bg-rose-50 border-l-4 border-rose-600 p-3.5 rounded text-xs font-semibold text-rose-800 animate-shake">
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Username / Email</label>
            <input 
              type="text" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="e.g. administrator"
              disabled={loading}
              className="w-full px-4 py-3 rounded-xl border border-gray-250 bg-gray-50/50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition font-medium text-gray-800"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Password</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              disabled={loading}
              className="w-full px-4 py-3 rounded-xl border border-gray-250 bg-gray-50/50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition font-medium text-gray-800"
            />
          </div>

          <button 
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3.5 px-4 rounded-xl shadow-lg hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 transform active:scale-98 flex items-center justify-center"
          >
            {loading ? (
              <div className="h-5 w-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              "Sign In"
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

const MainApp = () => {
  const { isAuthenticated } = useContext(AuthContext);
  return isAuthenticated ? <Dashboard /> : <LoginScreen />;
};

export const App = () => {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
};

export default App;
