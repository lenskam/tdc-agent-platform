"use client";

import { useState, useRef } from "react";
import {
  Upload,
  FileText,
  BarChart3,
  AlertTriangle,
  CheckCircle,
} from "lucide-react";

interface AnalysisResult {
  success: boolean;
  file?: string;
  shape?: { rows: number; columns: number };
  columns?: string[];
  missing_values?: Record<string, number>;
  numeric_summary?: Record<string, any>;
  categorical_summary?: Record<string, any>;
  results?: Record<string, any>;
  output_file?: string;
  error?: string;
}

export function DataAnalysis() {
  const [file, setFile] = useState<File | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [activeTab, setActiveTab] = useState<"stats" | "outliers" | "clean">(
    "stats",
  );
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile && selectedFile.name.endsWith(".csv")) {
      setFile(selectedFile);
      setResult(null);
    }
  };

  const analyzeData = async () => {
    if (!file) return;

    setAnalyzing(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("action", activeTab);

    try {
      const response = await fetch(
        "http://localhost:8000/api/v1/data/analyze",
        {
          method: "POST",
          body: formData,
        },
      );

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        success: false,
        error:
          "Backend not connected. This is a UI placeholder - connect to API for full functionality.",
      });
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-white rounded-lg shadow-md border border-gray-200">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-800">Data Analysis</h2>
        <p className="text-sm text-gray-600">
          Upload CSV files for analysis, cleaning, and outlier detection
        </p>
      </div>

      <div className="flex border-b border-gray-200">
        <button
          onClick={() => setActiveTab("stats")}
          className={`px-4 py-2 text-sm font-medium ${
            activeTab === "stats"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-600 hover:text-gray-800"
          }`}
        >
          <BarChart3 className="inline-block w-4 h-4 mr-1" />
          Statistics
        </button>
        <button
          onClick={() => setActiveTab("outliers")}
          className={`px-4 py-2 text-sm font-medium ${
            activeTab === "outliers"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-600 hover:text-gray-800"
          }`}
        >
          <AlertTriangle className="inline-block w-4 h-4 mr-1" />
          Outliers
        </button>
        <button
          onClick={() => setActiveTab("clean")}
          className={`px-4 py-2 text-sm font-medium ${
            activeTab === "clean"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-600 hover:text-gray-800"
          }`}
        >
          <CheckCircle className="inline-block w-4 h-4 mr-1" />
          Clean Data
        </button>
      </div>

      <div className="flex-1 p-4 overflow-y-auto">
        {!file ? (
          <div
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 transition-colors"
          >
            <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 mb-2">Click to upload a CSV file</p>
            <p className="text-sm text-gray-400">Supports .csv files</p>
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="hidden"
            />
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center">
                <FileText className="w-5 h-5 text-blue-600 mr-2" />
                <span className="font-medium text-gray-800">{file.name}</span>
              </div>
              <button
                onClick={() => {
                  setFile(null);
                  setResult(null);
                }}
                className="text-sm text-red-600 hover:text-red-700"
              >
                Remove
              </button>
            </div>

            <div className="flex gap-4">
              <button
                onClick={analyzeData}
                disabled={analyzing}
                className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {analyzing
                  ? "Analyzing..."
                  : `Analyze with ${activeTab === "stats" ? "Statistics" : activeTab === "outliers" ? "Outlier Detection" : "Data Cleaning"}`}
              </button>
            </div>

            {result && (
              <div
                className={`p-4 rounded-lg ${result.success ? "bg-green-50 border border-green-200" : "bg-red-50 border border-red-200"}`}
              >
                {result.success ? (
                  <div className="space-y-2">
                    {result.shape && (
                      <p className="text-sm">
                        <span className="font-medium">Dataset:</span>{" "}
                        {result.shape.rows} rows × {result.shape.columns}{" "}
                        columns
                      </p>
                    )}
                    {result.output_file && (
                      <p className="text-sm">
                        <span className="font-medium">Output:</span>{" "}
                        {result.output_file}
                      </p>
                    )}
                    {result.numeric_summary && (
                      <div className="mt-2">
                        <p className="text-sm font-medium mb-1">
                          Numeric Summary:
                        </p>
                        <pre className="text-xs bg-white p-2 rounded overflow-x-auto">
                          {JSON.stringify(result.numeric_summary, null, 2)}
                        </pre>
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="text-sm text-red-700">{result.error}</p>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
