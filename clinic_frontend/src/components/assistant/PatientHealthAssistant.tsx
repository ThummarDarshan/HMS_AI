import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Plus,
  Trash2,
  History,
  MessageSquare,
  ShieldCheck,
  RefreshCw,
  X,
  Bot,
} from 'lucide-react';
import {
  aiAssistantService,
  ChatMessageRecord,
  ChatSessionRecord,
} from '@/services/aiAssistantService';
import { ChatWindow } from './ChatWindow';
import { ChatInput } from './ChatInput';
import { toast } from 'sonner';

export const PatientHealthAssistant: React.FC = () => {
  const [sessions, setSessions] = useState<ChatSessionRecord[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | undefined>();
  const [messages, setMessages] = useState<ChatMessageRecord[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSessionsLoading, setIsSessionsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [lastUserMessage, setLastUserMessage] = useState<string>('');

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    setIsSessionsLoading(true);
    try {
      const data = await aiAssistantService.getSessions();
      setSessions(data);
    } catch (err) {
      console.error('Failed to load chat sessions:', err);
    } finally {
      setIsSessionsLoading(false);
    }
  };

  const handleSelectSession = async (session: ChatSessionRecord) => {
    setCurrentSessionId(session.id);
    setIsLoading(true);
    setError(null);
    setIsHistoryOpen(false);
    try {
      const fullSession = await aiAssistantService.getSession(session.id);
      setMessages(fullSession.messages || []);
    } catch (err) {
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
    } catch (err) {
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

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      console.error('Chat error:', err);
      const errMsg =
        err?.response?.data?.error ||
        'Unable to retrieve response. Please try again.';
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

  return (
    <div className="relative flex flex-col h-[calc(100vh-6.8rem)] rounded-3xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-950/70 backdrop-blur-xl shadow-xl overflow-hidden animate-fade-in">
      {/* Assistant Header with Strong Visual Hierarchy */}
      <div className="flex items-center justify-between px-5 sm:px-6 py-4 border-b border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md flex-shrink-0 z-10 shadow-xs">
        <div className="flex items-center gap-3.5">
          <div className="relative">
            <div className="p-2.5 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 text-white shadow-md shadow-blue-500/20">
              <Bot className="h-5 w-5" />
            </div>
            {/* Pulsing online status indicator */}
            <span className="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full bg-emerald-500 border-2 border-white dark:border-slate-900" />
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white">
                Velora AI Health Assistant
              </h2>
              <span className="hidden sm:inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20">
                <ShieldCheck className="h-3 w-3" /> CDSCO & DailyMed Verified
              </span>
            </div>
            <p className="text-xs text-muted-foreground">
              Clinical triage, symptom intake, and verified medication guidance
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          {/* Past Consultations Toggle */}
          <button
            onClick={() => setIsHistoryOpen(!isHistoryOpen)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-semibold text-slate-700 dark:text-slate-200 transition-colors shadow-xs"
            title="View Past Consultations"
          >
            <History className="h-4 w-4 text-blue-600" />
            <span className="hidden md:inline">History ({sessions.length})</span>
          </button>

          {/* New Chat Button */}
          <button
            onClick={handleNewChat}
            className="flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-semibold rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-md shadow-blue-500/20 transition-all active:scale-95"
            title="Start New Chat"
          >
            <Plus className="h-4 w-4" />
            <span className="hidden sm:inline">New Consultation</span>
          </button>
        </div>
      </div>

      {/* Main Body */}
      <div className="relative flex-1 min-h-0 flex flex-col overflow-hidden">
        {/* Chat Window Area */}
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          error={error}
          onRetry={handleRetry}
          onSelectPrompt={(prompt) => handleSendMessage(prompt)}
        />

        {/* Input Bar (Permanently pinned at bottom) */}
        <div className="flex-shrink-0 p-3 sm:p-4 border-t border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md">
          <ChatInput
            onSend={handleSendMessage}
            isLoading={isLoading}
            onQuickPrompt={(prompt) => handleSendMessage(prompt)}
          />
        </div>

        {/* History Slide-over Drawer */}
        {isHistoryOpen && (
          <div className="absolute inset-y-0 right-0 z-30 w-72 sm:w-80 border-l border-slate-200 dark:border-slate-800 bg-white/98 dark:bg-slate-900/98 backdrop-blur-2xl shadow-2xl p-4 flex flex-col animate-slide-left">
            <div className="flex items-center justify-between pb-3 border-b border-border flex-shrink-0">
              <h3 className="font-semibold text-sm text-foreground flex items-center gap-2">
                <History className="h-4 w-4 text-blue-600" /> Past Consultations
              </h3>
              <button
                onClick={() => setIsHistoryOpen(false)}
                className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto py-3 space-y-2">
              {isSessionsLoading ? (
                <div className="flex items-center justify-center p-6 text-xs text-muted-foreground">
                  <RefreshCw className="h-4 w-4 animate-spin mr-2" /> Loading history...
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
                        ? 'border-blue-600/50 bg-blue-50 dark:bg-blue-950/30 shadow-xs'
                        : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800/60'
                    }`}
                  >
                    <div className="flex items-start gap-2.5 overflow-hidden">
                      <MessageSquare className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
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
