import React from 'react';
import { User, Sparkles, Activity, ShieldCheck } from 'lucide-react';
import { ChatMessageRecord } from '@/services/aiAssistantService';
import { EmergencyAlert } from './EmergencyAlert';
import { AllergyWarning } from './AllergyWarning';
import { MedicationCard } from './MedicationCard';
import { SourceCitation } from './SourceCitation';
import { DoctorReviewBanner } from './DoctorReviewBanner';
import { cn } from '@/lib/utils';

interface ChatMessageItemProps {
  message: ChatMessageRecord;
}

export const ChatMessageItem: React.FC<ChatMessageItemProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const isEmergency = message.is_emergency;

  if (isUser) {
    return (
      <div className="flex items-start justify-end gap-3 animate-fade-in">
        <div className="max-w-[85%] sm:max-w-[75%] rounded-2xl rounded-tr-sm bg-primary px-4 py-3 text-primary-foreground shadow-md">
          <p className="text-sm font-medium whitespace-pre-wrap leading-relaxed">
            {message.content}
          </p>
          <span className="mt-1 block text-[10px] opacity-75 text-right">
            {message.created_at ? new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Just now'}
          </span>
        </div>
        <div className="w-8 h-8 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center text-primary flex-shrink-0">
          <User className="h-4 w-4" />
        </div>
      </div>
    );
  }

  // Assistant Message Layout
  return (
    <div className="flex items-start gap-3 animate-fade-in">
      <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-secondary flex items-center justify-center text-white flex-shrink-0 shadow-sm mt-1">
        <Sparkles className="h-4 w-4" />
      </div>

      <div className="flex-1 space-y-3 max-w-[95%] sm:max-w-[85%]">
        {/* Emergency Alert if triggered */}
        {isEmergency ? (
          <EmergencyAlert redFlags={message.red_flags} />
        ) : (
          <div className="rounded-2xl rounded-tl-sm border border-border bg-card/80 backdrop-blur-md p-4 sm:p-5 shadow-sm space-y-4">
            {/* Symptoms Tags if extracted */}
            {message.symptoms && message.symptoms.length > 0 && (
              <div className="flex flex-wrap items-center gap-1.5 pb-2 border-b border-border/50">
                <span className="text-xs font-semibold text-muted-foreground flex items-center gap-1 mr-1">
                  <Activity className="h-3.5 w-3.5 text-primary" />
                  Identified Symptoms:
                </span>
                {message.symptoms.map((sym, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-0.5 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20"
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

            {/* Answer Content */}
            <div className="prose prose-sm dark:prose-invert max-w-none text-foreground leading-relaxed whitespace-pre-wrap">
              {message.content}
            </div>

            {/* Structured Medication Cards */}
            {message.medications_data && message.medications_data.length > 0 && (
              <div className="space-y-3 pt-2">
                <div className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                  Verified Medication Monographs
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
                <ShieldCheck className="h-3 w-3 text-emerald-600" />
                Verified Clinical Guidance
              </span>
              <span>
                {message.created_at ? new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Just now'}
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
