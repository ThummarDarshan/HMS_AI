import React from 'react';
import { User, Sparkles, Activity, ShieldCheck, Clock } from 'lucide-react';
import { ChatMessageRecord } from '@/services/aiAssistantService';
import { EmergencyAlert } from './EmergencyAlert';
import { AllergyWarning } from './AllergyWarning';
import { MedicationCard } from './MedicationCard';
import { SourceCitation } from './SourceCitation';
import { DoctorReviewBanner } from './DoctorReviewBanner';
import { MarkdownRenderer } from './MarkdownRenderer';

interface ChatMessageItemProps {
  message: ChatMessageRecord;
}

export const ChatMessageItem: React.FC<ChatMessageItemProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const isEmergency = message.is_emergency;

  if (isUser) {
    return (
      <div className="flex items-start justify-end gap-3 animate-fade-in group">
        <div className="max-w-[85%] sm:max-w-[70%] rounded-2xl rounded-tr-xs bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-3.5 text-white shadow-md">
          <p className="text-[14px] sm:text-[15px] font-medium leading-relaxed whitespace-pre-wrap">
            {message.content}
          </p>
          <div className="mt-1.5 flex items-center justify-end gap-1 text-[10px] text-blue-100/80">
            <Clock className="h-2.5 w-2.5" />
            <span>
              {message.created_at
                ? new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                : 'Just now'}
            </span>
          </div>
        </div>
        <div className="w-8 h-8 rounded-full bg-blue-600/10 border border-blue-600/20 flex items-center justify-center text-blue-600 dark:text-blue-400 flex-shrink-0 shadow-xs mt-1">
          <User className="h-4 w-4" />
        </div>
      </div>
    );
  }

  // Assistant Message Layout
  return (
    <div className="flex items-start gap-3.5 animate-fade-in">
      <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white flex-shrink-0 shadow-md shadow-blue-500/20 mt-1">
        <Sparkles className="h-4.5 w-4.5" />
      </div>

      <div className="flex-1 space-y-3 max-w-[95%] sm:max-w-[90%]">
        {/* Emergency Alert if triggered */}
        {isEmergency ? (
          <EmergencyAlert redFlags={message.red_flags} />
        ) : (
          <div className="rounded-2xl rounded-tl-xs border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm hover:shadow-md transition-shadow p-5 sm:p-6 space-y-4">
            {/* Header info inside assistant bubble */}
            <div className="flex items-center justify-between pb-3 border-b border-border/50 text-xs text-muted-foreground">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-foreground text-sm">Velora Clinical Assistant</span>
                <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20">
                  <ShieldCheck className="h-3 w-3" /> Grounded RAG
                </span>
              </div>
              <span className="text-[11px]">
                {message.created_at
                  ? new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                  : 'Just now'}
              </span>
            </div>

            {/* Symptoms Tags if extracted */}
            {message.symptoms && message.symptoms.length > 0 && (
              <div className="flex flex-wrap items-center gap-1.5 pb-2 border-b border-border/40">
                <span className="text-xs font-semibold text-muted-foreground flex items-center gap-1 mr-1">
                  <Activity className="h-3.5 w-3.5 text-primary" />
                  Identified Symptoms:
                </span>
                {message.symptoms.map((sym, idx) => (
                  <span
                    key={idx}
                    className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-700 dark:text-blue-300 border border-blue-500/20"
                  >
                    {sym}
                  </span>
                ))}
              </div>
            )}

            {/* Allergy Conflicts if detected */}
            {message.allergy_conflicts && message.allergy_conflicts.length > 0 && (
              <AllergyWarning conflicts={message.allergy_conflicts} />
            )}

            {/* Rich Markdown Rendered Answer */}
            <div className="leading-relaxed">
              <MarkdownRenderer content={message.content} />
            </div>

            {/* Structured Medication Cards */}
            {message.medications_data && message.medications_data.length > 0 && (
              <div className="space-y-3 pt-3 border-t border-border/50">
                <div className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                  <ShieldCheck className="h-4 w-4 text-emerald-600" />
                  Official Medication Monographs
                </div>
                {message.medications_data.map((med, idx) => (
                  <MedicationCard key={idx} medication={med} />
                ))}
              </div>
            )}

            {/* Sources Citation block if not embedded in medication cards */}
            {message.sources && message.sources.length > 0 && (!message.medications_data || message.medications_data.length === 0) && (
              <SourceCitation sources={message.sources} />
            )}

            {/* Doctor review banner */}
            {message.doctor_review_required && !isEmergency && (
              <div className="pt-2">
                <DoctorReviewBanner />
              </div>
            )}

            <div className="flex items-center justify-between text-[11px] text-muted-foreground pt-1">
              <span className="flex items-center gap-1">
                <ShieldCheck className="h-3.5 w-3.5 text-emerald-600" />
                Verified Clinical Guidance • Velora Care Hospital
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
