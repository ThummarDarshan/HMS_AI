import React, { useEffect, useRef } from 'react';
import { Sparkles, Shield, AlertCircle, RefreshCw, HeartPulse, Stethoscope, Thermometer, Pill, AlertTriangle } from 'lucide-react';
import { ChatMessageRecord } from '@/services/aiAssistantService';
import { ChatMessageItem } from './ChatMessageItem';

interface ChatWindowProps {
  messages: ChatMessageRecord[];
  isLoading: boolean;
  error?: string | null;
  onRetry?: () => void;
  onSelectPrompt?: (prompt: string) => void;
}

const STARTER_CARDS = [
  {
    icon: <Thermometer className="h-4 w-4 text-amber-500" />,
    title: "Mild Fever & Fatigue",
    desc: "I have a low fever (99.5°F) since yesterday morning",
    prompt: "I have a low-grade fever of 99.5 F since yesterday morning with slight tiredness. What should I do?",
  },
  {
    icon: <Pill className="h-4 w-4 text-blue-500" />,
    title: "Headache & Cold",
    desc: "Mild throbbing headache and runny nose",
    prompt: "I have had a mild headache and runny nose for 1 day. What safe medication can I take?",
  },
  {
    icon: <AlertTriangle className="h-4 w-4 text-red-500" />,
    title: "High Fever / Urgent Check",
    desc: "High fever (103°F) for multiple days with chills",
    prompt: "I have had high fever 103.5 F for 4 days with severe shivering and body weakness.",
  },
  {
    icon: <Stethoscope className="h-4 w-4 text-emerald-500" />,
    title: "Medication Information",
    desc: "CDSCO monograph & safe usage",
    prompt: "What is paracetamol used for, what is the safe dosage, and what are its contraindications?",
  },
];

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
        <div className="max-w-2xl w-full mx-auto space-y-6">
          <div className="flex flex-col items-center">
            <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-3xl bg-gradient-to-tr from-blue-600 to-indigo-600 text-white flex items-center justify-center shadow-xl shadow-blue-500/25 mb-3.5 animate-bounce-subtle">
              <HeartPulse className="h-7 w-7 sm:h-8 sm:w-8" />
            </div>

            <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">
              Clinical Health & Symptom Assistant
            </h2>
            <p className="mt-1.5 text-xs sm:text-sm text-muted-foreground max-w-lg leading-relaxed">
              Describe your symptoms from home. Our AI assistant will ask needed clinical details, assess criticality, recommend safe OTC relief with official proof, or refer you to hospital doctors.
            </p>
          </div>

          {/* Quick Consultation Starters */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-left pt-2">
            {STARTER_CARDS.map((card, idx) => (
              <button
                key={idx}
                onClick={() => onSelectPrompt && onSelectPrompt(card.prompt)}
                className="p-3.5 rounded-2xl border border-border/80 bg-card/90 hover:border-primary/50 hover:bg-primary/5 hover:shadow-md transition-all text-left flex items-start gap-3 group"
              >
                <div className="p-2 rounded-xl bg-muted group-hover:bg-primary/10 transition-colors mt-0.5">
                  {card.icon}
                </div>
                <div>
                  <h4 className="text-xs sm:text-sm font-semibold text-foreground group-hover:text-primary transition-colors">
                    {card.title}
                  </h4>
                  <p className="text-[11px] sm:text-xs text-muted-foreground line-clamp-1 mt-0.5">
                    {card.desc}
                  </p>
                </div>
              </button>
            ))}
          </div>

          {/* Medically Responsible Notice */}
          <div className="rounded-2xl border border-border/70 bg-card/60 backdrop-blur-md p-3.5 text-left space-y-1.5 shadow-xs">
            <div className="flex items-center gap-1.5 text-xs font-semibold text-primary">
              <Shield className="h-3.5 w-3.5" />
              <span>Grounded in CDSCO (Govt of India) & DailyMed (FDA) Clinical Monologues</span>
            </div>
            <ul className="text-[11px] sm:text-xs text-muted-foreground space-y-0.5 list-disc list-inside">
              <li>Provides safe over-the-counter medication with proof for non-critical cases.</li>
              <li>Detects red flags and instructs immediate doctor consultation for critical symptoms.</li>
              <li>In a medical emergency, call <strong>108 / 112</strong> immediately.</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 min-h-0 overflow-y-auto px-4 sm:px-6 py-6">
      {/* Centered chat message stream */}
      <div className="max-w-4xl mx-auto w-full space-y-6">
        {messages.map((msg, idx) => (
          <ChatMessageItem key={msg.id || idx} message={msg} />
        ))}

        {/* Loading Typing Indicator */}
        {isLoading && (
          <div className="flex items-start gap-3.5 animate-fade-in">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white flex-shrink-0 shadow-md shadow-blue-500/20 mt-1">
              <Sparkles className="h-4.5 w-4.5 animate-spin-slow" />
            </div>
            <div className="rounded-2xl rounded-tl-xs border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-5 py-3.5 shadow-sm">
              <div className="flex items-center gap-2.5 text-xs sm:text-sm font-medium text-muted-foreground">
                <span className="flex space-x-1">
                  <span className="w-2 h-2 rounded-full bg-blue-600 animate-bounce [animation-delay:-0.3s]" />
                  <span className="w-2 h-2 rounded-full bg-blue-600 animate-bounce [animation-delay:-0.15s]" />
                  <span className="w-2 h-2 rounded-full bg-blue-600 animate-bounce" />
                </span>
                <span>Evaluating symptoms & checking regulatory medical monographs...</span>
              </div>
            </div>
          </div>
        )}

        {/* Error state with retry */}
        {error && (
          <div className="flex items-center justify-between p-4 rounded-2xl border border-destructive/30 bg-destructive/10 text-destructive text-xs sm:text-sm animate-shake">
            <div className="flex items-center gap-2">
              <AlertCircle className="h-4.5 w-4.5 flex-shrink-0" />
              <span>{error}</span>
            </div>
            {onRetry && (
              <button
                onClick={onRetry}
                className="inline-flex items-center gap-1.5 font-semibold underline hover:opacity-80 ml-2"
              >
                <RefreshCw className="h-3.5 w-3.5" /> Retry
              </button>
            )}
          </div>
        )}

        <div ref={scrollEndRef} />
      </div>
    </div>
  );
};
