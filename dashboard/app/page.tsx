"use client";

import { useState } from "react";
import { AgentChat } from "../components/AgentChat";
import { TaskBoard } from "../components/TaskBoard";
import { DataAnalysis } from "../components/DataAnalysis";
import { TrainingCenter } from "../components/TrainingCenter";
import { GovernanceCenter } from "../components/GovernanceCenter";
import { ApprovalQueue } from "../components/ApprovalQueue";
import { ProtectedRoute } from "../components/ProtectedRoute";
import { useAuth } from "../components/AuthContext";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"chat" | "board" | "data" | "training" | "governance" | "approvals">("chat");
  const { user, logout } = useAuth();

  return (
    <ProtectedRoute>
      <main className="flex min-h-screen flex-col bg-gray-50">
        <header className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-800">TDC Agent Platform</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">{user?.email}</span>
            <button
              onClick={logout}
              className="px-4 py-2 text-sm rounded-md text-red-600 hover:bg-red-50"
            >
              Logout
            </button>
          </div>
        </header>

        <nav className="bg-white border-b border-gray-200 px-6">
          <div className="flex space-x-4">
            <button
              onClick={() => setActiveTab("chat")}
              className={`px-4 py-3 text-sm font-medium border-b-2 ${
                activeTab === "chat"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              Agent Chat
            </button>
            <button
              onClick={() => setActiveTab("board")}
              className={`px-4 py-3 text-sm font-medium border-b-2 ${
                activeTab === "board"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              Task Board
            </button>
            <button
              onClick={() => setActiveTab("approvals")}
              className={`px-4 py-3 text-sm font-medium border-b-2 ${
                activeTab === "approvals"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              Approvals
            </button>
            <button
              onClick={() => setActiveTab("data")}
              className={`px-4 py-3 text-sm font-medium border-b-2 ${
                activeTab === "data"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              Data Analysis
            </button>
            <button
              onClick={() => setActiveTab("training")}
              className={`px-4 py-3 text-sm font-medium border-b-2 ${
                activeTab === "training"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              Training Center
            </button>
            <button
              onClick={() => setActiveTab("governance")}
              className={`px-4 py-3 text-sm font-medium border-b-2 ${
                activeTab === "governance"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              Governance
            </button>
          </div>
        </nav>

        <div className="flex-1 p-6 max-w-7xl w-full mx-auto">
          {activeTab === "chat" ? (
            <AgentChat />
          ) : activeTab === "board" ? (
            <TaskBoard />
          ) : activeTab === "approvals" ? (
            <ApprovalQueue />
          ) : activeTab === "data" ? (
            <DataAnalysis />
          ) : activeTab === "training" ? (
            <TrainingCenter />
          ) : (
            <GovernanceCenter />
          )}
        </div>
      </main>
    </ProtectedRoute>
  );
}
