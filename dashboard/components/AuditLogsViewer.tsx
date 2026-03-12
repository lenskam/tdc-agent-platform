"use client";

import { useState, useEffect } from "react";
import { useAuth } from "./AuthContext";

interface AuditLog {
  id: number;
  user_id: number | null;
  action: string;
  resource_type: string;
  resource_id: string | null;
  details: Record<string, unknown> | null;
  ip_address: string | null;
  timestamp: string;
}

interface AuditLogsViewerProps {
  resourceType?: string;
  limit?: number;
}

export function AuditLogsViewer({ resourceType, limit = 50 }: AuditLogsViewerProps) {
  const { token } = useAuth();
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        let url = `/api/v1/audit/?limit=${limit}`;
        if (resourceType) {
          url += `&resource_type=${resourceType}`;
        }
        const res = await fetch(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (res.ok) {
          const data = await res.json();
          setLogs(data);
        }
      } catch (error) {
        console.error("Failed to fetch audit logs:", error);
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchLogs();
    }
  }, [token, resourceType, limit]);

  const getActionColor = (action: string) => {
    if (action.includes("login") || action.includes("logout")) {
      return "text-blue-600";
    }
    if (action.includes("create")) {
      return "text-green-600";
    }
    if (action.includes("update") || action.includes("approve")) {
      return "text-yellow-600";
    }
    if (action.includes("delete") || action.includes("reject")) {
      return "text-red-600";
    }
    return "text-gray-600";
  };

  const getResourceIcon = (resourceType: string) => {
    switch (resourceType) {
      case "auth":
        return "🔐";
      case "task":
        return "📋";
      case "approval":
        return "✅";
      case "project":
        return "📁";
      default:
        return "📝";
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (logs.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400 text-lg mb-2">No audit logs found</div>
        <p className="text-gray-500">Actions will be logged here</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-gray-800">Audit Logs</h2>
        <span className="text-sm text-gray-500">{logs.length} entries</span>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Time
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Action
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Resource
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                User ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Details
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {logs.map((log) => (
              <tr key={log.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  <div>{new Date(log.timestamp).toLocaleDateString()}</div>
                  <div className="text-xs">{new Date(log.timestamp).toLocaleTimeString()}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`text-sm font-medium ${getActionColor(log.action)}`}>
                    {log.action}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center gap-2">
                    <span>{getResourceIcon(log.resource_type)}</span>
                    <span className="text-sm text-gray-900">
                      {log.resource_type}
                      {log.resource_id && <span className="text-gray-500">:#{log.resource_id}</span>}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {log.user_id || "-"}
                </td>
                <td className="px-6 py-4 text-sm text-gray-500 max-w-xs">
                  {log.details && (
                    <div className="truncate font-mono text-xs">
                      {JSON.stringify(log.details)}
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
