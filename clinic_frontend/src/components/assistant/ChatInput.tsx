import React, { useState, useRef, useEffect } from 'react';
import { ArrowUp, Sparkles, X, CornerDownLeft } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
  onQuickPrompt?: (prompt: string) => void;
}

const QUICK_PROMPTS = [
  'How do I book a doctor appointment?',
  'What are the hospital visiting hours?',
  'What is the first aid protocol for burns?',
  'What is Dengue fever and what are its symptoms?',
  'What is paracetamol used for and what are its warnings?',
  'What is the best diet for managing Type 2 Diabetes?',
  'How does cashless health insurance TPA work?',
  'What should I do if someone faints?',
];

export const ChatInput: React.FC<ChatInputProps> = ({
  onSend,
  isLoading,
  onQuickPrompt,
}) => {
  const [text, setText] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    // Keep focus on input without forcing parent container to auto-scroll
    if (!isLoading) {
      textareaRef.current?.focus({ preventScroll: true });
    }
  }, [isLoading]);

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
      textareaRef.current.style.height = `${Math.min(
        textareaRef.current.scrollHeight,
        140
      )}px`;
    }
  };

  const handleClear = () => {
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.focus();
    }
  };

  const hasContent = text.trim().length > 0;

  return (
    <div className="w-full space-y-2 select-none">
      {/* Suggestions Pills Bar (smooth horizontal scroll without ugly track) */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
        <span className="text-[11px] font-semibold text-muted-foreground flex items-center gap-1 flex-shrink-0 pl-1">
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
            className="flex-shrink-0 text-[11px] px-3 py-1 rounded-full border border-border/80 bg-card/90 hover:bg-card hover:border-primary/40 text-foreground/90 hover:text-primary transition-all shadow-xs disabled:opacity-50 whitespace-nowrap active:scale-95"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Modern WhatsApp-style Input Bar */}
      <form
        onSubmit={handleSubmit}
        className="relative flex items-end gap-2 rounded-2xl sm:rounded-3xl border border-border/90 bg-card/95 backdrop-blur-xl p-1.5 sm:p-2 shadow-sm focus-within:border-primary/70 focus-within:ring-2 focus-within:ring-primary/20 transition-all"
      >
        {/* Multiline auto-expanding textarea */}
        <textarea
          ref={textareaRef}
          value={text}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
          placeholder="Type a health question, symptoms, or medication query..."
          disabled={isLoading}
          rows={1}
          maxLength={2000}
          aria-label="Chat message"
          className="flex-1 max-h-[140px] min-h-[38px] resize-none bg-transparent px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none disabled:opacity-50 leading-relaxed font-sans"
        />

        {/* Clear Button (shown when text exists) */}
        {hasContent && (
          <button
            type="button"
            onClick={handleClear}
            disabled={isLoading}
            className="p-2 rounded-xl text-muted-foreground hover:text-foreground hover:bg-muted/60 transition-colors flex-shrink-0 mb-0.5"
            title="Clear text"
          >
            <X className="h-4 w-4" />
          </button>
        )}

        {/* Character counter (Desktop only) */}
        <div className="hidden lg:flex items-center text-[10px] text-muted-foreground/80 mb-2.5 flex-shrink-0 px-1">
          {text.length}/2000
        </div>

        {/* Modern WhatsApp-style Send Button */}
        <button
          type="submit"
          disabled={!hasContent || isLoading}
          aria-label="Send message"
          className={`flex-shrink-0 w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center transition-all duration-200 shadow-md ${
            hasContent && !isLoading
              ? 'bg-gradient-to-r from-primary to-secondary text-white hover:shadow-lg hover:shadow-primary/30 hover:scale-105 active:scale-95'
              : 'bg-muted text-muted-foreground cursor-not-allowed opacity-50'
          }`}
          title="Send message (Enter)"
        >
          <ArrowUp className="h-4 w-4 sm:h-4.5 sm:w-4.5 stroke-[2.5]" />
        </button>
      </form>

      {/* Helpful Hint Bar below */}
      <div className="flex items-center justify-between px-2 text-[10px] text-muted-foreground/75">
        <span className="flex items-center gap-1">
          <CornerDownLeft className="h-2.5 w-2.5" /> Press <kbd className="px-1 py-0.2 rounded bg-muted font-mono text-[9px]">Enter</kbd> to send, <kbd className="px-1 py-0.2 rounded bg-muted font-mono text-[9px]">Shift+Enter</kbd> for new line
        </span>
        <span className="hidden sm:inline">
          Velora Medical Intelligence
        </span>
      </div>
    </div>
  );
};
