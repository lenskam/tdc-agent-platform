"use client";

import { useState } from "react";

export function GovernanceCenter() {
  const [activeTool, setActiveTool] = useState<"risks" | "audit" | "budget">("risks");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSummarizeRisks = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/agents/director/risks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ time_period: "30_days" }),
      });
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch {
      setResponse("Error fetching risks. Please try again.");
    }
    setLoading(false);
  };

  const handleAuditSystem = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/agents/director/audit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ time_window_hours: 24 }),
      });
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch {
      setResponse("Error running audit. Please try again.");
    }
    setLoading(false);
  };

  const handleCheckBudget = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/agents/finance/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ budget_id: "Q1_2024" }),
      });
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch {
      setResponse("Error fetching budget. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Governance & Security</h2>
        <p className="text-gray-600 mb-6">
          Monitor organizational risks, audit system health, and review financial compliance.
        </p>

        <div className="flex space-x-4 mb-6">
          <button
            onClick={() => setActiveTool("risks")}
            className={`px-4 py-2 rounded-md ${activeTool === "risks" ? "bg-purple-600 text-white" : "bg-gray-100 text-gray-700"}`}
          >
            Risk Summary
          </button>
          <button
            onClick={() => setActiveTool("audit")}
            className={`px-4 py-2 rounded-md ${activeTool === "audit" ? "bg-purple-600 text-white" : "bg-gray-100 text-gray-700"}`}
          >
            System Audit
          </button>
          <button
            onClick={() => setActiveTool("budget")}
            className={`px-4 py-2 rounded-md ${activeTool === "budget" ? "bg-purple-600 text-white" : "bg-gray-100 text-gray-700"}`}
          >
            Budget Analysis
          </button>
        </div>

        {activeTool === "risks" && (
          <div className="space-y-4">
            <p className="text-gray-600">
              View key risks across projects, budgets, and compliance areas.
            </p>
            <button
              onClick={handleSummarizeRisks}
              disabled={loading}
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50"
            >
              {loading ? "Loading..." : "Summarize Risks"}
            </button>
          </div>
        )}

        {activeTool === "audit" && (
          <div className="space-y-4">
            <p className="text-gray-600">
              Scan system logs for anomalies and suspicious behavior patterns.
            </p>
            <button
              onClick={handleAuditSystem}
              disabled={loading}
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50"
            >
              {loading ? "Scanning..." : "Run System Audit"}
            </button>
          </div>
        )}

        {activeTool === "budget" && (
          <div className="space-y-4">
            <p className="text-gray-600">
              Analyze budget variance and donor compliance (READ-ONLY).
            </p>
            <button
              onClick={handleCheckBudget}
              disabled={loading}
              className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50"
            >
              {loading ? "Analyzing..." : "Analyze Q1 2024 Budget"}
            </button>
          </div>
        )}

        {response && (
          <div className="mt-6 p-4 bg-gray-50 rounded-md">
            <h3 className="font-medium text-gray-700 mb-2">Result:</h3>
            <pre className="whitespace-pre-wrap text-sm text-gray-800 overflow-auto max-h-96">
              {response}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
