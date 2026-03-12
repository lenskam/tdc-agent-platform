"use client";

import { useState, useEffect } from "react";
import { useAuth } from "./AuthContext";

interface ApprovalRequest {
  id: number;
  task_id: number;
  title: string;
  description: string | null;
  status: string;
  priority: string;
  created_at: string;
}

interface ApprovalQueueProps {
  refreshTrigger?: number;
}

export function ApprovalQueue({ refreshTrigger }: ApprovalQueueProps) {
  const { token } = useAuth();
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedApproval, setSelectedApproval] = useState<ApprovalRequest | null>(null);
  const [comments, setComments] = useState("");
  const [actionLoading, setActionLoading] = useState<number | null>(null);

  const fetchApprovals = async () => {
    try {
      const res = await fetch("/api/v1/approvals/pending", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (res.ok) {
        const data = await res.json();
        setApprovals(data);
      }
    } catch (error) {
      console.error("Failed to fetch approvals:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchApprovals();
    }
  }, [token, refreshTrigger]);

  const handleApprove = async (id: number) => {
    setActionLoading(id);
    try {
      const res = await fetch(`/api/v1/approvals/${id}/approve`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ comments }),
      });
      if (res.ok) {
        setApprovals(approvals.filter((a) => a.id !== id));
        setSelectedApproval(null);
        setComments("");
      }
    } catch (error) {
      console.error("Failed to approve:", error);
    } finally {
      setActionLoading(null);
    }
  };

  const handleReject = async (id: number) => {
    setActionLoading(id);
    try {
      const res = await fetch(`/api/v1/approvals/${id}/reject`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ comments }),
      });
      if (res.ok) {
        setApprovals(approvals.filter((a) => a.id !== id));
        setSelectedApproval(null);
        setComments("");
      }
    } catch (error) {
      console.error("Failed to reject:", error);
    } finally {
      setActionLoading(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (approvals.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400 text-lg mb-2">No pending approvals</div>
        <p className="text-gray-500">All caught up!</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-800">Approval Queue</h2>
        <span className="bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded-full">
          {approvals.length} pending
        </span>
      </div>

      <div className="grid gap-4">
        {approvals.map((approval) => (
          <div
            key={approval.id}
            className={`bg-white border rounded-lg p-4 shadow-sm hover:shadow-md transition ${
              approval.priority === "high" ? "border-red-300" : "border-gray-200"
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h3 className="font-medium text-gray-900">{approval.title}</h3>
                  {approval.priority === "high" && (
                    <span className="bg-red-100 text-red-800 text-xs px-2 py-0.5 rounded">High</span>
                  )}
                </div>
                {approval.description && (
                  <p className="text-sm text-gray-600 mt-1 line-clamp-2">{approval.description}</p>
                )}
                <p className="text-xs text-gray-400 mt-2">
                  Task #{approval.task_id} • {new Date(approval.created_at).toLocaleString()}
                </p>
              </div>
              <div className="flex gap-2 ml-4">
                <button
                  onClick={() => setSelectedApproval(approval)}
                  className="px-3 py-1.5 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  Review
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {selectedApproval && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-lg w-full p-6">
            <h3 className="text-lg font-semibold mb-4">{selectedApproval.title}</h3>
            {selectedApproval.description && (
              <p className="text-gray-600 mb-4">{selectedApproval.description}</p>
            )}
            <p className="text-sm text-gray-500 mb-4">
              Task ID: {selectedApproval.task_id} • Priority: {selectedApproval.priority}
            </p>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Comments (optional)
              </label>
              <textarea
                value={comments}
                onChange={(e) => setComments(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                rows={3}
                placeholder="Add any comments..."
              />
            </div>
            
            <div className="flex gap-3">
              <button
                onClick={() => handleReject(selectedApproval.id)}
                disabled={actionLoading === selectedApproval.id}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50"
              >
                {actionLoading === selectedApproval.id ? "Processing..." : "Reject"}
              </button>
              <button
                onClick={() => handleApprove(selectedApproval.id)}
                disabled={actionLoading === selectedApproval.id}
                className="flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50"
              >
                {actionLoading === selectedApproval.id ? "Processing..." : "Approve"}
              </button>
            </div>
            <button
              onClick={() => {
                setSelectedApproval(null);
                setComments("");
              }}
              className="mt-3 w-full px-4 py-2 text-gray-600 hover:text-gray-800"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
