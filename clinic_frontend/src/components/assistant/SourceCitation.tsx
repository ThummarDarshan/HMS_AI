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
    <div className="mt-3 pt-3 border-t border-border/50">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center justify-between w-full text-xs font-semibold text-emerald-700 dark:text-emerald-400 hover:text-emerald-800 transition-colors py-1 group"
      >
        <div className="flex items-center gap-1.5">
          <ShieldCheck className="h-4 w-4 text-emerald-600 flex-shrink-0" />
          <span>Verified Regulatory Sources ({uniqueSources.length} verified monographs)</span>
        </div>
        <div className="flex items-center gap-1 text-[11px] text-muted-foreground group-hover:text-foreground">
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
              ? 'bg-amber-500/10 text-amber-800 dark:text-amber-300 border-amber-500/30 hover:bg-amber-500/20'
              : isDailyMed
              ? 'bg-blue-500/10 text-blue-800 dark:text-blue-300 border-blue-500/30 hover:bg-blue-500/20'
              : 'bg-emerald-500/10 text-emerald-800 dark:text-emerald-300 border-emerald-500/30 hover:bg-emerald-500/20';

            return (
              <a
                key={idx}
                href={src.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium transition-all shadow-xs ${badgeBg}`}
                title={`Open official verification link for: ${src.name}`}
              >
                <BookOpen className="h-3 w-3 opacity-75" />
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
