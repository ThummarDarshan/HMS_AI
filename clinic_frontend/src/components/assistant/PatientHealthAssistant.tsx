import React, { useState, useEffect, useRef } from 'react';
import {
  Plus,
  Trash2,
  History,
  MessageSquare,
  RefreshCw,
  X,
  Palette,
  Check,
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import {
  aiAssistantService,
  type ChatMessageRecord,
  type ChatSessionRecord,
} from '@/services/aiAssistantService';
import { ChatWindow } from './ChatWindow';
import { ChatInput } from './ChatInput';
import { AiChatbotLogo } from './AiChatbotLogo';
import type { ChatBackgroundTheme } from './ChatWallpaper';
import { Chatbot3DLoadingScreen } from './Chatbot3DLoadingScreen';
import { toast } from 'sonner';

const THEME_OPTIONS: { id: ChatBackgroundTheme; name: string; desc: string; previewColor: string }[] = [
  {
    id: 'clinical-doodle',
    name: 'Clinical Doodle',
    desc: 'Light medical pattern (Matches Reference)',
    previewColor: 'bg-[#edf3f8]',
  },
  {
    id: 'soft-pearl',
    name: 'Soft Pearl',
    desc: 'Minimalist clean hospital pearl',
    previewColor: 'bg-[#f1f5f9]',
  },
  {
    id: 'teal-breeze',
    name: 'Teal Breeze',
    desc: 'Fresh healthcare mint & cyan',
    previewColor: 'bg-[#e6f7f6]',
  },
  {
    id: 'whatsapp-light',
    name: 'Messaging Light',
    desc: 'Classic soft messaging tones',
    previewColor: 'bg-[#e5ddd5]',
  },
];

export const PatientHealthAssistant: React.FC = () => {
  const { user } = useAuth();
  const [show3DIntro, setShow3DIntro] = useState(true);
  const [sessions, setSessions] = useState<ChatSessionRecord[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | undefined>();
  const [messages, setMessages] = useState<ChatMessageRecord[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSessionsLoading, setIsSessionsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [lastUserMessage, setLastUserMessage] = useState<string>('');

  // Background Theme State (Defaults to 'clinical-doodle' from User's 2nd reference image)
  const [wallpaperTheme, setWallpaperTheme] = useState<ChatBackgroundTheme>(() => {
    return (localStorage.getItem('chat_wallpaper_theme') as ChatBackgroundTheme) || 'clinical-doodle';
  });

  const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false);
  const themeMenuRef = useRef<HTMLDivElement>(null);

  // In-memory Session Cache for instant sub-second opening
  const sessionCacheRef = useRef<Record<string, ChatMessageRecord[]>>({});

  useEffect(() => {
    fetchSessions();
  }, []);

  // Listen to sidebar clicks on AI Health Assistant to trigger 3D loading animation
  useEffect(() => {
    const handleTriggerLoading = () => {
      setShow3DIntro(true);
    };
    window.addEventListener('trigger-ai-3d-loading', handleTriggerLoading);
    return () => {
      window.removeEventListener('trigger-ai-3d-loading', handleTriggerLoading);
    };
  }, []);

  // Close theme menu on outside click
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (themeMenuRef.current && !themeMenuRef.current.contains(e.target as Node)) {
        setIsThemeMenuOpen(false);
      }
    };
    if (isThemeMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isThemeMenuOpen]);

  const handleSelectTheme = (themeId: ChatBackgroundTheme) => {
    setWallpaperTheme(themeId);
    localStorage.setItem('chat_wallpaper_theme', themeId);
    setIsThemeMenuOpen(false);
    toast.success('Background theme updated');
  };

  const fetchSessions = async () => {
    setIsSessionsLoading(true);
    try {
      const data = await aiAssistantService.getSessions();
      setSessions(data);
      // Pre-cache messages in memory so clicking any past consultation opens instantly!
      data.forEach((s) => {
        if (s.messages && s.messages.length > 0) {
          sessionCacheRef.current[s.id] = s.messages;
        }
      });
    } catch (err) {
      console.error('Failed to load chat sessions:', err);
    } finally {
      setIsSessionsLoading(false);
    }
  };

  const handleSelectSession = async (session: ChatSessionRecord) => {
    setCurrentSessionId(session.id);
    setError(null);
    setIsHistoryOpen(false);

    // 1. INSTANT LOAD: Check memory cache or pre-fetched session messages
    const cached = sessionCacheRef.current[session.id] || session.messages;
    if (cached && cached.length > 0) {
      setMessages(cached);
      setIsLoading(false);
      sessionCacheRef.current[session.id] = cached;
      return; // Loaded instantly in 0.01 seconds!
    }

    // 2. Fallback: Fetch from API if not yet in cache
    setIsLoading(true);
    try {
      const fullSession = await aiAssistantService.getSession(session.id);
      const msgs = fullSession.messages || [];
      setMessages(msgs);
      sessionCacheRef.current[session.id] = msgs;
    } catch {
      toast.error('Failed to load consultation history.');
      setError('Unable to load consultation messages.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setCurrentSessionId(undefined);
    setMessages([]);
    setError(null);
    setIsHistoryOpen(false);
  };

  const handleDeleteSession = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    try {
      await aiAssistantService.deleteSession(id);
      setSessions((prev) => prev.filter((s) => s.id !== id));
      if (currentSessionId === id) {
        handleNewChat();
      }
      toast.success('Consultation history deleted.');
    } catch {
      toast.error('Failed to delete consultation.');
    }
  };

  const handleSendMessage = async (userText: string) => {
    if (!userText.trim() || isLoading) return;

    setError(null);
    setLastUserMessage(userText);

    // Optimistically add user message
    const optimisticMsg: ChatMessageRecord = {
      role: 'user',
      content: userText,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, optimisticMsg]);
    setIsLoading(true);

    try {
      const response = await aiAssistantService.sendMessage(userText, currentSessionId);

      if (!currentSessionId && response.session_id) {
        setCurrentSessionId(response.session_id);
        fetchSessions();
      }

      const assistantMsg: ChatMessageRecord = {
        role: 'assistant',
        content: response.answer,
        intent: response.intent,
        symptoms: response.symptoms,
        medications_data: response.medications,
        sources: response.sources,
        red_flags: response.redFlags,
        allergy_conflicts: response.allergyConflicts,
        doctor_review_required: response.doctorReviewRequired,
        is_emergency: response.emergency,
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => {
        const next = [...prev, assistantMsg];
        const activeId = currentSessionId || response.session_id;
        if (activeId) {
          sessionCacheRef.current[activeId] = next;
        }
        return next;
      });
    } catch (err: any) {
      console.error('Chat error:', err);
      const errMsg =
        err?.response?.data?.error ||
        'Unable to retrieve medical information. Please try again.';
      setError(errMsg);
      toast.error(errMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetry = () => {
    if (lastUserMessage) {
      handleSendMessage(lastUserMessage);
    }
  };

  if (show3DIntro) {
    return (
      <Chatbot3DLoadingScreen
        patientName={user?.first_name || user?.username || 'Patient'}
        onComplete={() => setShow3DIntro(false)}
      />
    );
  }

  return (
    <div className="relative flex flex-col h-[calc(100vh-6.8rem)] rounded-2xl sm:rounded-3xl border border-border/80 bg-card/60 backdrop-blur-xl shadow-2xl overflow-hidden animate-fade-in">
      {/* ================= WhatsApp / Messenger Top Navigation Header ================= */}
      <div className="flex items-center justify-between px-3.5 sm:px-5 py-3 border-b border-border/80 bg-card/95 backdrop-blur-md flex-shrink-0 z-20">
        <div className="flex items-center gap-3">
          {/* Dedicated Medical AI Robotic Logo */}
          <AiChatbotLogo size="md" showStatus={true} />

          <div>
            <h2 className="text-sm sm:text-base font-bold text-foreground tracking-tight">
              AI Health Assistant
            </h2>
            <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              <span className="font-semibold text-emerald-600 dark:text-emerald-400">Online</span>
              <span className="text-muted-foreground/40">•</span>
              <span>24/7 Clinical AI Guidance</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-1.5 sm:gap-2">
          {/* Theme Selector Popover (Clean, Solid, Opaque - No Transparency Bleed) */}
          <div className="relative" ref={themeMenuRef}>
            <button
              onClick={() => setIsThemeMenuOpen(!isThemeMenuOpen)}
              className="flex items-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-xl border border-border/80 bg-card hover:bg-muted text-xs font-medium text-muted-foreground hover:text-foreground transition-all shadow-xs"
              title="Change background theme"
            >
              <Palette className="h-4 w-4 text-primary" />
              <span className="hidden lg:inline">Theme</span>
            </button>

            {isThemeMenuOpen && (
              <div
                className="absolute right-0 mt-2 w-64 rounded-2xl border border-border bg-card shadow-2xl p-2.5 z-50 animate-scale-in"
                style={{ backgroundColor: 'hsl(var(--card))' }}
              >
                <div className="px-2 py-1 text-[11px] font-bold text-foreground uppercase tracking-wider border-b border-border/50 mb-1.5">
                  Background Theme
                </div>
                <div className="space-y-1">
                  {THEME_OPTIONS.map((opt) => (
                    <button
                      key={opt.id}
                      type="button"
                      onClick={() => handleSelectTheme(opt.id)}
                      className={`w-full flex items-center justify-between p-2 rounded-xl text-left text-xs transition-colors ${
                        wallpaperTheme === opt.id
                          ? 'bg-primary/10 text-primary font-semibold'
                          : 'hover:bg-muted/60 text-foreground'
                      }`}
                    >
                      <div className="flex items-center gap-2.5">
                        <span
                          className={`w-4 h-4 rounded-full border border-border/80 shadow-xs flex-shrink-0 ${opt.previewColor}`}
                        />
                        <div>
                          <div className="font-medium">{opt.name}</div>
                          <div className="text-[10px] text-muted-foreground">{opt.desc}</div>
                        </div>
                      </div>
                      {wallpaperTheme === opt.id && <Check className="h-4 w-4 text-primary" />}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Past Consultations Toggle Button */}
          <button
            onClick={() => setIsHistoryOpen(!isHistoryOpen)}
            className="flex items-center gap-1.5 px-2.5 sm:px-3 py-1.5 rounded-xl border border-border/80 bg-card hover:bg-muted text-xs font-medium text-muted-foreground hover:text-foreground transition-all shadow-xs"
            title="View Past Consultations"
          >
            <History className="h-4 w-4 text-primary" />
            <span className="hidden md:inline">History</span>
            {sessions.length > 0 && (
              <span className="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-primary/15 text-primary">
                {sessions.length}
              </span>
            )}
          </button>

          {/* New Chat Button */}
          <button
            onClick={handleNewChat}
            className="btn-gradient flex items-center gap-1 px-2.5 sm:px-3.5 py-1.5 text-xs font-semibold rounded-xl shadow-md active:scale-95"
            title="Start New Consultation"
          >
            <Plus className="h-4 w-4" />
            <span className="hidden sm:inline">New Consultation</span>
          </button>
        </div>
      </div>

      {/* ================= Main Conversation Body ================= */}
      <div className="relative flex-1 min-h-0 flex flex-col overflow-hidden">
        {/* Chat Window Area (with selected light theme wallpaper and messages) */}
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          error={error}
          wallpaperTheme={wallpaperTheme}
          onRetry={handleRetry}
          onSelectPrompt={(prompt) => handleSendMessage(prompt)}
        />

        {/* Input Bar (Permanently pinned at bottom) */}
        <div className="flex-shrink-0 p-2.5 sm:p-3.5 border-t border-border/80 bg-card/95 backdrop-blur-md z-10">
          <ChatInput
            onSend={handleSendMessage}
            isLoading={isLoading}
            onQuickPrompt={(prompt) => handleSendMessage(prompt)}
          />
        </div>

        {/* Backdrop for history drawer on mobile */}
        {isHistoryOpen && (
          <div
            onClick={() => setIsHistoryOpen(false)}
            className="absolute inset-0 z-30 bg-black/40 backdrop-blur-xs transition-opacity sm:hidden"
            aria-hidden="true"
          />
        )}

        {/* History Slide-over Drawer */}
        {isHistoryOpen && (
          <div className="absolute inset-y-0 right-0 z-40 w-72 sm:w-84 border-l border-border/80 bg-card/95 backdrop-blur-2xl shadow-2xl p-4 flex flex-col animate-slide-left">
            <div className="flex items-center justify-between pb-3 border-b border-border/80 flex-shrink-0">
              <h3 className="font-semibold text-sm text-foreground flex items-center gap-2">
                <History className="h-4 w-4 text-primary" /> Past Consultations
              </h3>
              <button
                onClick={() => setIsHistoryOpen(false)}
                className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground transition-colors"
                title="Close drawer"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto py-3 space-y-2">
              {isSessionsLoading ? (
                <div className="flex items-center justify-center p-6 text-xs text-muted-foreground">
                  <RefreshCw className="h-4 w-4 animate-spin mr-2" /> Loading consultations...
                </div>
              ) : sessions.length === 0 ? (
                <div className="p-6 text-center text-xs text-muted-foreground">
                  No previous consultation records found.
                </div>
              ) : (
                sessions.map((s) => (
                  <div
                    key={s.id}
                    onClick={() => handleSelectSession(s)}
                    className={`group relative flex items-start justify-between p-3 rounded-xl border transition-all cursor-pointer ${
                      currentSessionId === s.id
                        ? 'border-primary/50 bg-primary/10 shadow-xs'
                        : 'border-border/60 bg-card hover:bg-muted/50'
                    }`}
                  >
                    <div className="flex items-start gap-2.5 overflow-hidden">
                      <MessageSquare className="h-4 w-4 text-primary mt-0.5 flex-shrink-0" />
                      <div className="overflow-hidden">
                        <p className="text-xs font-semibold text-foreground truncate">
                          {s.title || 'Consultation'}
                        </p>
                        {s.last_message && (
                          <p className="text-[11px] text-muted-foreground truncate mt-0.5">
                            {s.last_message.content}
                          </p>
                        )}
                        <span className="text-[10px] text-muted-foreground/80 block mt-1">
                          {new Date(s.updated_at || s.created_at).toLocaleDateString([], {
                            month: 'short',
                            day: 'numeric',
                          })}
                        </span>
                      </div>
                    </div>

                    <button
                      onClick={(e) => handleDeleteSession(e, s.id)}
                      className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg hover:bg-destructive/10 hover:text-destructive text-muted-foreground transition-all ml-1 flex-shrink-0"
                      title="Delete session"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
