import React from 'react';
import { ExternalLink, ShieldCheck } from 'lucide-react';
import { SourceCitation as SourceCitationType } from '@/services/aiAssistantService';

interface SourceCitationProps {
  sources: SourceCitationType[];
}

export const SourceCitation: React.FC<SourceCitationProps> = ({ sources }) => {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-border/60">
      <div className="flex items-center gap-1.5 text-xs font-semibold text-emerald-700 dark:text-emerald-400 mb-2">
        <ShieldCheck className="h-4 w-4 text-emerald-600" />
        <span>Authoritative Regulatory Sources</span>
      </div>

      <div className="flex flex-wrap gap-2">
        {sources.map((src, idx) => {
          const isCdsco = src.name.includes('CDSCO') || src.source_type === 'CDSCO';
          const isDailyMed = src.name.includes('DailyMed') || src.source_type === 'DAILYMED';

          const badgeBg = isCdsco
            ? 'bg-amber-500/10 text-amber-700 border-amber-500/30 hover:bg-amber-500/20'
            : isDailyMed
            ? 'bg-blue-500/10 text-blue-700 border-blue-500/30 hover:bg-blue-500/20'
            : 'bg-emerald-500/10 text-emerald-700 border-emerald-500/30 hover:bg-emerald-500/20';

          return (
            <a
              key={idx}
              href={src.url}
              target="_blank"
              rel="noopener noreferrer"
              className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-lg border text-xs font-medium transition-all ${badgeBg}`}
              title={`View official document: ${src.section || src.name}`}
            >
              <span>{src.name}</span>
              {src.section && (
                <span className="opacity-75 text-[11px]">({src.section})</span>
              )}
              <ExternalLink className="h-3 w-3 ml-0.5 opacity-70" />
            </a>
          );
        })}
      </div>
    </div>
  );
};
