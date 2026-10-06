import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Stethoscope, CalendarPlus, ArrowRight } from 'lucide-react';

export const DoctorReviewBanner: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="rounded-2xl border border-[#D9E2F0] dark:border-slate-800 bg-gradient-to-r from-[#EFF6FF] via-[#F0F7FF] to-[#FAF5FF] dark:from-slate-900/90 dark:to-blue-950/40 p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-xs">
      <div className="flex items-center gap-3">
        <div className="p-2.5 rounded-xl bg-[#E0F2FE] dark:bg-sky-950/60 text-[#2563EB] dark:text-[#38BDF8]">
          <Stethoscope className="h-5 w-5" />
        </div>
        <div>
          <h4 className="font-bold text-sm text-[#1E3A8A] dark:text-white">
            Doctor Consultation Recommended
          </h4>
          <p className="text-xs text-[#64748B] dark:text-slate-300">
            Medication appropriateness and dosage require clinical assessment by a licensed physician.
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={() => navigate('/appointments/new')}
          className="aurora-btn-gradient inline-flex items-center gap-1.5 px-4 py-2 text-xs font-semibold rounded-xl shadow-md transition-all active:scale-95"
        >
          <CalendarPlus className="h-4 w-4" />
          <span>Book Appointment</span>
          <ArrowRight className="h-3 w-3" />
        </button>
      </div>
    </div>
  );
};
