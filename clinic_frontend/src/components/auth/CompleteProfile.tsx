import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Calendar,
  User,
  HeartPulse,
  Droplets,
  MapPin,
  AlertCircle,
  ArrowRight,
  ChevronDown,
  ShieldCheck,
  Stethoscope,
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { ButtonLoader } from '@/components/common/Loader';
import { toast } from '@/hooks/use-toast';
import { GENDERS, BLOOD_GROUPS } from '@/utils/constants';
import { patientService } from '@/services/patientService';

export const CompleteProfile = () => {
  const navigate = useNavigate();
  const { user, refreshUser, isAuthenticated, isLoading: authLoading } = useAuth();

  const [formData, setFormData] = useState({
    date_of_birth: '',
    gender: 'M',
    blood_group: '',
    address: '',
    emergency_contact: '',
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [ekgPath, setEkgPath] = useState('');

  const todayStr = new Date().toISOString().split('T')[0];

  // Redirect to login if user is not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      navigate('/login', { replace: true });
    }
  }, [isAuthenticated, authLoading, navigate]);

  // If patient already has profile details, prefill them
  useEffect(() => {
    if (isAuthenticated && user?.role === 'PATIENT') {
      patientService
        .getMyProfile()
        .then((profile) => {
          if (profile) {
            setFormData({
              date_of_birth: profile.date_of_birth || '',
              gender: profile.gender || 'M',
              blood_group: profile.blood_group || '',
              address: profile.address || '',
              emergency_contact: profile.emergency_contact || '',
            });
          }
        })
        .catch(() => {
          // If no profile exists yet, default empty form is fine
        });
    }
  }, [isAuthenticated, user]);

  // Dynamic EKG background path
  useEffect(() => {
    const patternWidth = 1000;
    const height = 200;
    const baseline = height / 2;

    const segments = [];
    let x = 0;

    while (x < patternWidth) {
      x += Math.random() * 30 + 20;
      if (x >= patternWidth) break;
      segments.push({ type: 'L', x, y: baseline });

      const spikeHeight = Math.random() * 100 + 30;
      segments.push({ type: 'L', x: x + 5, y: baseline - spikeHeight });
      segments.push({ type: 'L', x: x + 10, y: baseline + spikeHeight * 0.6 });
      segments.push({ type: 'L', x: x + 15, y: baseline });
      x += 20;
    }

    let path = `M 0 ${baseline}`;
    for (const seg of segments) {
      path += ` L ${seg.x} ${seg.y}`;
    }
    path += ` L ${patternWidth} ${baseline}`;

    for (const seg of segments) {
      path += ` L ${seg.x + patternWidth} ${seg.y}`;
    }
    path += ` L ${patternWidth * 2} ${baseline}`;

    setEkgPath(path);
  }, []);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.date_of_birth) {
      newErrors.date_of_birth = 'Date of birth is required';
    } else {
      const dob = new Date(formData.date_of_birth);
      const today = new Date();
      if (dob > today) {
        newErrors.date_of_birth = 'Date of birth cannot be in the future';
      }
    }

    if (!formData.gender) {
      newErrors.gender = 'Gender is required';
    }

    if (!formData.blood_group) {
      newErrors.blood_group = 'Blood group is required';
    }

    if (!formData.address.trim()) {
      newErrors.address = 'Residential address is required';
    } else if (formData.address.trim().length < 5) {
      newErrors.address = 'Address must be at least 5 characters';
    }

    if (!formData.emergency_contact.trim()) {
      newErrors.emergency_contact = 'Emergency contact is required';
    } else if (formData.emergency_contact.trim().length < 5) {
      newErrors.emergency_contact = 'Please provide contact name & phone number';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsSubmitting(true);
    try {
      await patientService.updateMyProfile({
        date_of_birth: formData.date_of_birth,
        gender: formData.gender,
        blood_group: formData.blood_group,
        address: formData.address,
        emergency_contact: formData.emergency_contact,
      });

      await refreshUser();

      toast({
        title: 'Profile Complete!',
        description: 'Your details have been saved. Welcome to Velora Care!',
      });

      navigate('/dashboard');
    } catch (error: any) {
      console.error('Failed to update profile:', error);
      const errorData = error.response?.data;
      let errorMsg = 'Failed to save profile details. Please try again.';

      if (errorData) {
        if (typeof errorData === 'string') {
          errorMsg = errorData;
        } else {
          const msgs = [];
          for (const [key, val] of Object.entries(errorData)) {
            const formattedKey =
              key === 'non_field_errors'
                ? 'Error'
                : key
                    .split('_')
                    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
                    .join(' ');

            if (Array.isArray(val) && val.length > 0) {
              msgs.push(`${formattedKey}: ${val[0]}`);
            } else if (typeof val === 'string') {
              msgs.push(`${formattedKey}: ${val}`);
            }
          }
          if (msgs.length > 0) errorMsg = msgs.join(' | ');
          else if (errorData.message) errorMsg = errorData.message;
        }
      }

      toast({
        variant: 'destructive',
        title: 'Save Failed',
        description: errorMsg,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-slate-50/50 dark:bg-background text-foreground flex items-center justify-center font-sans selection:bg-primary/20 selection:text-primary py-8 sm:py-12">
      {/* Background Mesh Layer */}
      <div className="absolute inset-0 z-0 bg-gradient-to-br from-background via-primary/5 to-background pointer-events-none" />

      {/* Background Glowing Blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute -top-[20%] -left-[10%] w-[800px] h-[800px] bg-primary/10 rounded-[100%] blur-[120px] mix-blend-multiply dark:mix-blend-screen opacity-70 animate-pulse-slow" />
        <div
          className="absolute -bottom-[20%] -right-[10%] w-[800px] h-[800px] bg-secondary/10 rounded-[100%] blur-[120px] mix-blend-multiply dark:mix-blend-screen opacity-70 animate-pulse-slow"
          style={{ animationDelay: '2s' }}
        />
        <div
          className="absolute top-[40%] left-[60%] w-[400px] h-[400px] bg-accent/10 rounded-[100%] blur-[80px] mix-blend-multiply dark:mix-blend-screen opacity-50 animate-pulse-slow"
          style={{ animationDelay: '4s' }}
        />

        {/* EKG Animation */}
        <div className="absolute inset-0 flex items-center justify-center opacity-[0.10] dark:opacity-[0.40]">
          <svg className="w-full h-64 overflow-visible" preserveAspectRatio="none" viewBox="0 0 1000 200">
            <defs>
              <linearGradient id="ekg-complete" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="transparent" />
                <stop offset="20%" stopColor="hsl(var(--primary))" />
                <stop offset="80%" stopColor="hsl(var(--primary))" />
                <stop offset="100%" stopColor="transparent" />
              </linearGradient>
            </defs>
            <path
              d={ekgPath || 'M0 100 L2000 100'}
              stroke="url(#ekg-complete)"
              strokeWidth="2"
              fill="none"
              className="animate-ekg-scroll"
            />
          </svg>
        </div>
      </div>

      <div className="relative z-10 w-full max-w-6xl grid lg:grid-cols-5 gap-8 lg:gap-12 p-4 sm:p-6 items-center">
        {/* Left Side - Branding */}
        <div className="hidden lg:flex lg:col-span-2 flex-col justify-center space-y-8 animate-fade-in pl-8">
          <div className="flex flex-col items-start justify-center">
            <div className="relative group -mb-2 -ml-2">
              <img src="/logo.png" alt="Velora Care Logo" className="h-28 w-auto object-contain drop-shadow-md" />
            </div>

            <div className="mt-2">
              <h1 className="text-4xl font-extrabold tracking-tight text-foreground mb-3 leading-tight">
                Complete Your{' '}
                <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                  Profile
                </span>{' '}
                <br />
                <span className="text-2xl font-normal text-muted-foreground">Personalized Care</span>
              </h1>
              <p className="text-muted-foreground text-lg max-w-sm mt-2 leading-relaxed font-medium">
                Please fill in your basic health details so our medical team can provide immediate and personalized care.
              </p>
            </div>

            <div className="space-y-4 pt-8 w-full">
              <div className="flex items-center gap-4 bg-card/60 backdrop-blur-sm border border-primary/10 rounded-xl p-4 transition-all hover:bg-card hover:shadow-md group cursor-default">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary group-hover:scale-110 transition-transform">
                  <Stethoscope className="h-6 w-6" />
                </div>
                <div className="text-left">
                  <p className="font-bold text-foreground">Accurate Consultations</p>
                  <p className="text-sm text-muted-foreground">Pre-filled health details for appointments</p>
                </div>
              </div>

              <div className="flex items-center gap-4 bg-card/60 backdrop-blur-sm border border-secondary/10 rounded-xl p-4 transition-all hover:bg-card hover:shadow-md group cursor-default">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-secondary/10 text-secondary group-hover:scale-110 transition-transform">
                  <ShieldCheck className="h-6 w-6" />
                </div>
                <div className="text-left">
                  <p className="font-bold text-foreground">Emergency Ready</p>
                  <p className="text-sm text-muted-foreground">Instant access to blood group & emergency contacts</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Side - Form */}
        <div className="lg:col-span-3 w-full max-w-xl mx-auto">
          <div className="relative backdrop-blur-xl bg-card border border-border/60 rounded-[2rem] shadow-2xl shadow-primary/5 p-5 sm:p-8 md:p-10 overflow-hidden ring-1 ring-black/5">
            <div className="mb-6 sm:mb-8 text-center lg:text-left">
              <h2 className="text-2xl font-bold text-foreground">Profile Details</h2>
              <p className="text-muted-foreground mt-1 text-sm bg-muted inline-block px-3 py-1 rounded-full border border-border">
                Fill up basic details to enter system
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Date of Birth */}
                <div className="space-y-1.5">
                  <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">
                    Date of Birth <span className="text-destructive">*</span>
                  </label>
                  <div className="relative group">
                    <Calendar className="absolute left-3 top-3.5 w-4 h-4 text-muted-foreground group-focus-within:text-primary transition-colors z-10 pointer-events-none" />
                    <input
                      type="date"
                      max={todayStr}
                      value={formData.date_of_birth}
                      onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
                      className="w-full bg-background border border-input rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 text-foreground placeholder-muted-foreground pl-10 pr-4 py-2.5 sm:py-3 outline-none text-sm font-medium transition-all shadow-sm"
                    />
                  </div>
                  {errors.date_of_birth && (
                    <p className="text-xs text-destructive font-medium ml-1">{errors.date_of_birth}</p>
                  )}
                </div>

                {/* Gender */}
                <div className="space-y-1.5">
                  <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">
                    Gender <span className="text-destructive">*</span>
                  </label>
                  <div className="relative">
                    <select
                      value={formData.gender}
                      onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                      className="w-full bg-background border border-input rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 text-foreground px-4 py-2.5 sm:py-3 outline-none text-sm font-medium transition-all shadow-sm appearance-none"
                    >
                      {GENDERS.map((g) => (
                        <option key={g.value} value={g.value}>
                          {g.label}
                        </option>
                      ))}
                    </select>
                    <ChevronDown className="absolute right-3 top-3.5 w-4 h-4 text-muted-foreground pointer-events-none" />
                  </div>
                  {errors.gender && <p className="text-xs text-destructive font-medium ml-1">{errors.gender}</p>}
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {/* Blood Group */}
                <div className="space-y-1.5">
                  <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">
                    Blood Group <span className="text-destructive">*</span>
                  </label>
                  <div className="relative">
                    <select
                      value={formData.blood_group}
                      onChange={(e) => setFormData({ ...formData, blood_group: e.target.value })}
                      className="w-full bg-background border border-input rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 text-foreground px-4 py-2.5 sm:py-3 outline-none text-sm font-medium transition-all shadow-sm appearance-none"
                    >
                      <option value="">Select blood group</option>
                      {BLOOD_GROUPS.map((bg) => (
                        <option key={bg} value={bg}>
                          {bg}
                        </option>
                      ))}
                    </select>
                    <ChevronDown className="absolute right-3 top-3.5 w-4 h-4 text-muted-foreground pointer-events-none" />
                  </div>
                  {errors.blood_group && (
                    <p className="text-xs text-destructive font-medium ml-1">{errors.blood_group}</p>
                  )}
                </div>

                {/* Emergency Contact */}
                <div className="space-y-1.5">
                  <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">
                    Emergency Contact <span className="text-destructive">*</span>
                  </label>
                  <div className="relative group">
                    <AlertCircle className="absolute left-3 top-3.5 w-4 h-4 text-muted-foreground group-focus-within:text-primary transition-colors z-10 pointer-events-none" />
                    <input
                      type="text"
                      value={formData.emergency_contact}
                      onChange={(e) => setFormData({ ...formData, emergency_contact: e.target.value })}
                      placeholder="e.g. Jane Doe (+1 555-0199)"
                      className="w-full bg-background border border-input rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 text-foreground placeholder-muted-foreground pl-10 pr-4 py-2.5 sm:py-3 outline-none text-sm font-medium transition-all shadow-sm"
                    />
                  </div>
                  {errors.emergency_contact && (
                    <p className="text-xs text-destructive font-medium ml-1">{errors.emergency_contact}</p>
                  )}
                </div>
              </div>

              {/* Residential Address */}
              <div className="space-y-1.5">
                <label className="text-xs font-bold uppercase tracking-wider text-muted-foreground ml-1">
                  Residential Address <span className="text-destructive">*</span>
                </label>
                <div className="relative group">
                  <MapPin className="absolute left-3 top-3.5 w-4 h-4 text-muted-foreground group-focus-within:text-primary transition-colors z-10 pointer-events-none" />
                  <input
                    type="text"
                    value={formData.address}
                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                    placeholder="Street Address, City, State"
                    className="w-full bg-background border border-input rounded-xl focus:border-primary focus:ring-2 focus:ring-primary/20 text-foreground placeholder-muted-foreground pl-10 pr-4 py-2.5 sm:py-3 outline-none text-sm font-medium transition-all shadow-sm"
                  />
                </div>
                {errors.address && <p className="text-xs text-destructive font-medium ml-1">{errors.address}</p>}
              </div>

              {/* Action Button: Save & Enter System */}
              <div className="pt-3">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full relative overflow-hidden rounded-xl bg-gradient-to-r from-primary to-secondary p-[1px] shadow-lg shadow-primary/30 transition-all hover:scale-[1.01] hover:shadow-primary/40 group"
                >
                  <div className="relative h-full w-full bg-gradient-to-r from-primary to-secondary px-4 py-2.5 sm:py-3.5 transition-all">
                    <div className="flex items-center justify-center gap-2">
                      {isSubmitting ? (
                        <ButtonLoader className="text-white" />
                      ) : (
                        <>
                          <span className="font-bold text-white tracking-wide text-sm sm:text-base">
                            Save Profile & Enter System
                          </span>
                          <ArrowRight className="w-4 h-4 text-white group-hover:translate-x-1 transition-transform" />
                        </>
                      )}
                    </div>
                  </div>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes ekg-scroll {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }
        .animate-ekg-scroll {
            animation: ekg-scroll 20s linear infinite;
        }
      `}</style>
    </div>
  );
};
