import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, CornerDownLeft } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  onQuickPrompt?: (prompt: string) => void;
}

const QUICK_PROMPTS = [
  "I have fever and headache. What should I do?",
  "I have had low fever 99.5 F for 1 day.",
  "I have high fever 103 F for 4 days with chills.",
  "What is paracetamol used for and what are its warnings?",
  "What are the side effects of ibuprofen?",
];

export const ChatInput: React.FC<ChatInputProps> = ({ onSend, isLoading, onQuickPrompt }) => {
  const [text, setText] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    textareaRef.current?.focus();
  }, []);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!text.trim() || isLoading) return;
    onSend(text.trim());
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 140)}px`;
    }
  };

  return (
    <div className="max-w-4xl mx-auto w-full space-y-3">
      {/* Quick Suggestion Chips */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none">
        <span className="text-[11px] font-bold text-muted-foreground uppercase tracking-wider flex items-center gap-1 flex-shrink-0 mr-1">
          <Sparkles className="h-3 w-3 text-blue-600" /> Prompts:
        </span>
        {QUICK_PROMPTS.map((prompt, idx) => (
          <button
            key={idx}
            type="button"
            disabled={isLoading}
            onClick={() => {
              if (onQuickPrompt) onQuickPrompt(prompt);
              else onSend(prompt);
            }}
            className="flex-shrink-0 text-xs px-3 py-1.5 rounded-full border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-950/40 text-foreground transition-all shadow-xs disabled:opacity-50"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Input Box Card */}
      <form
        onSubmit={handleSubmit}
        className="relative flex items-end gap-2 rounded-2xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-2.5 shadow-md focus-within:border-blue-600 focus-within:ring-2 focus-within:ring-blue-500/20 transition-all"
      >
        <textarea
          ref={textareaRef}
          value={text}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
          placeholder="Describe your symptoms (e.g. fever, headache, duration, how many days)... Press Enter to send"
          disabled={isLoading}
          rows={1}
          maxLength={2000}
          className="flex-1 max-h-[140px] resize-none bg-transparent px-3 py-1.5 text-sm sm:text-base text-foreground placeholder:text-muted-foreground focus:outline-none disabled:opacity-50 leading-relaxed"
        />

        <div className="flex items-center gap-2 flex-shrink-0 pb-1 pr-1">
          <span className="text-[10px] text-muted-foreground hidden sm:inline">
            {text.length}/2000
          </span>

          <button
            type="submit"
            disabled={!text.trim() || isLoading}
            className="p-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-md shadow-blue-500/20 disabled:opacity-40 disabled:pointer-events-none transition-all active:scale-95 flex items-center justify-center"
            title="Send message (Enter)"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  );
};
