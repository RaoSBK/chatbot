import React, { useRef, useEffect } from 'react';
import { 
  Sparkles, 
  Send, 
  User, 
  Bot, 
  HelpCircle, 
  Zap,
  Target,
  AlertTriangle
} from 'lucide-react';
import { usedashboardStore } from '../../store/dashboardStore';

export default function AICoachView() {
  const { chatMessages, chatInput, setChatInput, sendChatMessage } = usedashboardStore();
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      sendChatMessage();
    }
  };

  const sampleQuestions = [
    { text: 'How can I cut my shopping spend by 30%?', icon: Zap },
    { text: 'Will I hit my ₹8,000 Emergency Fund savings goal?', icon: Target },
    { text: 'Explain my current stress score of 42/100.', icon: AlertTriangle },
  ];

  // Helper function to format message text with bold and lists
  const renderMessageText = (text: string, isAI: boolean) => {
    return text.split('\n').map((line, idx) => {
      let formattedLine = line;
      const boldRegex = /\*\*(.*?)\*\*/g;
      
      const parts = [];
      let lastIndex = 0;
      let match;
      
      while ((match = boldRegex.exec(line)) !== null) {
        if (match.index > lastIndex) {
          parts.push(line.substring(lastIndex, match.index));
        }
        parts.push(
          <strong key={match.index} className={isAI ? 'text-slate-950 font-extrabold' : 'text-white font-extrabold'}>
            {match[1]}
          </strong>
        );
        lastIndex = boldRegex.lastIndex;
      }
      
      if (lastIndex < line.length) {
        parts.push(line.substring(lastIndex));
      }

      const content = parts.length > 0 ? parts : line;

      // Unordered lists
      if (line.trim().startsWith('- ')) {
        return (
          <li key={idx} className={`ml-4 list-disc text-xs my-1 font-semibold leading-relaxed ${isAI ? 'text-slate-700' : 'text-white/90'}`}>
            {line.trim().substring(2)}
          </li>
        );
      }

      return (
        <p key={idx} className={`text-xs leading-relaxed font-semibold my-1 ${isAI ? 'text-slate-700' : 'text-white/90'}`}>
          {content}
        </p>
      );
    });
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-230px)]">
      
      {/* Suggested Prompts sidebar */}
      <div className="lg:col-span-1 flex flex-col justify-between h-full bg-card border border-border p-5 rounded-2xl shadow-sm">
        <div className="space-y-4">
          <h4 className="text-xs font-black text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
            <HelpCircle className="w-4 h-4 text-ai-purple" />
            Suggested Prompts
          </h4>
          <p className="text-[10px] text-slate-500 font-semibold leading-relaxed">
            Click any prompt to instantly query the AI Coach regarding your live balance and ledger data:
          </p>

          <div className="space-y-2">
            {sampleQuestions.map((q, idx) => {
              const Icon = q.icon;
              return (
                <button
                  key={idx}
                  onClick={() => sendChatMessage(q.text)}
                  className="w-full text-left p-3.5 rounded-xl border border-border bg-slate-50/50 text-xs font-bold text-slate-600 hover:text-slate-900 hover:border-ai-purple/30 hover:bg-slate-100/50 transition-all flex items-start gap-2.5"
                >
                  <Icon className="w-4 h-4 text-ai-purple shrink-0 mt-0.5" />
                  <span>{q.text}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="bg-slate-50 border border-border/80 p-4 rounded-xl text-[10px] text-slate-500 font-semibold leading-relaxed mt-4">
          💡 <span className="text-slate-700 font-bold">Privacy Lock</span>: All conversation records and financial analysis are processed inside your client browser.
        </div>
      </div>

      {/* Chat Thread Panel */}
      <div className="lg:col-span-3 flex flex-col h-full bg-card border border-border rounded-2xl overflow-hidden shadow-sm">
        
        {/* Chat Header */}
        <div className="px-6 py-4 border-b border-border bg-slate-50 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-ai-purple to-purple-700 flex items-center justify-center text-white shadow-sm shadow-purple-600/10">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h4 className="text-sm font-extrabold text-slate-950">MoneyMind X AI Advisor</h4>
              <p className="text-[10px] text-primary font-bold flex items-center gap-1 mt-0.5">
                <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                Online & Synced with Ledger
              </p>
            </div>
          </div>
        </div>

        {/* Scrollable messages container */}
        <div className="flex-grow p-6 overflow-y-auto space-y-4 min-h-0 bg-slate-50/30">
          {chatMessages.map((msg) => {
            const isAI = msg.sender === 'ai';
            return (
              <div 
                key={msg.id}
                className={`flex gap-3 max-w-[85%] ${isAI ? 'mr-auto' : 'ml-auto flex-row-reverse'}`}
              >
                {/* Avatar */}
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border ${
                  isAI 
                    ? 'bg-ai-purple/10 border-ai-purple/20 text-ai-purple' 
                    : 'bg-primary/10 border-primary/20 text-primary'
                }`}>
                  {isAI ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
                </div>

                {/* Bubble Container */}
                <div className={`p-4 rounded-2xl relative border ${
                  isAI 
                    ? 'bg-white border-slate-200 text-slate-800 shadow-sm' 
                    : 'bg-gradient-to-br from-primary to-primary-light border-primary/25 text-white shadow-sm'
                }`}>
                  {renderMessageText(msg.text, isAI)}
                  <span className={`block text-[8px] font-bold text-right mt-2 ${isAI ? 'text-slate-400' : 'text-white/70'}`}>
                    {msg.timestamp}
                  </span>
                </div>
              </div>
            );
          })}
          <div ref={chatEndRef} />
        </div>

        {/* Chat Input form area */}
        <div className="p-4 border-t border-border bg-slate-50 flex items-center gap-2 shrink-0">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Type your message to AI Coach (e.g. How can I optimize my food savings?)..."
            className="flex-grow bg-white border border-slate-200 rounded-xl px-4 py-3 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-ai-purple transition shadow-inner"
          />
          <button
            onClick={() => sendChatMessage()}
            disabled={!chatInput.trim()}
            className="w-10 h-10 rounded-xl bg-gradient-to-tr from-ai-purple to-purple-600 hover:opacity-90 active:scale-95 text-white flex items-center justify-center transition disabled:opacity-40 disabled:scale-100 disabled:pointer-events-none shadow-sm shadow-purple-600/10"
            title="Send message"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>

      </div>

    </div>
  );
}
