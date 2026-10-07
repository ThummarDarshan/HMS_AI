import React, { useEffect, useRef, useState, useCallback } from 'react';
import {
  Sparkles,
  Shield,
  AlertCircle,
  RefreshCw,
  HeartPulse,
  Lock,
  ArrowDown,
  Stethoscope,
  Pill,
  Clock,
  Flame,
} from 'lucide-react';
import { ChatMessageRecord } from '@/services/aiAssistantService';
import { ChatMessageItem } from './ChatMessageItem';
import { ChatTypingIndicator } from './ChatTypingIndicator';
import { ChatWallpaper, ChatBackgroundTheme } from './ChatWallpaper';
import { AiChatbotLogo } from './AiChatbotLogo';
import { Chatbot3DAvatar } from './Chatbot3DAvatar';

interface ChatWindowProps {
  messages: ChatMessageRecord[];
  isLoading: boolean;
  error?: string | null;
  wallpaperTheme?: ChatBackgroundTheme;
  onRetry?: () => void;
  onSelectPrompt?: (prompt: string) => void;
}

const STARTER_CARDS = [
  {
    icon: Stethoscope,
    title: 'Symptom Checker',
    desc: 'Describe what you feel for clinical triage guidance',
    prompt: 'What are the early symptoms of Dengue fever and when should I see a doctor?',
    badge: 'Clinical',
  },
  {
    icon: Pill,
    title: 'Medication Safety',
    desc: 'Dosage rules, contraindications, and warnings',
    prompt: 'What is paracetamol used for and what are its maximum daily doses and warnings?',
    badge: 'Monographs',
  },
  {
    icon: Flame,
    title: 'First Aid Guidance',
    desc: 'Immediate emergency actions before professional help',
    prompt: 'What is the immediate first aid protocol for minor to moderate burns?',
    badge: 'Immediate',
  },
  {
    icon: Clock,
    title: 'Hospital Services',
    desc: 'OPD timings, appointments, and insurance TPAs',
    prompt: 'How do I book a doctor appointment and what documents are required for insurance TPA?',
    badge: 'Hospital',
  },
];

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  isLoading,
  error,
  wallpaperTheme = 'clinical-doodle',
  onRetry,
  onSelectPrompt,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const scrollEndRef = useRef<HTMLDivElement>(null);
  const [showScrollBottom, setShowScrollBottom] = useState(false);
  const isNearBottomRef = useRef(true);

  // Monitor scroll position
  const handleScroll = useCallback(() => {
    if (!containerRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
    const distanceFromBottom = scrollHeight - scrollTop - clientHeight;
    const isNearBottom = distanceFromBottom < 100;
    isNearBottomRef.current = isNearBottom;
    setShowScrollBottom(!isNearBottom);
  }, []);

  const scrollToBottom = useCallback((smooth = true) => {
    if (containerRef.current) {
      containerRef.current.scrollTo({
        top: containerRef.current.scrollHeight,
        behavior: smooth ? 'smooth' : 'auto',
      });
    }
    scrollEndRef.current?.scrollIntoView({
      behavior: smooth ? 'smooth' : 'auto',
      block: 'end',
    });
  }, []);

  // Auto-scroll on new messages only when in an active conversation
  useEffect(() => {
    if (messages.length === 0) {
      // When opening chatbot on welcome screen, stay at the top to display 3D avatar & title
      if (containerRef.current) {
        containerRef.current.scrollTop = 0;
      }
      return;
    }

    if (isNearBottomRef.current || messages.length === 1) {
      scrollToBottom(true);
    }
  }, [messages, isLoading, error, scrollToBottom]);

  return (
    <div className="relative flex-1 min-h-0 flex flex-col overflow-hidden">
      {/* Background Wallpaper */}
      <ChatWallpaper theme={wallpaperTheme} />

      {/* Main Scrollable Messages Container */}
      <div
        ref={containerRef}
        onScroll={handleScroll}
        className="relative z-10 flex-1 min-h-0 overflow-y-auto px-3 sm:px-6 py-4 space-y-4 sm:space-y-5 scroll-smooth"
      >
        {messages.length === 0 ? (
          /* ================= Empty / Welcome State with 3D Animated Bot ================= */
          <div className="flex flex-col items-center justify-center min-h-full py-4 text-center animate-fade-in max-w-2xl mx-auto">
            {/* Interactive 3D Animated Chatbot Avatar */}
            <Chatbot3DAvatar className="mb-2" />

            {/* Title & Description */}
            <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground">
              AI Health & Clinical Assistant
            </h2>
            <p className="mt-1.5 text-xs sm:text-sm text-muted-foreground max-w-lg leading-relaxed">
              Your 24/7 intelligent companion for symptom assessment, verified medication monographs, first aid protocols, and clinical queries.
            </p>

            {/* WhatsApp / Medical Security Notice */}
            <div className="mt-3 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-card/80 border border-border/70 text-[11px] font-medium text-muted-foreground shadow-xs">
              <Lock className="h-3 w-3 text-emerald-600" />
              <span>Private & confidential patient consultation session</span>
            </div>

            {/* Interactive Starter Cards Grid */}
            <div className="mt-6 w-full grid grid-cols-1 sm:grid-cols-2 gap-2.5 sm:gap-3 text-left">
              {STARTER_CARDS.map((card, idx) => {
                const IconComponent = card.icon;
                return (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => onSelectPrompt?.(card.prompt)}
                    className="group relative p-3.5 rounded-2xl border border-border/80 bg-card/90 backdrop-blur-md hover:bg-card hover:border-primary/50 shadow-xs hover:shadow-md transition-all text-left flex items-start gap-3 active:scale-[0.99]"
                  >
                    <div className="p-2 rounded-xl bg-primary/10 text-primary group-hover:bg-primary group-hover:text-white transition-colors flex-shrink-0 mt-0.5">
                      <IconComponent className="h-4 w-4" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-1">
                        <span className="text-xs font-bold text-foreground group-hover:text-primary transition-colors">
                          {card.title}
                        </span>
                        <span className="text-[10px] font-semibold px-1.5 py-0.2 rounded-full bg-muted text-muted-foreground border border-border/50">
                          {card.badge}
                        </span>
                      </div>
                      <p className="text-[11px] text-muted-foreground line-clamp-2 mt-0.5 leading-snug">
                        {card.desc}
                      </p>
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Responsible Medical Notice */}
            <div className="mt-6 w-full rounded-2xl border border-border/70 bg-card/85 backdrop-blur-md p-3.5 text-left shadow-xs">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-primary mb-1">
                <Shield className="h-3.5 w-3.5" />
                <span>Medically Responsible AI Disclaimer</span>
              </div>
              <ul className="text-[11px] text-muted-foreground space-y-1 list-disc list-inside leading-relaxed">
                <li>Direct real-time clinical intelligence powered by Velora Clinical AI.</li>
                <li>This guidance is educational and does <strong>not</strong> substitute professional medical advice.</li>
                <li>In any acute medical emergency, immediately dial <strong>108 / 112</strong> or visit the nearest ER.</li>
              </ul>
            </div>
          </div>
        ) : (
          /* ================= Conversation Messages List ================= */
          <>
            {/* WhatsApp-style Session Date / Security Banner */}
            <div className="flex justify-center select-none pt-1 pb-2">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-card/90 border border-border/70 shadow-xs text-[11px] font-medium text-muted-foreground">
                <Lock className="h-3 w-3 text-emerald-600" />
                <span>Messages are encrypted & clinically audited</span>
              </div>
            </div>

            {messages.map((msg, idx) => (
              <ChatMessageItem key={msg.id || idx} message={msg} />
            ))}

            {/* Loading Typing Indicator */}
            {isLoading && <ChatTypingIndicator />}

            {/* Error Message with Retry */}
            {error && (
              <div className="flex items-center justify-between p-3.5 rounded-2xl border border-destructive/30 bg-destructive/10 text-destructive text-xs sm:text-sm animate-shake shadow-xs">
                <div className="flex items-center gap-2">
                  <AlertCircle className="h-4 w-4 flex-shrink-0" />
                  <span>{error}</span>
                </div>
                {onRetry && (
                  <button
                    onClick={onRetry}
                    className="inline-flex items-center gap-1 font-semibold underline hover:opacity-80 px-2 py-1 rounded-lg hover:bg-destructive/15 transition-colors"
                  >
                    <RefreshCw className="h-3.5 w-3.5" /> Retry
                  </button>
                )}
              </div>
            )}
          </>
        )}

        {/* Universal scroll anchor present in both welcome state and active chat */}
        <div ref={scrollEndRef} className="h-1 pointer-events-none" />
      </div>

      {/* Floating Scroll to Bottom Button */}
      {showScrollBottom && (
        <button
          type="button"
          onClick={() => scrollToBottom(true)}
          className="absolute bottom-4 right-5 z-20 p-2.5 rounded-full bg-card/95 hover:bg-card border border-border shadow-lg text-foreground hover:text-primary transition-all duration-200 active:scale-95 animate-fade-in group flex items-center justify-center"
          title="Scroll to latest message"
        >
          <ArrowDown className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
        </button>
      )}
    </div>
  );
};
