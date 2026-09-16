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
        'Unable to retrieve medication information. Please try again.';
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
    <div className="relative flex flex-col h-[calc(100vh-6.8rem)] rounded-3xl border border-border bg-card/60 backdrop-blur-xl shadow-xl overflow-hidden animate-fade-in">
      {/* Assistant Header */}
      <div className="flex items-center justify-between px-5 py-3.5 border-b border-border bg-card/90 backdrop-blur-md flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-2xl bg-gradient-to-tr from-primary to-secondary text-white shadow-md shadow-primary/20">
            <Sparkles className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base sm:text-lg font-bold text-foreground">AI Health Assistant</h2>
              <span className="hidden sm:inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
                <ShieldCheck className="h-3 w-3" /> CDSCO / DailyMed Verified
              </span>
            </div>
            <p className="text-[11px] sm:text-xs text-muted-foreground">
              Official medication documentation & symptom understanding
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Past Consultations Toggle */}
          <button
            onClick={() => setIsHistoryOpen(!isHistoryOpen)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-border bg-card hover:bg-muted text-xs font-medium text-muted-foreground hover:text-foreground transition-colors shadow-xs"
            title="View Past Consultations"
          >
            <History className="h-4 w-4" />
            <span className="hidden md:inline">History ({sessions.length})</span>
          </button>

          {/* New Chat Button */}
          <button
            onClick={handleNewChat}
            className="btn-gradient flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-xl shadow-md"
            title="Start New Chat"
          >
            <Plus className="h-4 w-4" />
            <span className="hidden sm:inline">New Consultation</span>
          </button>
        </div>
      </div>

      {/* Main Body */}
      <div className="relative flex-1 min-h-0 flex flex-col overflow-hidden">
        {/* Chat Window Area (Takes all available remaining height and scrolls) */}
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          error={error}
          onRetry={handleRetry}
          onSelectPrompt={(prompt) => handleSendMessage(prompt)}
        />

        {/* Input Bar (Permanently pinned at bottom) */}
        <div className="flex-shrink-0 p-3 sm:p-4 border-t border-border/80 bg-card/90 backdrop-blur-md">
          <ChatInput
            onSend={handleSendMessage}
            isLoading={isLoading}
            onQuickPrompt={(prompt) => handleSendMessage(prompt)}
          />
        </div>

        {/* History Slide-over Drawer */}
        {isHistoryOpen && (
          <div className="absolute inset-y-0 right-0 z-30 w-72 sm:w-80 border-l border-border bg-card/95 backdrop-blur-2xl shadow-2xl p-4 flex flex-col animate-slide-left">
            <div className="flex items-center justify-between pb-3 border-b border-border flex-shrink-0">
              <h3 className="font-semibold text-sm text-foreground flex items-center gap-2">
                <History className="h-4 w-4 text-primary" /> Past Consultations
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
