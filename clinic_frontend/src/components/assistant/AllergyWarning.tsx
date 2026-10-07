import React from 'react';
import { AlertCircle } from 'lucide-react';
import { AllergyConflictItem } from '@/services/aiAssistantService';

interface AllergyWarningProps {
  conflicts: AllergyConflictItem[];
}

export const AllergyWarning: React.FC<AllergyWarningProps> = ({ conflicts }) => {
  if (!conflicts || conflicts.length === 0) return null;

  return (
    <div className="rounded-2xl border-2 border-amber-500/70 bg-amber-500/10 p-4 shadow-sm">
      <div className="flex items-start gap-3">
        <div className="p-2 rounded-xl bg-amber-500 text-white shadow-sm mt-0.5">
          <AlertCircle className="h-5 w-5" />
        </div>
        <div className="flex-1">
          <h4 className="font-bold text-amber-800 dark:text-amber-300 text-sm">
            Hospital Profile Allergy Conflict Detected
          </h4>
          <div className="mt-2 space-y-2">
            {conflicts.map((c, i) => (
              <p key={i} className="text-xs text-amber-900 dark:text-amber-200 font-medium leading-relaxed">
                ⚠️ {c.warning}
              </p>
            ))}
          </div>
          <p className="mt-2 text-[11px] text-amber-700 dark:text-amber-400 font-semibold">
            Always alert your attending doctor and pharmacist of all recorded allergies before taking any medication.
          </p>
        </div>
      </div>
    </div>
  );
};
