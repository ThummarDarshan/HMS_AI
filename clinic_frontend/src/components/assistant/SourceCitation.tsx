import React, { useState } from 'react';
import { ExternalLink, ShieldCheck, ChevronDown, ChevronUp, BookOpen } from 'lucide-react';
import { SourceCitation as SourceCitationType } from '@/services/aiAssistantService';

interface SourceCitationProps {
  sources: SourceCitationType[];
}

export const SourceCitation: React.FC<SourceCitationProps> = ({ sources }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!sources || sources.length === 0) return null;

  // Deduplicate sources by name
  const uniqueSources = sources.filter(
    (src, index, self) => index === self.findIndex((s) => s.name === s.name && s.url === s.url)
  );

  return (
    <div className="mt-3 pt-3 border-t border-[#D9E2F0]/80 dark:border-slate-800">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center justify-between w-full text-xs font-semibold text-[#1E3A8A] dark:text-[#38BDF8] hover:text-[#2563EB] transition-colors py-1 group"
      >
        <div className="flex items-center gap-1.5">
          <ShieldCheck className="h-4 w-4 text-[#2563EB] dark:text-[#38BDF8] flex-shrink-0" />
          <span>Verified Regulatory Sources ({uniqueSources.length} verified monographs)</span>
        </div>
        <div className="flex items-center gap-1 text-[11px] text-[#64748B] group-hover:text-[#1E3A8A] dark:group-hover:text-white">
          <span>{isExpanded ? 'Hide' : 'View sources'}</span>
          {isExpanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
        </div>
      </button>

      {isExpanded && (
        <div className="mt-2.5 flex flex-wrap gap-2 animate-fade-in">
          {uniqueSources.map((src, idx) => {
            const isCdsco = src.name.includes('CDSCO') || src.source_type === 'CDSCO';
            const isDailyMed = src.name.includes('DailyMed') || src.source_type === 'DAILYMED';

            const badgeBg = isCdsco
              ? 'bg-[#EFF6FF] dark:bg-sky-950/50 text-[#1E3A8A] dark:text-sky-300 border-[#BFDBFE] dark:border-sky-800 hover:border-[#38BDF8]'
              : isDailyMed
              ? 'bg-[#F0FDF4] dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800 hover:border-emerald-400'
              : 'bg-[#EFF6FF] dark:bg-blue-950/40 text-[#1E3A8A] dark:text-blue-300 border-[#BFDBFE] dark:border-blue-800 hover:border-[#38BDF8]';

            return (
              <a
                key={idx}
                href={src.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-medium transition-all shadow-xs ${badgeBg}`}
                title={`Open official verification link for: ${src.name}`}
              >
                <BookOpen className="h-3.5 w-3.5 opacity-80" />
                <span>{src.name}</span>
                <ExternalLink className="h-3 w-3 ml-0.5 opacity-70" />
              </a>
            );
          })}
        </div>
      )}
    </div>
  );
};
