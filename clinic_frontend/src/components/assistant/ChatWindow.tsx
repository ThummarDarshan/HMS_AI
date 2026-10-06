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
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-[#2563EB] to-[#1E3A8A] text-white flex items-center justify-center shadow-xl shadow-[#2563EB]/25 ring-8 ring-[#E0F2FE]/70 dark:ring-sky-950/40 mb-3.5 animate-bounce-subtle">
              <HeartPulse className="h-8 w-8 text-white" />
            </div>

            <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-[#1E3A8A] dark:text-white">
              Clinical Health & Symptom Assistant
            </h2>
            <p className="mt-1.5 text-xs sm:text-sm text-[#475569] dark:text-slate-300 max-w-lg leading-relaxed">
              Describe your symptoms from home. Our AI assistant evaluates symptoms, cross-checks official CDSCO and FDA clinical monographs, and guides you to safe OTC relief or immediate physician care.
            </p>
          </div>

          {/* Quick Consultation Starters with Soft Aurora Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-left pt-2">
            {STARTER_CARDS.map((card, idx) => (
              <button
                key={idx}
                onClick={() => onSelectPrompt && onSelectPrompt(card.prompt)}
                className="aurora-card p-4 rounded-2xl text-left flex items-start gap-3.5 group hover:border-[#38BDF8] hover:bg-white/95 dark:hover:bg-slate-800 transition-all duration-300 hover:shadow-lg hover:shadow-[#38BDF8]/10 hover:-translate-y-0.5"
              >
                <div className="p-2.5 rounded-xl bg-[#EFF6FF] dark:bg-sky-950/50 group-hover:bg-[#E0F2FE] dark:group-hover:bg-sky-900/60 transition-colors mt-0.5 flex-shrink-0">
                  {card.icon}
                </div>
                <div>
                  <h4 className="text-xs sm:text-sm font-semibold text-[#1E3A8A] dark:text-white group-hover:text-[#2563EB] dark:group-hover:text-[#38BDF8] transition-colors">
                    {card.title}
                  </h4>
                  <p className="text-[11px] sm:text-xs text-[#64748B] dark:text-slate-400 line-clamp-1 mt-0.5">
                    {card.desc}
                  </p>
                </div>
              </button>
            ))}
          </div>

          {/* Medically Responsible Notice */}
          <div className="aurora-card rounded-2xl p-4 text-left space-y-2 border border-[#D9E2F0] dark:border-slate-800">
            <div className="flex items-center gap-2 text-xs font-semibold text-[#1E3A8A] dark:text-[#38BDF8]">
              <Shield className="h-4 w-4 text-[#2563EB] dark:text-[#38BDF8]" />
              <span>Grounded in CDSCO (Govt of India) & DailyMed (FDA) Clinical Monographs</span>
            </div>
            <ul className="text-[11px] sm:text-xs text-[#475569] dark:text-slate-300 space-y-1 list-disc list-inside">
              <li>Provides verified over-the-counter relief guidance with official proof for mild cases.</li>
              <li>Instantly flags red flag symptoms requiring clinical doctor assessment.</li>
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
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-[#2563EB] to-[#1E3A8A] flex items-center justify-center text-white flex-shrink-0 shadow-md shadow-[#2563EB]/20 mt-1">
              <Sparkles className="h-4.5 w-4.5 animate-spin-slow" />
            </div>
            <div className="aurora-card rounded-2xl rounded-tl-xs px-5 py-3.5">
              <div className="flex items-center gap-2.5 text-xs sm:text-sm font-medium text-[#475569] dark:text-slate-300">
                <span className="flex space-x-1">
                  <span className="w-2 h-2 rounded-full bg-[#2563EB] animate-bounce [animation-delay:-0.3s]" />
                  <span className="w-2 h-2 rounded-full bg-[#2563EB] animate-bounce [animation-delay:-0.15s]" />
                  <span className="w-2 h-2 rounded-full bg-[#2563EB] animate-bounce" />
                </span>
                <span>Evaluating symptoms & checking regulatory medical monographs...</span>
              </div>
            </div>
          </div>
        )}

        {/* Error state with retry */}
        {error && (
          <div className="flex items-center justify-between p-4 rounded-2xl border border-rose-300/70 bg-rose-50/90 dark:bg-rose-950/40 text-rose-800 dark:text-rose-200 text-xs sm:text-sm animate-shake shadow-xs">
            <div className="flex items-center gap-2">
              <AlertCircle className="h-4.5 w-4.5 flex-shrink-0 text-rose-600" />
              <span>{error}</span>
            </div>
            {onRetry && (
              <button
                onClick={onRetry}
                className="inline-flex items-center gap-1.5 font-semibold underline hover:opacity-80 ml-2 text-rose-700 dark:text-rose-300"
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
