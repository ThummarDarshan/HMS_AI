import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  onQuickPrompt?: (prompt: string) => void;
}

const QUICK_PROMPTS = [
  "I have fever and headache. What should I do?",
  "What is paracetamol used for and what are its warnings?",
  "What are the side effects of ibuprofen?",
  "Can amoxicillin be taken with food?",
];

export const ChatInput: React.FC<ChatInputProps> = ({ onSend, isLoading, onQuickPrompt }) => {
  const [text, setText] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    // Focus textarea on mount
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
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  };

  return (
    <div className="w-full space-y-2.5">
      {/* Quick Prompts */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-0.5 scrollbar-none">
        <span className="text-xs font-semibold text-muted-foreground flex items-center gap-1 flex-shrink-0">
          <Sparkles className="h-3 w-3 text-primary" /> Suggestions:
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
            className="flex-shrink-0 text-[11px] sm:text-xs px-3 py-1 rounded-full border border-border bg-card/80 hover:bg-primary/10 hover:border-primary/40 text-foreground transition-all shadow-xs disabled:opacity-50"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Input Box */}
      <form
        onSubmit={handleSubmit}
        className="relative flex items-center gap-2 rounded-2xl border-2 border-primary/30 bg-background/90 p-2 shadow-md focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/20 transition-all"
      >
        <textarea
          ref={textareaRef}
          value={text}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about symptoms, medications, side effects, or warnings... (Press Enter to send)"
          disabled={isLoading}
          rows={1}
          maxLength={2000}
          className="flex-1 max-h-[120px] resize-none bg-transparent px-3 py-1 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none disabled:opacity-50"
        />

        <div className="flex items-center gap-2 flex-shrink-0 pr-1">
          <span className="text-[10px] text-muted-foreground hidden md:inline">
            {text.length}/2000
          </span>

          <button
            type="submit"
            disabled={!text.trim() || isLoading}
            className="btn-gradient p-2.5 rounded-xl text-white shadow-md disabled:opacity-40 disabled:pointer-events-none transition-transform active:scale-95 flex items-center justify-center"
            title="Send message (Enter)"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </form>
    </div>
  );
};
