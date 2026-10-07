import React from 'react';
import { Sparkles } from 'lucide-react';
import { AiChatbotLogo } from './AiChatbotLogo';

export const ChatTypingIndicator: React.FC = () => {
  return (
    <div className="flex items-end gap-2.5 max-w-[85%] sm:max-w-[75%] animate-fade-in select-none">
      {/* Professional AI Health Avatar */}
      <AiChatbotLogo size="sm" showStatus={true} />

      {/* Modern WhatsApp / Messenger Typing Bubble */}
      <div className="rounded-2xl rounded-bl-xs border border-border/70 bg-card/95 backdrop-blur-md px-4 py-3 shadow-sm flex items-center gap-3">
        {/* Three Animated Bouncing Dots */}
        <div className="flex items-center gap-1.5 py-0.5">
          <span
            className="w-2 h-2 rounded-full bg-primary/80 animate-bounce"
            style={{ animationDuration: '0.9s', animationDelay: '0ms' }}
          />
          <span
            className="w-2 h-2 rounded-full bg-primary/80 animate-bounce"
            style={{ animationDuration: '0.9s', animationDelay: '180ms' }}
          />
          <span
            className="w-2 h-2 rounded-full bg-primary/80 animate-bounce"
            style={{ animationDuration: '0.9s', animationDelay: '360ms' }}
          />
        </div>

        <span className="text-[11px] font-medium text-muted-foreground hidden sm:inline flex items-center gap-1">
          <Sparkles className="h-3 w-3 text-primary animate-pulse" />
          Clinical Assistant is thinking...
        </span>
      </div>
    </div>
  );
};
