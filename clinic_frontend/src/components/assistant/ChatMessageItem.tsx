import React from 'react';
import {
  User,
  Sparkles,
  Activity,
  ShieldCheck,
  Clock,
  Stethoscope,
  ClipboardCheck,
  BookOpen,
  Baby,
  AlertTriangle,
} from 'lucide-react';
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
  const isPediatricRefusal = message.intent === 'PEDIATRIC_REFUSAL';

  if (isUser) {
    return (
      <div className="flex items-start justify-end gap-3.5 animate-fade-in group">
        <div className="max-w-[85%] sm:max-w-[75%] rounded-3xl rounded-tr-md bg-gradient-to-r from-[#2563EB] to-[#1E3A8A] px-5 sm:px-6 py-3.5 sm:py-4 text-white shadow-lg shadow-[#2563EB]/20">
          <p className="text-[14px] sm:text-[15px] font-medium leading-relaxed whitespace-pre-wrap">
            {message.content}
          </p>
          <div className="mt-2 flex items-center justify-end gap-1.5 text-[10px] text-blue-100/80 font-medium">
            <Clock className="h-3 w-3" />
            <span>
              {message.created_at
                ? new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                : 'Just now'}
            </span>
          </div>
        </div>
        <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-[#2563EB]/20 to-[#38BDF8]/20 border border-[#BAE6FD] dark:border-blue-800 flex items-center justify-center text-[#2563EB] dark:text-[#38BDF8] flex-shrink-0 shadow-xs ring-2 ring-white/80 dark:ring-slate-800 mt-1">
          <User className="h-4.5 w-4.5" />
        </div>
      </div>
    );
  }

  // Assistant Message Layout with Soft Medical Aurora Styling
  return (
    <div className="flex items-start gap-3.5 animate-fade-in">
      <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-[#2563EB] to-[#1E3A8A] flex items-center justify-center text-white flex-shrink-0 shadow-md shadow-[#2563EB]/25 ring-2 ring-[#E0F2FE] dark:ring-sky-950 mt-1">
        <Sparkles className="h-5 w-5" />
      </div>

      <div className="flex-1 space-y-3 max-w-[95%] sm:max-w-[90%]">
        {/* Emergency Alert if triggered */}
        {isEmergency ? (
          <EmergencyAlert redFlags={message.red_flags} />
        ) : (
          <div className="aurora-card rounded-3xl rounded-tl-md p-5 sm:p-7 space-y-4">
            {/* Header info inside assistant bubble */}
            <div className="flex items-center justify-between pb-3.5 border-b border-[#D9E2F0]/80 dark:border-slate-800 text-xs text-[#64748B]">
              <div className="flex items-center gap-2.5">
                <span className="font-bold text-[#1E3A8A] dark:text-white text-sm sm:text-base tracking-tight">Velora Clinical Assistant</span>
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-[#E0F2FE] dark:bg-sky-950/60 text-[#0284C7] dark:text-[#38BDF8] border border-[#BAE6FD] dark:border-sky-800">
                  <ShieldCheck className="h-3 w-3" /> Grounded Clinical AI
                </span>
                {isPediatricRefusal && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
                    <Baby className="h-3 w-3" /> Pediatric Safety Guard
                  </span>
                )}
              </div>
              <span className="text-[11px] text-[#64748B] dark:text-slate-400">
                {message.created_at
                  ? new Date(message.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                  : 'Just now'}
              </span>
            </div>

            {/* Symptoms Tags if extracted */}
            {message.symptoms && message.symptoms.length > 0 && (
              <div className="flex flex-wrap items-center gap-1.5 pb-2 border-b border-[#D9E2F0]/60 dark:border-slate-800">
                <span className="text-xs font-semibold text-[#1E3A8A] dark:text-slate-300 flex items-center gap-1 mr-1">
                  <Activity className="h-3.5 w-3.5 text-[#2563EB]" />
                  Identified Symptoms:
                </span>
                {message.symptoms.map((sym, idx) => (
                  <span
                    key={idx}
                    className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[#EFF6FF] dark:bg-blue-950/50 text-[#1E40AF] dark:text-blue-200 border border-[#BFDBFE] dark:border-blue-900"
                  >
                    {sym}
                  </span>
                ))}
              </div>
            )}

            {/* Expanded Medical Abbreviations Tag Chips */}
            {message.abbreviations_expanded && message.abbreviations_expanded.length > 0 && (
              <div className="flex flex-wrap items-center gap-1.5 p-2.5 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-[#D9E2F0]/80 dark:border-slate-800">
                <span className="text-[11px] font-semibold text-[#1E3A8A] dark:text-slate-300 flex items-center gap-1 mr-1">
                  <BookOpen className="h-3.5 w-3.5 text-[#2563EB]" />
                  Medical Terms:
                </span>
                {message.abbreviations_expanded.map((abbr, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-white dark:bg-slate-800 text-[#334155] dark:text-slate-200 border border-slate-200 dark:border-slate-700 shadow-2xs"
                  >
                    <strong className="text-[#2563EB] dark:text-[#38BDF8]">{abbr.abbreviation}</strong>: {abbr.expansion}
                  </span>
                ))}
              </div>
            )}

            {/* Differential Diagnosis Considerations Card */}
            {message.differentials && message.differentials.length > 0 && (
              <div className="rounded-2xl p-4 bg-gradient-to-br from-[#F0F9FF] to-[#EDE9FE]/50 dark:from-slate-900 dark:to-slate-900/80 border border-[#BAE6FD] dark:border-sky-900 shadow-xs space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-[#1E3A8A] dark:text-sky-300">
                    <Stethoscope className="h-4 w-4 text-[#2563EB]" />
                    Differential Considerations
                  </div>
                  <span className="text-[10px] text-[#64748B] dark:text-slate-400 italic">
                    Clinical inquiry • Not final diagnosis
                  </span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                  {message.differentials.map((diff, idx) => (
                    <div
                      key={idx}
                      className="flex items-center gap-2 p-2 rounded-xl bg-white/80 dark:bg-slate-800/80 border border-blue-100 dark:border-slate-700 text-xs font-semibold text-[#1E293B] dark:text-slate-200"
                    >
                      <span className="w-1.5 h-1.5 rounded-full bg-[#2563EB]" />
                      {diff}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Laboratory Report Analysis Card */}
            {message.lab_reports && message.lab_reports.length > 0 && (
              <div className="rounded-2xl p-4 bg-white dark:bg-slate-900 border border-[#BAE6FD] dark:border-sky-900 shadow-sm space-y-3">
                <div className="flex items-center justify-between pb-2 border-b border-slate-100 dark:border-slate-800">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-[#1E3A8A] dark:text-sky-300">
                    <ClipboardCheck className="h-4 w-4 text-[#0284C7]" />
                    Laboratory Report Evaluation
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-50 dark:bg-slate-800 text-blue-700 dark:text-blue-300 font-semibold border border-blue-200 dark:border-slate-700">
                    Reference Ranges Applied
                  </span>
                </div>
                <div className="space-y-2.5">
                  {message.lab_reports.map((report, idx) => {
                    const isHigh = report.flag === 'HIGH';
                    const isLow = report.flag === 'LOW';
                    const badgeClass = isHigh
                      ? 'bg-rose-50 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-rose-800'
                      : isLow
                      ? 'bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-800'
                      : 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800';

                    return (
                      <div
                        key={idx}
                        className="p-3 rounded-xl bg-slate-50/80 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 space-y-1"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-[#1E293B] dark:text-white">
                            {report.test_name}
                          </span>
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${badgeClass}`}>
                            {report.flag === 'NORMAL' ? 'NORMAL' : `${report.flag} (${report.flag_label})`}
                          </span>
                        </div>
                        <div className="flex items-baseline gap-2 text-xs">
                          <span className="font-bold text-sm text-[#0F172A] dark:text-slate-100">
                            {report.value} <span className="text-xs font-normal text-slate-500">{report.unit}</span>
                          </span>
                          <span className="text-[11px] text-slate-500">
                            Ref: {report.reference_range}
                          </span>
                        </div>
                        {report.guidance && (
                          <p className="text-[11px] text-slate-600 dark:text-slate-300 leading-snug pt-1">
                            {report.guidance}
                          </p>
                        )}
                      </div>
                    );
                  })}
                </div>
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
              <div className="space-y-3 pt-3 border-t border-[#D9E2F0]/80 dark:border-slate-800">
                <div className="text-xs font-bold uppercase tracking-wider text-[#1E3A8A] dark:text-sky-300 flex items-center gap-1.5">
                  <ShieldCheck className="h-4 w-4 text-[#2563EB]" />
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

            <div className="flex items-center justify-between text-[11px] text-[#64748B] dark:text-slate-400 pt-1">
              <span className="flex items-center gap-1">
                <ShieldCheck className="h-3.5 w-3.5 text-[#2563EB] dark:text-[#38BDF8]" />
                Verified Clinical Guidance • Velora Care Hospital
              </span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

