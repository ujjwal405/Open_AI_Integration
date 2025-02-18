import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

interface Message {
  type: 'user' | 'assistant';
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = { type: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Make API call to backend
      const response = await fetch(`http://localhost:8000/faq/?question=${encodeURIComponent(input)}`);
      
      if (!response.ok) {
        throw new Error('Failed to get response from server');
      }

      const data = await response.json();
      
      // Add assistant message
      const assistantMessage: Message = {
        type: 'assistant',
        content: data.answer || data.response || 'Sorry, I could not process your request.'
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      // Add error message
      const errorMessage: Message = {
        type: 'assistant',
        content: 'Sorry, there was an error processing your request. Please try again.'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 flex flex-col bg-gray-100">
      {/* Main container with max width */}
      <div className="flex-1 w-full max-w-4xl mx-auto flex flex-col h-full">
        {/* Scrollable messages area */}
        <div className="flex-1 overflow-y-auto p-4">
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-white shadow-sm ml-auto max-w-[80%]'
                    : 'bg-blue-50 shadow-sm max-w-[80%]'
                }`}
              >
                <p className="text-sm font-medium mb-1">
                  {message.type === 'user' ? 'You' : 'Assistant'}
                </p>
                <p className="text-gray-700">{message.content}</p>
              </div>
            ))}
            {isLoading && (
              <div className="bg-blue-50 p-4 rounded-lg shadow-sm max-w-[80%]">
                <p className="text-sm font-medium mb-1">Assistant</p>
                <p className="text-gray-700">Thinking...</p>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Fixed input form at bottom */}
        <div className="p-4 bg-gray-100 border-t border-gray-200">
          <form onSubmit={handleSubmit}>
            <div className="relative">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Send a message..."
                className="w-full p-4 pr-12 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-gray-500 hover:text-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;