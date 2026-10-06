import React from 'react';
import { AlertTriangle, PhoneCall, Hospital } from 'lucide-react';
import { RedFlagItem } from '@/services/aiAssistantService';

interface EmergencyAlertProps {
  redFlags?: RedFlagItem[];
}

export const EmergencyAlert: React.FC<EmergencyAlertProps> = ({ redFlags }) => {
  return (
    <div className="rounded-2xl border-2 border-red-500/80 bg-red-50/90 dark:bg-red-950/40 p-5 backdrop-blur-md shadow-lg shadow-red-500/10 animate-pulse-slow">
      <div className="flex items-start gap-3">
        <div className="p-2.5 rounded-xl bg-red-600 text-white shadow-md shadow-red-500/20">
          <AlertTriangle className="h-6 w-6" />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-bold text-red-700 dark:text-red-400">
            Emergency Medical Alert
          </h3>
          <p className="mt-1 text-sm text-red-900 dark:text-red-200 leading-relaxed font-medium">
            Your message describes symptoms requiring **immediate in-person medical evaluation**. 
            Do not wait for online chat or rely on automated advice.
          </p>

          {redFlags && redFlags.length > 0 && (
            <div className="mt-3 space-y-1 bg-red-500/10 p-3 rounded-xl border border-red-500/20">
              <p className="text-xs font-semibold text-red-800 dark:text-red-300 uppercase tracking-wider">
                Identified Critical Concern:
              </p>
              {redFlags.map((flag, idx) => (
                <div key={idx} className="text-xs text-red-700 dark:text-red-300 font-medium flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-red-500" />
                  <span>{flag.category}: {flag.clinical_concern}</span>
                </div>
              ))}
            </div>
          )}

          <div className="mt-4 flex flex-wrap gap-3">
            <a
              href="tel:108"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-red-600 to-rose-700 hover:from-red-700 hover:to-rose-800 text-white text-sm font-semibold shadow-md shadow-red-600/20 transition-all hover:scale-105 active:scale-95"
            >
              <PhoneCall className="h-4 w-4" />
              <span>Call Emergency (108 / 112)</span>
            </a>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white/90 dark:bg-slate-900 border border-red-200 dark:border-red-900/60 text-red-800 dark:text-red-200 text-sm font-medium shadow-xs">
              <Hospital className="h-4 w-4 text-red-600" />
              <span>Go to Nearest Emergency Room</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
