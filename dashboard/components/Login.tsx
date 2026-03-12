"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

interface LoginProps {
  onLoginSuccess?: (token: string, user: { userId: string; email: string; role: string }) => void;
}

export function Login({ onLoginSuccess }: LoginProps) {
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleDemoLogin = async () => {
    setIsLoading(true);
    setError("");
    try {
      const response = await fetch("/api/v1/auth/login-demo", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Demo login failed");
      }

      localStorage.setItem("auth_token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));

      if (onLoginSuccess) {
        onLoginSuccess(data.access_token, data.user);
      } else {
        router.push("/");
        router.refresh();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Demo login failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-800">TDC Agent Platform</h1>
          <p className="text-gray-600 mt-2">Sign in to your account</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm mb-6">
            {error}
          </div>
        )}

        <div className="space-y-4">
          <button
            onClick={handleDemoLogin}
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            {isLoading ? "Signing in..." : "Demo Login"}
          </button>
        </div>

        <div className="mt-6 text-center text-sm text-gray-500">
          <p>Click Demo Login to access the platform</p>
        </div>
      </div>
    </div>
  );
}
