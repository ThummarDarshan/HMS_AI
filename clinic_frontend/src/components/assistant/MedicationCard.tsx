import React, { useState } from 'react';
import { Pill, AlertTriangle, CheckCircle2, ShieldAlert, FileText, ChevronDown, ChevronUp } from 'lucide-react';
import { MedicationCardData } from '@/services/aiAssistantService';
import { SourceCitation } from './SourceCitation';

interface MedicationCardProps {
  medication: MedicationCardData;
}

export const MedicationCard: React.FC<MedicationCardProps> = ({ medication }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const sections = medication.sections || {};

  return (
    <div className="rounded-2xl border border-border bg-card/90 backdrop-blur-md p-4 shadow-sm hover:shadow-md transition-all">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400">
            <Pill className="h-5 w-5" />
          </div>
          <div>
            <h4 className="font-bold text-base text-foreground">
              {medication.name}
            </h4>
            {medication.brand_names && medication.brand_names.length > 0 && (
              <p className="text-xs text-muted-foreground">
                Common brands: <span className="font-medium">{medication.brand_names.slice(0, 4).join(', ')}</span>
              </p>
            )}
          </div>
        </div>

        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-1.5 rounded-lg hover:bg-muted text-muted-foreground transition-colors"
          aria-label={isExpanded ? 'Collapse card' : 'Expand card'}
        >
          {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </button>
      </div>

      {isExpanded && (
        <div className="mt-4 space-y-3 animate-fade-in text-xs sm:text-sm">
          {/* Indications */}
          {sections['INDICATIONS'] && (
            <div className="p-3 rounded-xl bg-emerald-500/5 border border-emerald-500/20">
              <div className="flex items-center gap-1.5 font-semibold text-emerald-800 dark:text-emerald-400 mb-1">
                <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                <span>Approved Indications</span>
              </div>
              <p className="text-muted-foreground leading-relaxed">
                {sections['INDICATIONS'].content}
              </p>
            </div>
          )}

          {/* Warnings */}
          {sections['WARNINGS'] && (
            <div className="p-3 rounded-xl bg-amber-500/5 border border-amber-500/20">
              <div className="flex items-center gap-1.5 font-semibold text-amber-800 dark:text-amber-400 mb-1">
                <AlertTriangle className="h-4 w-4 text-amber-600" />
                <span>Official Warnings & Precautions</span>
              </div>
              <p className="text-muted-foreground leading-relaxed">
                {sections['WARNINGS'].content}
              </p>
            </div>
          )}

          {/* Contraindications */}
          {sections['CONTRAINDICATIONS'] && (
            <div className="p-3 rounded-xl bg-rose-500/5 border border-rose-500/20">
              <div className="flex items-center gap-1.5 font-semibold text-rose-800 dark:text-rose-400 mb-1">
                <ShieldAlert className="h-4 w-4 text-rose-600" />
                <span>Contraindications</span>
              </div>
              <p className="text-muted-foreground leading-relaxed">
                {sections['CONTRAINDICATIONS'].content}
              </p>
            </div>
          )}

          {/* Adverse Reactions */}
          {sections['ADVERSE_REACTIONS'] && (
            <div className="p-3 rounded-xl bg-muted/40 border border-border">
              <div className="flex items-center gap-1.5 font-semibold text-foreground mb-1">
                <FileText className="h-4 w-4 text-primary" />
                <span>Reported Side Effects / Adverse Reactions</span>
              </div>
              <p className="text-muted-foreground leading-relaxed">
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
