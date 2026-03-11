"use client";

import { useState } from "react";
import { AgentChat } from "../components/AgentChat";
import { TaskBoard } from "../components/TaskBoard";
import { DataAnalysis } from "../components/DataAnalysis";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"chat" | "board" | "data">("chat");

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
        </div>
      </header>

      <div className="flex-1 p-6 max-w-7xl w-full mx-auto">
        {activeTab === "chat" ? (
          <AgentChat />
        ) : activeTab === "board" ? (
          <TaskBoard />
        ) : (
          <DataAnalysis />
        )}
      </div>
    </main>
  );
}
