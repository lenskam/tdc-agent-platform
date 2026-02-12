'use client';

import { useState } from 'react';
import { Send, User, Bot } from 'lucide-react';

interface Message {
  role: 'user' | 'agent';
  content: string;
}

export function AgentChat() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'agent', content: 'Hello! I am your Project Manager Agent. How can I help you plan your next project?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      // In a real app, this would call the API
      // const res = await fetch('http://localhost:8000/api/v1/agents/pm/plan', ...);
      
      // Mock response for now
      setTimeout(() => {
        const agentMsg: Message = { 
            role: 'agent', 
            content: `I have received your request: "${userMsg.content}". I am analyzing the requirements and breaking this down into tasks. (Backend integration pending)` 
        };
        setMessages(prev => [...prev, agentMsg]);
        setLoading(false);
      }, 1000);
      
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-white rounded-lg shadow-md border border-gray-200">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex items-start max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
              <div className={`p-2 rounded-full ${msg.role === 'user' ? 'bg-blue-100 ml-2' : 'bg-gray-100 mr-2'}`}>
                {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
              </div>
              <div className={`p-3 rounded-lg ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800'}`}>
                {msg.content}
              </div>
            </div>
          </div>
        ))}
        {loading && <div className="text-gray-400 text-sm ml-12">Thinking...</div>}
      </div>
      
      <div className="p-4 border-t border-gray-200 flex gap-2">
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Describe your project..."
          className="flex-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
        />
        <button 
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 text-white p-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}
