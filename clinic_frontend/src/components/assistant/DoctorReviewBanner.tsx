import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Stethoscope, CalendarPlus, ArrowRight } from 'lucide-react';

export const DoctorReviewBanner: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="rounded-2xl border border-primary/20 bg-primary/5 p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="p-2.5 rounded-xl bg-primary/10 text-primary">
          <Stethoscope className="h-5 w-5" />
        </div>
        <div>
          <h4 className="font-semibold text-sm text-foreground">
            Doctor Consultation Recommended
          </h4>
          <p className="text-xs text-muted-foreground">
            Medication appropriateness and dosage require clinical assessment by a licensed physician.
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={() => navigate('/appointments/new')}
          className="btn-gradient inline-flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-semibold rounded-xl shadow-md"
        >
          <CalendarPlus className="h-4 w-4" />
          <span>Book Appointment</span>
          <ArrowRight className="h-3 w-3" />
        </button>
      </div>
    </div>
  );
};
