'use client';

import { useState } from 'react';

interface Task {
  id: number;
  title: string;
  status: 'TODO' | 'IN_PROGRESS' | 'DONE';
  assignee: string;
}

const MOCK_TASKS: Task[] = [
  { id: 1, title: 'Analyze GEMINI.md', status: 'DONE', assignee: 'Project Manager' },
  { id: 2, title: 'Setup FastAPI', status: 'DONE', assignee: 'DevOps' },
  { id: 3, title: 'Implement Frontend', status: 'IN_PROGRESS', assignee: 'Frontend Dev' },
  { id: 4, title: 'Deploy to Hostinger', status: 'TODO', assignee: 'DevOps' },
];

export function TaskBoard() {
  const [tasks, setTasks] = useState<Task[]>(MOCK_TASKS);

  const getTasksByStatus = (status: Task['status']) => tasks.filter(t => t.status === status);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-[600px]">
      {['TODO', 'IN_PROGRESS', 'DONE'].map((status) => (
        <div key={status} className="bg-gray-100 rounded-lg p-4">
          <h3 className="font-bold text-gray-700 mb-4">{status}</h3>
          <div className="space-y-3">
            {getTasksByStatus(status as Task['status']).map(task => (
              <div key={task.id} className="bg-white p-3 rounded shadow-sm border border-gray-200">
                <h4 className="font-medium text-gray-900">{task.title}</h4>
                <div className="text-xs text-gray-500 mt-2 flex justify-between">
                  <span>#{task.id}</span>
                  <span className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded text-[10px]">{task.assignee}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
