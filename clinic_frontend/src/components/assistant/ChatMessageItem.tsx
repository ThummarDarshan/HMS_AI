import React, { useState } from 'react';
import {
  User,
  Activity,
  CheckCheck,
  Copy,
  Check,
  Sparkles,
  ShieldCheck,
} from 'lucide-react';
import { AiChatbotLogo } from './AiChatbotLogo';
import { ChatMessageRecord } from '@/services/aiAssistantService';
import { EmergencyAlert } from './EmergencyAlert';
import { AllergyWarning } from './AllergyWarning';
import { MedicationCard } from './MedicationCard';
import { SourceCitation } from './SourceCitation';
import { DoctorReviewBanner } from './DoctorReviewBanner';
import { MarkdownRenderer } from './MarkdownRenderer';
import { toast } from 'sonner';

interface ChatMessageItemProps {
  message: ChatMessageRecord;
}

export const ChatMessageItem: React.FC<ChatMessageItemProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const isEmergency = message.is_emergency;
  const [copied, setCopied] = useState(false);

  const formattedTime = message.created_at
    ? new Date(message.created_at).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
      })
    : new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const handleCopyContent = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      toast.success('Response copied to clipboard');
      setTimeout(() => setCopied(false), 2000);
    } catch {
      toast.error('Failed to copy response');
    }
  };

  // ================= USER MESSAGE (Right-aligned, WhatsApp bubble) =================
  if (isUser) {
    return (
      <div className="flex items-end justify-end gap-2 sm:gap-2.5 animate-fade-in group">
        <div className="flex flex-col items-end max-w-[85%] sm:max-w-[75%] md:max-w-[70%]">
          {/* User Chat Bubble */}
          <div className="relative rounded-2xl rounded-tr-xs bg-gradient-to-r from-primary to-secondary text-primary-foreground px-4 py-2.5 sm:px-4.5 sm:py-3 shadow-md shadow-primary/10 transition-all hover:shadow-lg">
            <p className="text-sm font-normal sm:font-medium leading-relaxed whitespace-pre-wrap break-words selection:bg-white/30">
              {message.content}
            </p>

            {/* Bubble Footer: Timestamp & WhatsApp Delivery Tick */}
            <div className="flex items-center justify-end gap-1 mt-1 text-[11px] text-primary-foreground/75 select-none">
              <span>{formattedTime}</span>
              <CheckCheck className="h-3.5 w-3.5 text-primary-foreground/90 ml-0.5" />
            </div>
          </div>
        </div>

        {/* User Avatar */}
        <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-primary/15 border border-primary/25 flex items-center justify-center text-primary flex-shrink-0 shadow-xs mb-1">
          <User className="h-3.5 w-3.5 sm:h-4 sm:w-4" />
        </div>
      </div>
    );
  }

  // ================= ASSISTANT MESSAGE (Left-aligned, WhatsApp/ChatGPT bubble) =================
  return (
    <div className="flex items-start gap-2 sm:gap-3 animate-fade-in group">
      {/* Professional AI Health Avatar */}
      <AiChatbotLogo size="sm" showStatus={false} className="mt-0.5" />

      <div className="flex-1 space-y-2.5 max-w-[92%] sm:max-w-[85%] md:max-w-[80%] min-w-0">
        {/* Emergency Alert (High priority if triggered) */}
        {isEmergency ? (
          <EmergencyAlert redFlags={message.red_flags} />
        ) : (
          /* Main Assistant Card Bubble */
          <div className="rounded-2xl rounded-tl-xs border border-border/80 bg-card/95 backdrop-blur-md p-3.5 sm:p-5 shadow-sm hover:shadow-md transition-all space-y-3.5 overflow-hidden">
            {/* Header Meta: Assistant Tag & AI Model Pill */}
            <div className="flex items-center justify-between pb-2 border-b border-border/50 text-xs">
              <div className="flex items-center gap-1.5 font-semibold text-foreground">
                <Sparkles className="h-3.5 w-3.5 text-primary" />
                <span>AI Clinical Assistant</span>
                <span className="inline-flex items-center gap-0.5 px-1.5 py-0.2 rounded-full text-[10px] font-medium bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
                  <ShieldCheck className="h-2.5 w-2.5" /> Verified
                </span>
              </div>
              <span className="text-[11px] text-muted-foreground hidden sm:inline">
                Velora Medical Intelligence
              </span>
            </div>

            {/* Identified Symptoms Tags (displayed on complete consultation) */}
            {message.intent !== 'SYMPTOM_CLARIFICATION' && message.symptoms && message.symptoms.length > 0 && (
              <div className="flex flex-wrap items-center gap-1.5 pt-0.5 pb-2 border-b border-border/40">
                <span className="text-[11px] font-semibold text-muted-foreground flex items-center gap-1 mr-1">
                  <Activity className="h-3.5 w-3.5 text-primary" />
                  Identified Symptoms:
                </span>
                {message.symptoms.map((sym, idx) => (
                  <span
                    key={idx}
                    className="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-primary/10 text-primary border border-primary/20 shadow-xs"
                  >
                    {sym}
                  </span>
                ))}
              </div>
            )}

            {/* Allergy Conflicts Banner (if detected) */}
            {message.allergy_conflicts && message.allergy_conflicts.length > 0 && (
              <AllergyWarning conflicts={message.allergy_conflicts} />
            )}

            {/* Rich Markdown Response Body */}
            <div className="py-0.5">
              <MarkdownRenderer content={message.content} />
            </div>

            {/* Verified Medication Monographs (if provided) */}
            {message.medications_data && message.medications_data.length > 0 && (
              <div className="space-y-2.5 pt-2 border-t border-border/50">
                <div className="text-[11px] font-bold uppercase tracking-wider text-muted-foreground">
                  Verified Medication Monographs
                </div>
                {message.medications_data.map((med, idx) => (
                  <MedicationCard key={idx} medication={med} />
                ))}
              </div>
            )}

            {/* Authoritative Sources Citations (if standalone) */}
            {message.sources &&
              message.sources.length > 0 &&
              (!message.medications_data || message.medications_data.length === 0) && (
                <SourceCitation sources={message.sources} />
              )}

            {/* In-person Doctor Review Banner (only on complete consultation) */}
            {message.doctor_review_required && !isEmergency && message.intent !== 'SYMPTOM_CLARIFICATION' && (
              <div className="pt-2">
                <DoctorReviewBanner />
              </div>
            )}

            {/* Assistant Footer: Copy button, timestamp & clinical disclaimer */}
            <div className="flex items-center justify-between text-[11px] text-muted-foreground pt-2 border-t border-border/40 select-none">
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={handleCopyContent}
                  className="inline-flex items-center gap-1 px-2 py-1 rounded-lg hover:bg-muted text-muted-foreground hover:text-foreground transition-colors font-medium"
                  title="Copy response to clipboard"
                >
                  {copied ? (
                    <>
                      <Check className="h-3 w-3 text-emerald-500" />
                      <span className="text-emerald-500 font-semibold">Copied</span>
                    </>
                  ) : (
                    <>
                      <Copy className="h-3 w-3" />
                      <span>Copy</span>
                    </>
                  )}
                </button>
              </div>

              <div className="flex items-center gap-1 text-[11px]">
                <span>{formattedTime}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
