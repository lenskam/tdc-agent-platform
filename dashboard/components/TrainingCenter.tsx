"use client";

import { useState } from "react";

export function TrainingCenter() {
  const [activeTool, setActiveTool] = useState<"quiz" | "manual" | "helpdesk">("quiz");
  const [topic, setTopic] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerateQuiz = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/agents/training/quiz", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, difficulty, num_questions: 5 }),
      });
      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch {
      setResponse("Error generating quiz. Please try again.");
    }
    setLoading(false);
  };

  const handleHelpdesk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/agents/training/helpdesk", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setResponse(data.response || data.message);
    } catch {
      setResponse("Error contacting helpdesk. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Training Center</h2>
        <p className="text-gray-600 mb-6">
          Generate quizzes, create user manuals, or ask the helpdesk for assistance.
        </p>

        <div className="flex space-x-4 mb-6">
          <button
            onClick={() => setActiveTool("quiz")}
            className={`px-4 py-2 rounded-md ${activeTool === "quiz" ? "bg-green-600 text-white" : "bg-gray-100 text-gray-700"}`}
          >
            Generate Quiz
          </button>
          <button
            onClick={() => setActiveTool("manual")}
            className={`px-4 py-2 rounded-md ${activeTool === "manual" ? "bg-green-600 text-white" : "bg-gray-100 text-gray-700"}`}
          >
            User Manual
          </button>
          <button
            onClick={() => setActiveTool("helpdesk")}
            className={`px-4 py-2 rounded-md ${activeTool === "helpdesk" ? "bg-green-600 text-white" : "bg-gray-100 text-gray-700"}`}
          >
            Helpdesk
          </button>
        </div>

        {activeTool === "quiz" && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Topic</label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., DHIS2 data entry, HIV surveillance"
                className="w-full px-3 py-2 border rounded-md"
              />
            </div>
            <div className="flex space-x-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Difficulty</label>
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="px-3 py-2 border rounded-md"
                >
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>
            </div>
            <button
              onClick={handleGenerateQuiz}
              disabled={loading || !topic.trim()}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? "Generating..." : "Generate Quiz"}
            </button>
          </div>
        )}

        {activeTool === "helpdesk" && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Ask a question
              </label>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="e.g., How do I reset my password?"
                rows={3}
                className="w-full px-3 py-2 border rounded-md"
              />
            </div>
            <button
              onClick={handleHelpdesk}
              disabled={loading || !question.trim()}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? "Searching..." : "Ask Helpdesk"}
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
