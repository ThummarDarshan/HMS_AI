import React, { useEffect, useRef } from 'react';
import { Sparkles, Shield, AlertCircle, RefreshCw, HeartPulse } from 'lucide-react';
import { ChatMessageRecord } from '@/services/aiAssistantService';
import { ChatMessageItem } from './ChatMessageItem';

interface ChatWindowProps {
  messages: ChatMessageRecord[];
  isLoading: boolean;
  error?: string | null;
  onRetry?: () => void;
  onSelectPrompt?: (prompt: string) => void;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  isLoading,
  error,
  onRetry,
  onSelectPrompt,
}) => {
  const scrollEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading, error]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 min-h-0 overflow-y-auto flex flex-col items-center justify-center p-4 sm:p-6 text-center animate-fade-in">
        <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl bg-gradient-to-tr from-primary to-secondary text-white flex items-center justify-center shadow-lg shadow-primary/20 mb-3 animate-bounce-subtle">
          <HeartPulse className="h-6 w-6 sm:h-7 sm:w-7" />
        </div>

        <h2 className="text-lg sm:text-xl font-bold tracking-tight text-foreground">
          AI Medication & Symptom Assistant
        </h2>
        <p className="mt-1 text-xs sm:text-sm text-muted-foreground max-w-md leading-relaxed">
          Ask questions regarding symptoms, approved indications, warnings, side effects, and contraindications.
        </p>

        {/* Responsible Medical Notice */}
        <div className="mt-4 max-w-md w-full rounded-2xl border border-border bg-card/70 backdrop-blur-md p-3.5 text-left space-y-1.5 shadow-xs">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-primary">
            <Shield className="h-3.5 w-3.5" />
            <span>Medically Responsible & Verified Information</span>
          </div>
          <ul className="text-[11px] sm:text-xs text-muted-foreground space-y-1 list-disc list-inside">
            <li>Information grounded strictly in official monographs (<strong>CDSCO / DailyMed</strong>).</li>
            <li>This assistant does <strong>NOT</strong> prescribe medicines or replace your doctor.</li>
            <li>In an emergency, immediately call <strong>108 / 112</strong> or go to the nearest ER.</li>
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 min-h-0 overflow-y-auto p-4 sm:p-6 space-y-5">
      {messages.map((msg, idx) => (
        <ChatMessageItem key={msg.id || idx} message={msg} />
      ))}

      {/* Loading Typing Indicator */}
      {isLoading && (
        <div className="flex items-center gap-3 animate-fade-in">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-secondary flex items-center justify-center text-white flex-shrink-0 shadow-sm">
            <Sparkles className="h-4 w-4 animate-spin-slow" />
          </div>
          <div className="rounded-2xl rounded-tl-sm border border-border bg-card/70 px-4 py-2.5 shadow-xs">
            <div className="flex items-center gap-2 text-xs font-medium text-muted-foreground">
              <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              <span>Checking verified regulatory documentation...</span>
            </div>
          </div>
        </div>
      )}

      {/* Error state with retry */}
      {error && (
        <div className="flex items-center justify-between p-3.5 rounded-2xl border border-destructive/30 bg-destructive/10 text-destructive text-xs sm:text-sm animate-shake">
          <div className="flex items-center gap-2">
            <AlertCircle className="h-4 w-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
          {onRetry && (
            <button
              onClick={onRetry}
              className="inline-flex items-center gap-1 font-semibold underline hover:opacity-80"
            >
              <RefreshCw className="h-3 w-3" /> Retry
            </button>
          )}
        </div>
      )}

      <div ref={scrollEndRef} />
    </div>
  );
};
