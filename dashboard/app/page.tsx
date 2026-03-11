"use client";

import { useState } from "react";
import { AgentChat } from "../components/AgentChat";
import { TaskBoard } from "../components/TaskBoard";
import { DataAnalysis } from "../components/DataAnalysis";
import { TrainingCenter } from "../components/TrainingCenter";
import { GovernanceCenter } from "../components/GovernanceCenter";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"chat" | "board" | "data" | "training" | "governance">("chat");

  return (
    <main className="flex min-h-screen flex-col bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">TDC Agent Platform</h1>
        <div className="flex space-x-4">
          <button
            onClick={() => setActiveTab("chat")}
            className={`px-4 py-2 rounded-md ${activeTab === "chat" ? "bg-blue-600 text-white" : "text-gray-600 hover:bg-gray-100"}`}
          >
            Agent Chat
          </button>
          <button
            onClick={() => setActiveTab("board")}
            className={`px-4 py-2 rounded-md ${activeTab === "board" ? "bg-blue-600 text-white" : "text-gray-600 hover:bg-gray-100"}`}
          >
            Task Board
          </button>
          <button
            onClick={() => setActiveTab("data")}
            className={`px-4 py-2 rounded-md ${activeTab === "data" ? "bg-blue-600 text-white" : "text-gray-600 hover:bg-gray-100"}`}
          >
            Data Analysis
          </button>
          <button
            onClick={() => setActiveTab("training")}
            className={`px-4 py-2 rounded-md ${activeTab === "training" ? "bg-blue-600 text-white" : "text-gray-600 hover:bg-gray-100"}`}
          >
            Training Center
          </button>
          <button
            onClick={() => setActiveTab("governance")}
            className={`px-4 py-2 rounded-md ${activeTab === "governance" ? "bg-blue-600 text-white" : "text-gray-600 hover:bg-gray-100"}`}
          >
            Governance
          </button>
        </div>
      </header>

      <div className="flex-1 p-6 max-w-7xl w-full mx-auto">
        {activeTab === "chat" ? (
          <AgentChat />
        ) : activeTab === "board" ? (
          <TaskBoard />
        ) : activeTab === "data" ? (
          <DataAnalysis />
        ) : activeTab === "training" ? (
          <TrainingCenter />
        ) : (
          <GovernanceCenter />
        )}
      </div>
    </main>
  );
}
