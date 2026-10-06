import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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
  ArrowLeft,
  PanelLeftClose,
  PanelLeftOpen,
  Search,
  PhoneCall,
  User as UserIcon,
  HeartPulse,
  ChevronRight,
} from 'lucide-react';
import {
  aiAssistantService,
  ChatMessageRecord,
  ChatSessionRecord,
} from '@/services/aiAssistantService';
import { useAuth } from '@/context/AuthContext';
import { ChatWindow } from './ChatWindow';
import { ChatInput } from './ChatInput';
import { toast } from 'sonner';

export const PatientHealthAssistant: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [sessions, setSessions] = useState<ChatSessionRecord[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | undefined>();
  const [messages, setMessages] = useState<ChatMessageRecord[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSessionsLoading, setIsSessionsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
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
        lab_reports: response.labReports,
        differentials: response.differentials,
        clinical_state: response.clinicalState,
        abbreviations_expanded: response.abbreviationsExpanded,
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

  const filteredSessions = sessions.filter((s) =>
    (s.title || 'Consultation').toLowerCase().includes(searchQuery.toLowerCase())
  );

  const currentSession = sessions.find((s) => s.id === currentSessionId);

  return (
    <div className="relative flex h-screen w-full bg-[#F8FAFD] dark:bg-[#0A0F1D] text-[#1E293B] dark:text-[#F8FAFC] overflow-hidden select-none font-sans">
      {/* Dynamic Animated Ambient Aurora Orbs */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden z-0">
        <div className="absolute -top-24 -left-24 w-[520px] h-[520px] rounded-full bg-[#EDE9FE]/75 dark:bg-purple-950/25 blur-[120px] aurora-orb-1" />
        <div className="absolute top-1/4 -right-24 w-[550px] h-[550px] rounded-full bg-[#E0F2FE]/85 dark:bg-sky-950/25 blur-[130px] aurora-orb-2" />
        <div className="absolute -bottom-24 left-1/3 w-[500px] h-[500px] rounded-full bg-[#E0F7FA]/75 dark:bg-teal-950/20 blur-[130px] aurora-orb-1" />
      </div>

      {/* Left Collapsible Clinical Panel / Consultation Drawer */}
      <aside
        className={`relative z-20 flex flex-col h-full border-r border-[#D9E2F0]/80 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-2xl transition-all duration-300 ease-in-out shadow-[4px_0_24px_rgba(30,58,138,0.03)] ${
          isSidebarOpen ? 'w-72 sm:w-80' : 'w-0 -translate-x-full overflow-hidden border-r-0'
        }`}
      >
        {/* Brand & Workspace Header */}
        <div className="flex items-center justify-between p-4 pb-3 border-b border-[#D9E2F0]/70 dark:border-slate-800 flex-shrink-0">
          <div className="flex items-center gap-2.5 overflow-hidden">
            <div className="p-2 rounded-xl bg-gradient-to-tr from-[#2563EB] to-[#1E3A8A] text-white shadow-md shadow-[#2563EB]/25 flex-shrink-0">
              <HeartPulse className="h-4.5 w-4.5" />
            </div>
            <div className="overflow-hidden">
              <h1 className="font-bold text-sm tracking-tight text-[#1E3A8A] dark:text-white truncate">
                Velora Clinical AI
              </h1>
              <p className="text-[10px] text-[#64748B] dark:text-slate-400 font-medium">
                Health Assistant Workspace
              </p>
            </div>
          </div>

          <button
            onClick={() => setIsSidebarOpen(false)}
            className="p-1.5 rounded-lg text-[#64748B] hover:text-[#1E3A8A] hover:bg-[#F0F5FA] dark:hover:bg-slate-800 transition-colors"
            title="Collapse Sidebar"
          >
            <PanelLeftClose className="h-4 w-4" />
          </button>
        </div>

        {/* New Consultation CTA */}
        <div className="p-3.5 pb-2 flex-shrink-0">
          <button
            onClick={handleNewChat}
            className="w-full flex items-center justify-center gap-2 py-2.5 px-4 text-xs font-semibold rounded-xl aurora-btn-gradient text-white transition-all shadow-md shadow-[#2563EB]/25 active:scale-[0.98]"
          >
            <Plus className="h-4 w-4" />
            <span>New Consultation</span>
          </button>
        </div>

        {/* Filter Search */}
        <div className="px-3.5 pb-2 flex-shrink-0">
          <div className="relative flex items-center">
            <Search className="absolute left-3 h-3.5 w-3.5 text-[#94A3B8]" />
            <input
              type="text"
              placeholder="Search consultations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-8 pr-3 py-1.5 text-xs rounded-xl bg-[#F0F5FA]/80 dark:bg-slate-800/80 border border-[#D9E2F0]/80 dark:border-slate-700 text-[#1E293B] dark:text-slate-200 placeholder:text-[#94A3B8] focus:outline-none focus:border-[#2563EB] transition-colors"
            />
          </div>
        </div>

        {/* Consultations List */}
        <div className="flex-1 overflow-y-auto px-3 py-1 space-y-1.5 custom-scrollbar">
          <div className="px-2 py-1 flex items-center justify-between text-[11px] font-semibold text-[#64748B] uppercase tracking-wider">
            <span>Recent Sessions</span>
            <span>{sessions.length}</span>
          </div>

          {isSessionsLoading ? (
            <div className="flex items-center justify-center p-6 text-xs text-[#64748B]">
              <RefreshCw className="h-4 w-4 animate-spin mr-2 text-[#2563EB]" /> Loading history...
            </div>
          ) : filteredSessions.length === 0 ? (
            <div className="p-6 text-center text-xs text-[#94A3B8]">
              {searchQuery ? 'No matching records.' : 'No previous consultations recorded.'}
            </div>
          ) : (
            filteredSessions.map((s) => {
              const isSelected = currentSessionId === s.id;
              return (
                <div
                  key={s.id}
                  onClick={() => handleSelectSession(s)}
                  className={`group relative flex items-center justify-between p-2.5 rounded-xl border text-xs cursor-pointer transition-all ${
                    isSelected
                      ? 'border-[#2563EB]/60 bg-[#EFF6FF] dark:bg-blue-950/40 text-[#1E3A8A] dark:text-blue-200 shadow-xs font-semibold'
                      : 'border-transparent hover:border-[#D9E2F0] hover:bg-[#F8FAFD] dark:hover:bg-slate-800/50 text-[#334155] dark:text-slate-300'
                  }`}
                >
                  <div className="flex items-center gap-2.5 overflow-hidden">
                    <MessageSquare
                      className={`h-4 w-4 flex-shrink-0 ${
                        isSelected ? 'text-[#2563EB]' : 'text-[#94A3B8] group-hover:text-[#2563EB]'
                      }`}
                    />
                    <div className="overflow-hidden">
                      <p className="truncate font-medium">{s.title || 'Consultation'}</p>
                      <span className="text-[10px] text-[#94A3B8] block mt-0.5">
                        {new Date(s.updated_at || s.created_at).toLocaleDateString([], {
                          month: 'short',
                          day: 'numeric',
                        })}
                      </span>
                    </div>
                  </div>

                  <button
                    onClick={(e) => handleDeleteSession(e, s.id)}
                    className="opacity-0 group-hover:opacity-100 p-1 rounded-lg hover:bg-rose-100 hover:text-rose-600 dark:hover:bg-rose-950 dark:hover:text-rose-300 text-[#94A3B8] transition-all flex-shrink-0 ml-1"
                    title="Delete consultation"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </button>
                </div>
              );
            })
          )}
        </div>

        {/* Bottom Profile & Return to Dashboard */}
        <div className="p-3 border-t border-[#D9E2F0]/80 dark:border-slate-800 flex-shrink-0 space-y-2 bg-white/40 dark:bg-slate-900/40">
          <div className="flex items-center justify-between p-2 rounded-xl bg-[#F0F5FA]/80 dark:bg-slate-800/80 border border-[#D9E2F0]/70 dark:border-slate-700">
            <div className="flex items-center gap-2 overflow-hidden">
              <div className="w-7 h-7 rounded-full bg-gradient-to-tr from-[#2563EB] to-[#1E3A8A] text-white flex items-center justify-center text-xs font-bold flex-shrink-0">
                {user?.first_name ? user.first_name[0] : 'U'}
              </div>
              <div className="overflow-hidden">
                <p className="text-xs font-semibold text-[#1E3A8A] dark:text-white truncate">
                  {user?.full_name || user?.first_name || 'Hospital User'}
                </p>
                <span className="text-[10px] font-semibold text-[#0284C7] dark:text-[#38BDF8]">
                  {user?.role || 'CLINICAL'}
                </span>
              </div>
            </div>
          </div>

          <button
            onClick={() => navigate('/dashboard')}
            className="w-full flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl border border-[#D9E2F0] dark:border-slate-700 hover:bg-[#F0F5FA] dark:hover:bg-slate-800 text-xs font-semibold text-[#1E3A8A] dark:text-slate-200 transition-colors"
          >
            <ArrowLeft className="h-3.5 w-3.5 text-[#2563EB]" />
            <span>Return to Hospital Dashboard</span>
          </button>
        </div>
      </aside>

      {/* Main Conversational Canvas */}
      <main className="relative flex-1 min-w-0 flex flex-col h-full z-10 overflow-hidden">
        {/* Top Header Bar */}
        <header className="flex items-center justify-between px-4 sm:px-6 py-3 border-b border-[#D9E2F0]/80 dark:border-slate-800 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl flex-shrink-0 z-20 shadow-xs">
          <div className="flex items-center gap-3 min-w-0">
            {!isSidebarOpen && (
              <button
                onClick={() => setIsSidebarOpen(true)}
                className="p-1.5 rounded-xl border border-[#D9E2F0] dark:border-slate-800 bg-white/90 dark:bg-slate-900/90 text-[#64748B] hover:text-[#1E3A8A] hover:bg-[#F0F5FA] dark:hover:bg-slate-800 transition-colors shadow-xs flex-shrink-0"
                title="Expand Consultations"
              >
                <PanelLeftOpen className="h-4 w-4 text-[#2563EB]" />
              </button>
            )}

            <div className="flex items-center gap-2.5 min-w-0">
              <div className="relative flex-shrink-0">
                <div className="p-2 rounded-xl bg-gradient-to-tr from-[#2563EB] to-[#1E3A8A] text-white shadow-sm">
                  <Bot className="h-4.5 w-4.5" />
                </div>
                <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-[#38BDF8] border-2 border-white dark:border-slate-900" />
              </div>

              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <h2 className="text-sm sm:text-base font-bold text-[#1E3A8A] dark:text-white truncate">
                    {currentSession?.title || 'Velora Clinical Assistant'}
                  </h2>
                  <span className="hidden sm:inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-[#E0F2FE] text-[#0284C7] dark:bg-sky-950/60 dark:text-[#38BDF8] border border-[#BAE6FD] dark:border-sky-800">
                    <ShieldCheck className="h-3 w-3" /> CDSCO Grounded
                  </span>
                </div>
                <p className="text-[11px] text-[#64748B] dark:text-slate-400 truncate hidden sm:block">
                  AI Symptom Triage & Verified Monograph Guidance
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 flex-shrink-0">
            {/* Emergency Hotline Alert Badge */}
            <a
              href="tel:108"
              className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl bg-rose-50 hover:bg-rose-100 dark:bg-rose-950/40 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-900/60 text-xs font-semibold transition-colors shadow-xs"
              title="Call Ambulance Hotline"
            >
              <PhoneCall className="h-3 w-3 text-rose-600" />
              <span className="hidden md:inline">Emergency:</span> 108 / 112
            </a>

            {!isSidebarOpen && (
              <button
                onClick={handleNewChat}
                className="flex items-center gap-1 px-3 py-1.5 text-xs font-semibold rounded-xl aurora-btn-gradient text-white transition-all shadow-xs active:scale-95"
              >
                <Plus className="h-3.5 w-3.5" />
                <span className="hidden sm:inline">New Chat</span>
              </button>
            )}
          </div>
        </header>

        {/* Scrollable Chat Window Area */}
        <div className="relative flex-1 min-h-0 flex flex-col overflow-hidden">
          <ChatWindow
            messages={messages}
            isLoading={isLoading}
            error={error}
            onRetry={handleRetry}
            onSelectPrompt={(prompt) => handleSendMessage(prompt)}
          />

          {/* Floating Bottom Console Bar */}
          <div className="flex-shrink-0 p-3 sm:p-4 bg-gradient-to-t from-white/95 via-white/80 to-transparent dark:from-slate-900/95 dark:via-slate-900/80 backdrop-blur-md border-t border-[#D9E2F0]/60 dark:border-slate-800">
            <ChatInput
              onSend={handleSendMessage}
              isLoading={isLoading}
              onQuickPrompt={(prompt) => handleSendMessage(prompt)}
            />
            <p className="text-center text-[11px] text-[#94A3B8] mt-2">
              Velora AI provides evidence-based guidance grounded in CDSCO and FDA monographs. In emergencies, dial <strong>108 / 112</strong> immediately.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};
