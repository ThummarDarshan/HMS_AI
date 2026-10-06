import React, { useState } from 'react';
import { Pill, AlertTriangle, CheckCircle2, ShieldAlert, FileText, ChevronDown, ChevronUp, BookOpen } from 'lucide-react';
import { MedicationCardData } from '@/services/aiAssistantService';
import { SourceCitation } from './SourceCitation';

interface MedicationCardProps {
  medication: MedicationCardData;
}

export const MedicationCard: React.FC<MedicationCardProps> = ({ medication }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const sections = medication.sections || {};

  return (
    <div className="rounded-2xl border border-[#D9E2F0] dark:border-slate-800 bg-white/70 dark:bg-slate-900/70 backdrop-blur-md p-3.5 sm:p-4 shadow-xs hover:border-[#38BDF8] transition-all">
      <div
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center justify-between cursor-pointer select-none"
      >
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-[#E0F2FE] dark:bg-sky-950/60 text-[#2563EB] dark:text-[#38BDF8] flex-shrink-0">
            <Pill className="h-5 w-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h4 className="font-bold text-sm sm:text-base text-[#1E3A8A] dark:text-white">
                {medication.name}
              </h4>
              <span className="text-[10px] font-semibold px-2.5 py-0.5 rounded-full bg-[#E0F2FE] text-[#0284C7] dark:bg-sky-950/50 dark:text-sky-300 border border-[#BAE6FD] dark:border-sky-800">
                Official Monograph
              </span>
            </div>
            {medication.brand_names && medication.brand_names.length > 0 && (
              <p className="text-xs text-[#64748B] dark:text-slate-400 mt-0.5">
                Common Indian brands: <span className="font-medium text-[#1E293B] dark:text-slate-200">{medication.brand_names.slice(0, 4).join(', ')}</span>
              </p>
            )}
          </div>
        </div>

        <button
          type="button"
          className="flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-semibold text-[#1E3A8A] dark:text-sky-300 hover:bg-[#F0F5FA] dark:hover:bg-slate-800 transition-colors"
          aria-label={isExpanded ? 'Collapse monograph' : 'Expand monograph'}
        >
          <span className="hidden sm:inline">{isExpanded ? 'Hide' : 'View details'}</span>
          {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </button>
      </div>

      {isExpanded && (
        <div className="mt-4 pt-3 border-t border-border/50 space-y-3 animate-fade-in text-xs sm:text-sm">
          {/* Indications */}
          {sections['INDICATIONS'] && (
            <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
              <div className="flex items-center gap-1.5 font-bold text-emerald-900 dark:text-emerald-300 mb-1">
                <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                <span>Approved Indications</span>
              </div>
              <p className="text-slate-800 dark:text-slate-200 leading-relaxed font-normal">
                {sections['INDICATIONS'].content}
              </p>
            </div>
          )}

          {/* Dosage & Administration */}
          {sections['DOSAGE_AND_ADMINISTRATION'] && (
            <div className="p-3 rounded-xl bg-blue-500/10 border border-blue-500/20">
              <div className="flex items-center gap-1.5 font-bold text-blue-900 dark:text-blue-300 mb-1">
                <BookOpen className="h-4 w-4 text-blue-600" />
                <span>Dosage & Administration</span>
              </div>
              <p className="text-slate-800 dark:text-slate-200 leading-relaxed font-normal">
                {sections['DOSAGE_AND_ADMINISTRATION'].content}
              </p>
            </div>
          )}

          {/* Warnings */}
          {sections['WARNINGS'] && (
            <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
              <div className="flex items-center gap-1.5 font-bold text-amber-900 dark:text-amber-300 mb-1">
                <AlertTriangle className="h-4 w-4 text-amber-600" />
                <span>Official Warnings & Precautions</span>
              </div>
              <p className="text-slate-800 dark:text-slate-200 leading-relaxed font-normal">
                {sections['WARNINGS'].content}
              </p>
            </div>
          )}

          {/* Contraindications */}
          {sections['CONTRAINDICATIONS'] && (
            <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20">
              <div className="flex items-center gap-1.5 font-bold text-rose-900 dark:text-rose-300 mb-1">
                <ShieldAlert className="h-4 w-4 text-rose-600" />
                <span>Contraindications</span>
              </div>
              <p className="text-slate-800 dark:text-slate-200 leading-relaxed font-normal">
                {sections['CONTRAINDICATIONS'].content}
              </p>
            </div>
          )}

          {/* Adverse Reactions */}
          {sections['ADVERSE_REACTIONS'] && (
            <div className="p-3 rounded-xl bg-slate-100 dark:bg-slate-800 border border-border">
              <div className="flex items-center gap-1.5 font-bold text-slate-900 dark:text-white mb-1">
                <FileText className="h-4 w-4 text-primary" />
                <span>Reported Side Effects / Adverse Reactions</span>
              </div>
              <p className="text-slate-700 dark:text-slate-300 leading-relaxed font-normal">
                {sections['ADVERSE_REACTIONS'].content}
              </p>
            </div>
          )}

          {/* Sources */}
          {medication.sources && medication.sources.length > 0 && (
            <SourceCitation sources={medication.sources} />
          )}
        </div>
      )}
    </div>
  );
};
