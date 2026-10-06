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
    <div className="max-w-4xl mx-auto w-full space-y-2.5">
      {/* Quick Suggestion Chips with Soft Aurora Styling (Guaranteed Zero Scrollbar) */}
      <div
        className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none no-scrollbar select-none"
        style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        <span className="text-[11px] font-bold text-[#1E3A8A] dark:text-[#38BDF8] uppercase tracking-wider flex items-center gap-1 flex-shrink-0 mr-1">
          <Sparkles className="h-3 w-3 text-[#2563EB]" /> Prompts:
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
            className="flex-shrink-0 text-xs px-3.5 py-1.5 rounded-full border border-[#D9E2F0] dark:border-slate-800 bg-white/95 dark:bg-slate-900/95 hover:border-[#38BDF8] hover:bg-[#F0F7FF] dark:hover:bg-slate-800 text-[#1E3A8A] dark:text-slate-200 transition-all shadow-xs hover:shadow-sm disabled:opacity-50 font-medium active:scale-95"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Floating Input Box Card */}
      <form
        onSubmit={handleSubmit}
        className="relative flex items-end gap-2.5 rounded-2xl bg-white dark:bg-slate-900 border border-[#D9E2F0] dark:border-slate-800 p-2.5 sm:p-3 shadow-[0_12px_36px_-6px_rgba(30,58,138,0.09)] focus-within:border-[#2563EB] focus-within:ring-2 focus-within:ring-[#38BDF8]/20 transition-all"
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
          className="flex-1 max-h-[140px] resize-none bg-transparent px-3 py-1 text-sm sm:text-base text-[#1E293B] dark:text-slate-100 placeholder:text-[#94A3B8] focus:outline-none disabled:opacity-50 leading-relaxed custom-scrollbar"
        />

        <div className="flex items-center gap-2 flex-shrink-0 pb-0.5 pr-1">
          <span className="text-[10px] text-[#94A3B8] hidden sm:inline">
            {text.length}/2000
          </span>

          <button
            type="submit"
            disabled={!text.trim() || isLoading}
            className="p-2.5 rounded-xl aurora-btn-gradient disabled:opacity-40 disabled:pointer-events-none transition-all active:scale-95 flex items-center justify-center shadow-md shadow-[#2563EB]/25"
            title="Send message (Enter)"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  );
};
