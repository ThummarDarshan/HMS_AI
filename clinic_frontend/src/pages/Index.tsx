import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ArrowRight,
  ShieldCheck,
  Clock,
  Users,
  Calendar,
  ChevronDown,
  Stethoscope,
  HeartPulse,
  Phone,
  Sparkles,
  BedDouble,
  FlaskConical,
  CreditCard,
  AlertTriangle,
  CheckCircle2,
  Lock,
  ExternalLink,
  ChevronRight,
  Zap,
  Building2,
  Heart,
} from 'lucide-react';

export default function Index() {
  const [activeTab, setActiveTab] = useState<'ai' | 'appointments' | 'beds' | 'labs' | 'billing'>('ai');
  const [activeFaq, setActiveFaq] = useState<number | null>(0);
  const [ekgPath, setEkgPath] = useState('');

  // Generate dynamic medical EKG heartbeat path
  useEffect(() => {
    const patternWidth = 1000;
    const height = 140;
    const baseline = height / 2;

    const segments = [];
    let x = 0;

    while (x < patternWidth) {
      x += Math.random() * 25 + 20;
      if (x >= patternWidth) break;
      segments.push({ type: 'L', x, y: baseline });

      const spikeHeight = Math.random() * 60 + 25;
      segments.push({ type: 'L', x: x + 4, y: baseline - spikeHeight });
      segments.push({ type: 'L', x: x + 8, y: baseline + spikeHeight * 0.5 });
      segments.push({ type: 'L', x: x + 12, y: baseline });
      x += 16;
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

  const stats = [
    { value: "12,500+", label: "Patients Treated", icon: Users, sub: "Across all clinical wings" },
    { value: "65+", label: "Senior Specialists", icon: Stethoscope, sub: "Board-certified doctors" },
    { value: "< 15 min", label: "ER Triage Response", icon: Clock, sub: "24/7 Rapid Emergency Care" },
    { value: "99.8%", label: "Clinical Precision", icon: ShieldCheck, sub: "CDSCO & DailyMed Grounded" },
  ];

  const ecosystemModules = [
    {
      id: 'ai' as const,
      label: 'AI Health Assistant',
      icon: Sparkles,
      tag: 'Grounded Clinical RAG',
      title: 'Conversational Triage & Drug Monograph Intelligence',
      description: 'Evaluates patient concerns across 13 core healthcare conversation capabilities, performs automated lab report interpretation, checks allergy cross-reactivity, and grounds advice in official CDSCO and DailyMed regulatory documentation.',
      bullets: [
        'Non-repetitive clinical intake (duration, severity 1-10, temperature)',
        'Automated Lab Report parsing for CBC, Hb, Glucose, Creatinine, & LFTs',
        'Deterministic allergy checking (e.g. Penicillin vs Amoxicillin conflicts)',
        'Immediate emergency red-flag interception with 108 / 112 routing',
      ],
      linkText: 'Launch AI Assistant in New Tab',
      linkUrl: '/ai-assistant',
      isExternal: true,
    },
    {
      id: 'appointments' as const,
      label: 'Smart Appointments',
      icon: Calendar,
      tag: 'Real-Time Scheduling',
      title: 'Instant Booking with Top Hospital Specialists',
      description: 'Patients can seamlessly browse doctors by department, view real-time available time slots, book in-person or telemedicine consultations, and receive automated confirmations with zero wait time.',
      bullets: [
        'Live calendar slot allocation with zero double-booking',
        'Department-based routing across Cardiology, Neurology, Pediatrics, etc.',
        'Automatic patient history linkage to scheduled appointments',
        'Instant cancellation and rescheduling controls',
      ],
      linkText: 'Book an Appointment',
      linkUrl: '/appointments',
      isExternal: false,
    },
    {
      id: 'beds' as const,
      label: 'Smart Bed Tracking',
      icon: BedDouble,
      tag: 'Inpatient Operations',
      title: 'Real-Time Ward & ICU Occupancy Dashboard',
      description: 'Hospital administrators and nursing staff maintain instantaneous visibility into bed occupancy across ICU, General Ward, Emergency, and Pediatric units, accelerating admission and discharge workflows.',
      bullets: [
        'Floor-by-floor visual bed status matrix (Available, Occupied, Cleaning)',
        'Direct patient admission and discharge tracking',
        'Critical care ICU bed priority management',
        'Daily occupancy rate telemetry and automated alerts',
      ],
      linkText: 'View Bed Dashboard',
      linkUrl: '/beds',
      isExternal: false,
    },
    {
      id: 'labs' as const,
      label: 'LIMS & Laboratory',
      icon: FlaskConical,
      tag: 'Diagnostics & Reports',
      title: 'End-to-End Diagnostic Pathology Management',
      description: 'Doctors order diagnostic tests directly from the consultation interface. Laboratory technicians enter verified results which are automatically checked against standard reference ranges and flagged for physician review.',
      bullets: [
        'Complete test catalog: Hematology, Biochemistry, Renal, Liver, Thyroid',
        'Automated HIGH/LOW abnormal value highlighting',
        'One-click professional PDF Medical Report generation',
        'Patient portal access to downloadable diagnostic reports',
      ],
      linkText: 'Explore Lab Requests',
      linkUrl: '/lab-requests',
      isExternal: false,
    },
    {
      id: 'billing' as const,
      label: 'Billing & Invoicing',
      icon: CreditCard,
      tag: 'Financial Operations',
      title: 'Transparent Inpatient & Outpatient Invoicing',
      description: 'Streamlined invoicing, automated cost calculations for consultations, bed stay, procedures, and laboratory diagnostics, complete with printable hospital invoices and transparent status tracking.',
      bullets: [
        'Itemized billing for consultations, bed occupancy, and diagnostic tests',
        'Multi-status tracking: Pending, Paid, Partially Paid, and Cancelled',
        'Official hospital branded printable invoice generator',
        'Financial audit trail compliant with medical accounting standards',
      ],
      linkText: 'Billing Portal',
      linkUrl: '/billing',
      isExternal: false,
    },
  ];

  const departments = [
    {
      name: "Cardiology & Vascular Center",
      description: "Comprehensive cardiac catheterization lab, acute angina triage, and 24/7 heart attack care.",
      image: "/departments/cardiology.png",
      badge: "24/7 Cath Lab Ready",
      doctors: "12 Specialists",
    },
    {
      name: "Neurology & Neurosurgery",
      description: "Advanced brain and spine diagnostics, acute stroke FAST intervention, and neuro-ICU care.",
      image: "/departments/neurology.png",
      badge: "Stroke Emergency Unit",
      doctors: "9 Specialists",
    },
    {
      name: "Pediatrics & Neonatology",
      description: "Dedicated NICU, compassionate child development, and verified pediatric safe medication dosing.",
      image: "/departments/pediatrics.png",
      badge: "Level 3 NICU",
      doctors: "8 Specialists",
    },
    {
      name: "Orthopedics & Joint Care",
      description: "Minimally invasive joint replacements, arthroscopic sports surgery, and rapid trauma rehab.",
      image: "/departments/orthopedics.png",
      badge: "Robotic Surgery",
      doctors: "10 Specialists",
    },
  ];

  const workflowSteps = [
    {
      step: "01",
      title: "Intelligent Triage & Intake",
      desc: "Patients start with our Clinical AI Assistant or select a specialist directly. Symptoms are gathered in a structured, non-repetitive way.",
      icon: Sparkles,
    },
    {
      step: "02",
      title: "Seamless Doctor Consultation",
      desc: "Doctors access unified electronic medical records, previous diagnoses, active prescriptions, and documented allergies in one view.",
      icon: Stethoscope,
    },
    {
      step: "03",
      title: "Integrated Diagnostics & Beds",
      desc: "Physicians order lab investigations and assign ward or ICU beds with instant automated status updates across all departments.",
      icon: FlaskConical,
    },
    {
      step: "04",
      title: "Transparent Recovery & Billing",
      desc: "Patients receive verified medication monographs, follow-up notifications, and itemized transparent hospital invoices.",
      icon: CheckCircle2,
    },
  ];

  const faqs = [
    {
      q: "How does the AI Clinical Health Assistant assist patients before seeing a doctor?",
      a: "The assistant conducts an empathetic, non-repetitive intake regarding your symptoms, asks missing details (such as duration, temperature, or pain severity), checks your profile allergies against drug classes, interprets laboratory reports against normal ranges, and provides evidence-backed medication guidance from official CDSCO and DailyMed monographs. If any critical red-flags are detected, it directs you immediately to 108 / 112 emergency care."
    },
    {
      q: "Can I book appointments with specific medical specialists online?",
      a: "Yes. Patients can browse verified doctors by specialty (Cardiology, Neurology, Pediatrics, Orthopedics, etc.), inspect real-time available time slots, and confirm appointments instantly through the Patient Portal."
    },
    {
      q: "How are laboratory reports and diagnostic test results accessed?",
      a: "Once diagnostic samples are processed by our laboratory technicians, the verified report is uploaded directly to your patient health record. You can view structured values flagged against standard reference ranges and download official print-ready PDF reports."
    },
    {
      q: "Is patient medical data safe and confidential?",
      a: "Velora Care enforces enterprise-grade security protocols, including 256-bit AES/TLS encryption, role-based access control, and complete compliance with healthcare privacy standards. Only authorized medical staff have access to your clinical records."
    },
    {
      q: "What should I do in case of a life-threatening medical emergency?",
      a: "For acute emergencies (such as crushing chest pain, difficulty breathing, stroke symptoms, or severe bleeding), call the emergency helpline at 108 / 112 or visit our 24/7 Level 1 Trauma Center immediately. Our AI Assistant also features a deterministic safety layer that automatically halts non-urgent flows and displays emergency guidance."
    },
  ];

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-[#F8FAFD] dark:bg-[#0A0F1D] text-[#1E293B] dark:text-[#F8FAFC] font-sans selection:bg-[#2563EB]/20 selection:text-[#2563EB]">
      {/* Dynamic Ambient Medical Aurora Background Mesh */}
      <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
        <div className="absolute -top-[25%] -left-[15%] w-[850px] h-[850px] bg-gradient-to-tr from-[#E0F2FE] via-[#EDE9FE] to-transparent rounded-full blur-[140px] opacity-75 dark:opacity-20 animate-pulse-glow" />
        <div className="absolute top-[35%] -right-[15%] w-[750px] h-[750px] bg-gradient-to-bl from-[#E0F7FA] via-[#E0F2FE] to-transparent rounded-full blur-[140px] opacity-70 dark:opacity-20 animate-pulse-glow" style={{ animationDelay: '2.5s' }} />
        <div className="absolute -bottom-[20%] left-[20%] w-[900px] h-[900px] bg-gradient-to-tr from-[#EDE9FE] via-[#E0F2FE] to-transparent rounded-full blur-[150px] opacity-65 dark:opacity-15 animate-pulse-glow" style={{ animationDelay: '4s' }} />

        {/* Ambient Continuous EKG Waveform Line */}
        <div className="absolute top-[32%] left-0 right-0 flex items-center justify-center opacity-[0.07] dark:opacity-[0.16] pointer-events-none">
          <svg className="w-[180%] sm:w-full h-36 overflow-visible" preserveAspectRatio="none" viewBox="0 0 1000 140">
            <defs>
              <linearGradient id="ekg-aurora" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="transparent" />
                <stop offset="25%" stopColor="#2563EB" />
                <stop offset="75%" stopColor="#38BDF8" />
                <stop offset="100%" stopColor="transparent" />
              </linearGradient>
            </defs>
            <path
              d={ekgPath || "M0 70 L2000 70"}
              stroke="url(#ekg-aurora)"
              strokeWidth="2"
              fill="none"
              className="animate-ekg-scroll"
            />
          </svg>
        </div>
      </div>

      {/* TOP EMERGENCY DISPATCH RIBBON */}
      <div className="relative z-50 bg-[#1E3A8A] text-white text-xs font-semibold px-4 py-2 text-center flex items-center justify-between max-w-full overflow-hidden border-b border-blue-900/40">
        <div className="max-w-7xl mx-auto w-full flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping inline-block" />
            <span className="text-blue-100 font-medium">Level 1 Trauma & 24/7 ER Ready</span>
            <span className="hidden sm:inline text-blue-300">•</span>
            <span className="hidden sm:inline text-blue-200">Rapid Response GPS Ambulance On-Duty</span>
          </div>
          <div className="flex items-center gap-4 text-[11px] sm:text-xs">
            <a href="tel:108" className="text-white hover:text-sky-200 font-bold flex items-center gap-1">
              <Phone className="h-3 w-3 text-rose-400 animate-bounce" /> Emergency: <span className="underline">108 / 112</span>
            </a>
            <span className="hidden md:inline text-blue-300">|</span>
            <span className="hidden md:inline text-blue-200">Toll-Free: 1-800-VELORA-CARE</span>
          </div>
        </div>
      </div>

      {/* MAIN CLEAN FLOATING NAVIGATION BAR */}
      <motion.nav
        initial={{ y: -40, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="sticky top-0 z-40 px-4 sm:px-8 py-3.5 backdrop-blur-xl bg-white/85 dark:bg-[#0A0F1D]/85 border-b border-[#D9E2F0]/80 dark:border-slate-800 shadow-xs"
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Brand Identity */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-[#2563EB] to-[#1E3A8A] flex items-center justify-center text-white shadow-md shadow-[#2563EB]/25 group-hover:scale-105 transition-transform">
              <HeartPulse className="h-5 w-5 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-[#1E3A8A] via-[#2563EB] to-[#0284C7] dark:from-white dark:to-sky-300 bg-clip-text text-transparent">
                Velora Care
              </span>
              <span className="text-[10px] font-semibold text-[#64748B] dark:text-slate-400 tracking-wider uppercase">
                Hospital Management OS
              </span>
            </div>
          </Link>

          {/* Clean Spaced Navigation Links */}
          <div className="hidden lg:flex items-center gap-8 text-sm font-semibold text-[#475569] dark:text-slate-300">
            <a href="#about" className="hover:text-[#2563EB] dark:hover:text-sky-400 transition-colors">About</a>
            <a href="#specialties" className="hover:text-[#2563EB] dark:hover:text-sky-400 transition-colors">Specialties</a>
            <a href="#ecosystem" className="hover:text-[#2563EB] dark:hover:text-sky-400 transition-colors">Ecosystem</a>
            <a href="#workflow" className="hover:text-[#2563EB] dark:hover:text-sky-400 transition-colors">Workflow</a>
            <a href="#faq" className="hover:text-[#2563EB] dark:hover:text-sky-400 transition-colors">FAQ</a>
          </div>

          {/* Action Button Group */}
          <div className="flex items-center gap-3">
            {/* AI Assistant Direct Launch Button */}
            <a
              href="/ai-assistant"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-bold bg-blue-50 dark:bg-blue-950/60 text-[#2563EB] dark:text-sky-300 border border-[#BAE6FD] dark:border-blue-800 hover:border-[#2563EB] transition-all hover:scale-105 shadow-2xs"
            >
              <Sparkles className="h-4 w-4 text-[#2563EB] animate-pulse" />
              <span className="hidden sm:inline">AI Health Assistant</span>
              <span className="sm:hidden">AI Bot</span>
              <ExternalLink className="h-3 w-3 text-[#2563EB]/70" />
            </a>

            {/* Staff Login */}
            <Link
              to="/login"
              className="hidden sm:inline-flex text-xs sm:text-sm font-bold text-[#334155] dark:text-slate-200 hover:text-[#2563EB] px-3.5 py-2 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-[#2563EB]/40 bg-white/60 dark:bg-slate-900/60 transition-all"
            >
              Staff Login
            </Link>

            {/* Patient Portal CTA */}
            <Link
              to="/register"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs sm:text-sm font-bold text-white bg-gradient-to-r from-[#2563EB] to-[#1E3A8A] hover:from-[#1D4ED8] hover:to-[#172554] shadow-md shadow-[#2563EB]/25 hover:shadow-lg transition-all hover:scale-105"
            >
              <span>Patient Portal</span>
              <ArrowRight className="h-4 w-4 hidden sm:inline" />
            </Link>
          </div>
        </div>
      </motion.nav>

      {/* MAIN CONTENT AREA */}
      <main className="relative z-10 w-full">
        {/* =========================================================================
            1. HERO SECTION WITH POLISHED INTEGRATED CONSOLE
        ========================================================================= */}
        <section className="relative px-4 sm:px-8 py-12 lg:py-20 max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-12 gap-10 lg:gap-8 items-center">
            {/* Left Column: Hero Content */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="lg:col-span-7 space-y-6 text-center lg:text-left"
            >
              {/* Feature Pill */}
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 dark:bg-blue-950/60 border border-[#BAE6FD] dark:border-blue-900 text-[#1E40AF] dark:text-sky-300 text-xs sm:text-sm font-semibold shadow-2xs">
                <Sparkles className="w-4 h-4 text-[#2563EB] shrink-0" />
                <span>Next-Gen Healthcare Management & Clinical AI</span>
              </div>

              {/* Main Headline */}
              <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight text-[#0F172A] dark:text-white leading-[1.14]">
                Intelligent Medical Care <br className="hidden sm:inline" />
                <span className="bg-gradient-to-r from-[#2563EB] via-[#0284C7] to-[#1E3A8A] dark:from-[#60A5FA] dark:via-[#38BDF8] dark:to-white bg-clip-text text-transparent">
                  Powered by Clinical AI
                </span>
              </h1>

              {/* Narrative Subtitle */}
              <p className="text-base sm:text-lg text-[#475569] dark:text-slate-300 max-w-xl leading-relaxed mx-auto lg:mx-0 font-normal">
                Velora Care unites smart appointments, electronic health records, smart bed management, pathology lab tracking, and an authoritative <strong>13-pillar Clinical AI Assistant</strong> grounded in official CDSCO and DailyMed regulatory monographs.
              </p>

              {/* Call-to-Action Group */}
              <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-3.5 pt-2">
                <a
                  href="/ai-assistant"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-3.5 rounded-2xl font-bold text-white bg-gradient-to-r from-[#2563EB] to-[#1E3A8A] shadow-lg shadow-[#2563EB]/25 hover:shadow-xl hover:scale-[1.02] transition-all group"
                >
                  <Sparkles className="h-5 w-5 text-sky-200 animate-pulse" />
                  <span>Launch AI Health Assistant</span>
                  <ExternalLink className="h-4 w-4 opacity-80 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                </a>

                <Link
                  to="/appointments"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl font-bold text-[#1E3A8A] dark:text-white bg-white dark:bg-slate-900 border border-[#D9E2F0] dark:border-slate-700 shadow-xs hover:bg-slate-50 dark:hover:bg-slate-800 transition-all hover:scale-[1.02]"
                >
                  <Calendar className="h-5 w-5 text-[#2563EB]" />
                  <span>Book Consultation</span>
                </Link>
              </div>

              {/* Regulatory & Safety Badges */}
              <div className="pt-3 flex flex-wrap items-center justify-center lg:justify-start gap-4 text-xs font-semibold text-[#64748B] dark:text-slate-400">
                <div className="flex items-center gap-1.5">
                  <ShieldCheck className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
                  <span>CDSCO & DailyMed Verified</span>
                </div>
                <span>•</span>
                <div className="flex items-center gap-1.5">
                  <Lock className="h-4 w-4 text-[#2563EB] dark:text-sky-400" />
                  <span>256-Bit Encrypted EHR</span>
                </div>
                <span>•</span>
                <div className="flex items-center gap-1.5">
                  <Heart className="h-4 w-4 text-rose-500" />
                  <span>Doctor Review Mandatory</span>
                </div>
              </div>
            </motion.div>

            {/* Right Column: Clean Self-Contained Clinical Console */}
            <motion.div
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.7, delay: 0.15 }}
              className="lg:col-span-5"
            >
              <div className="aurora-card rounded-3xl p-6 sm:p-7 space-y-4 border border-[#BAE6FD] dark:border-blue-900 shadow-xl bg-white/95 dark:bg-slate-900/95">
                {/* Console Header Bar */}
                <div className="flex items-center justify-between pb-3.5 border-b border-[#D9E2F0]/80 dark:border-slate-800">
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping inline-block" />
                    <span className="text-xs font-bold text-[#1E3A8A] dark:text-white uppercase tracking-wider">
                      Live Hospital Telemetry
                    </span>
                  </div>
                  <span className="text-[10px] font-mono text-[#0284C7] dark:text-sky-400 bg-sky-50 dark:bg-sky-950/60 px-2.5 py-0.5 rounded-full border border-sky-200 dark:border-sky-800 font-bold">
                    ACTIVE: 24/7
                  </span>
                </div>

                {/* Bed Availability Gauge */}
                <div className="p-3.5 rounded-2xl bg-gradient-to-r from-blue-50/70 to-indigo-50/70 dark:from-slate-800/80 dark:to-slate-900/80 border border-blue-100 dark:border-slate-700 space-y-2">
                  <div className="flex items-center justify-between text-xs font-semibold">
                    <span className="text-[#334155] dark:text-slate-300 flex items-center gap-1.5">
                      <BedDouble className="h-4 w-4 text-[#2563EB]" />
                      Smart Bed Availability
                    </span>
                    <span className="font-bold text-[#1E3A8A] dark:text-sky-300">18 Beds Open</span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full overflow-hidden">
                    <div className="bg-gradient-to-r from-[#2563EB] to-emerald-500 h-full rounded-full" style={{ width: '88%' }} />
                  </div>
                  <div className="flex justify-between text-[10px] text-[#64748B] dark:text-slate-400 font-medium">
                    <span>142 Inpatients Admitted</span>
                    <span>ICU / CCU / ER Priority</span>
                  </div>
                </div>

                {/* AI Assistant Live Case Snippet */}
                <div className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-[#BAE6FD] dark:border-slate-700 shadow-2xs space-y-2.5">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-[#0F172A] dark:text-white">
                      <Sparkles className="h-3.5 w-3.5 text-[#2563EB]" />
                      AI Health Assistant • Live Case
                    </div>
                    <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-2 py-0.5 rounded-full">
                      Triage Active
                    </span>
                  </div>

                  <div className="space-y-2 text-xs">
                    <div className="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800 text-[#1E293B] dark:text-slate-200">
                      <strong className="text-[#2563EB] dark:text-sky-400">Patient:</strong> "Fever (101°F) and cough for 2 days."
                    </div>
                    <div className="p-2.5 rounded-xl bg-blue-50/80 dark:bg-blue-950/50 border border-blue-100 dark:border-blue-900 text-[#1E3A8A] dark:text-slate-200 space-y-1">
                      <div className="font-bold flex items-center gap-1 text-[11px] text-[#2563EB]">
                        <Stethoscope className="h-3.5 w-3.5" /> Differentials: Viral URI / Acute Bronchitis
                      </div>
                      <p className="text-[11px] leading-relaxed text-[#334155] dark:text-slate-300">
                        First-Line: Paracetamol 500 mg. Proof: CDSCO / DailyMed regulatory monographs verified.
                      </p>
                    </div>
                  </div>

                  <a
                    href="/ai-assistant"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full flex items-center justify-center gap-1.5 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-[#2563EB] to-[#1E3A8A] hover:brightness-110 transition-all shadow-sm"
                  >
                    <span>Open Live AI Consultation</span>
                    <ExternalLink className="h-3 w-3" />
                  </a>
                </div>

                {/* Telemetry Footer Status Badges */}
                <div className="grid grid-cols-2 gap-2 pt-1 text-[11px]">
                  <div className="p-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-100 dark:border-slate-700 flex items-center gap-1.5 font-medium text-[#334155] dark:text-slate-300">
                    <FlaskConical className="h-3.5 w-3.5 text-[#0284C7]" />
                    <span>Auto Lab Range Flags</span>
                  </div>
                  <div className="p-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-100 dark:border-slate-700 flex items-center gap-1.5 font-medium text-[#334155] dark:text-slate-300">
                    <ShieldCheck className="h-3.5 w-3.5 text-emerald-500" />
                    <span>Allergy Conflict Shield</span>
                  </div>
                </div>

                {/* Doctor On-Duty Roster Link */}
                <div className="flex items-center justify-between text-xs pt-1 text-[#64748B] dark:text-slate-400 border-t border-slate-100 dark:border-slate-800">
                  <span className="flex items-center gap-1.5 font-medium">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500" />
                    50+ Specialists Active Today
                  </span>
                  <Link to="/doctors" className="font-bold text-[#2563EB] dark:text-sky-400 hover:underline">
                    View Roster →
                  </Link>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* =========================================================================
            2. REAL-TIME HOSPITAL TELEMETRY RIBBON
        ========================================================================= */}
        <section className="py-12 border-y border-[#D9E2F0]/80 dark:border-slate-800 bg-white/70 dark:bg-slate-900/60 backdrop-blur-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-8">
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
              {stats.map((stat, idx) => {
                const Icon = stat.icon;
                return (
                  <div
                    key={idx}
                    className="p-5 rounded-2xl bg-white dark:bg-slate-800/80 border border-slate-100 dark:border-slate-800 shadow-2xs space-y-1.5"
                  >
                    <div className="flex items-center justify-between">
                      <div className="w-9 h-9 rounded-xl bg-blue-50 dark:bg-blue-950/60 flex items-center justify-center text-[#2563EB] dark:text-sky-300">
                        <Icon className="h-5 w-5" />
                      </div>
                      <span className="w-2 h-2 rounded-full bg-emerald-500" />
                    </div>
                    <h3 className="text-3xl sm:text-4xl font-black text-[#0F172A] dark:text-white tracking-tight pt-1">
                      {stat.value}
                    </h3>
                    <p className="text-sm font-bold text-[#1E3A8A] dark:text-sky-300">{stat.label}</p>
                    <p className="text-xs text-[#64748B] dark:text-slate-400">{stat.sub}</p>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* =========================================================================
            3. INTERACTIVE ECOSYSTEM EXPLORER (5 CORE MODULES)
        ========================================================================= */}
        <section id="ecosystem" className="py-20 px-4 sm:px-8 max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-12 space-y-3">
            <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-blue-50 dark:bg-blue-950/60 text-[#2563EB] dark:text-sky-300 border border-blue-200 dark:border-blue-900 text-xs font-bold uppercase tracking-wider">
              <Zap className="h-3.5 w-3.5" />
              Unified Healthcare Architecture
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-[#0F172A] dark:text-white tracking-tight">
              Explore the <span className="text-[#2563EB] dark:text-sky-400">Velora Care Ecosystem</span>
            </h2>
            <p className="text-base text-[#64748B] dark:text-slate-300 leading-relaxed">
              Every hospital module operates in real-time synergy, from outpatient triage to inpatient ward discharge.
            </p>
          </div>

          {/* Module Selector Navigation Tabs */}
          <div className="flex items-center justify-start sm:justify-center gap-2 sm:gap-3 overflow-x-auto pb-4 no-scrollbar mb-8">
            {ecosystemModules.map((mod) => {
              const Icon = mod.icon;
              const isActive = activeTab === mod.id;
              return (
                <button
                  key={mod.id}
                  onClick={() => setActiveTab(mod.id)}
                  className={`flex items-center gap-2 px-4 sm:px-5 py-2.5 rounded-2xl text-xs sm:text-sm font-bold whitespace-nowrap transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-[#2563EB] to-[#1E3A8A] text-white shadow-md shadow-[#2563EB]/25 scale-105'
                      : 'bg-white dark:bg-slate-900 border border-[#D9E2F0] dark:border-slate-800 text-[#475569] dark:text-slate-300 hover:border-[#2563EB]/50'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{mod.label}</span>
                </button>
              );
            })}
          </div>

          {/* Tab Content Display Card */}
          <AnimatePresence mode="wait">
            {ecosystemModules
              .filter((m) => m.id === activeTab)
              .map((m) => (
                <motion.div
                  key={m.id}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -12 }}
                  transition={{ duration: 0.3 }}
                  className="aurora-card rounded-3xl p-6 sm:p-10 border border-[#BAE6FD] dark:border-blue-900 shadow-lg bg-white/95 dark:bg-slate-900/95"
                >
                  <div className="grid lg:grid-cols-12 gap-8 items-center">
                    <div className="lg:col-span-7 space-y-4">
                      <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-950/60 text-[#2563EB] dark:text-sky-300 text-xs font-bold border border-blue-200 dark:border-blue-900">
                        {m.tag}
                      </div>
                      <h3 className="text-2xl sm:text-3xl font-extrabold text-[#0F172A] dark:text-white tracking-tight">
                        {m.title}
                      </h3>
                      <p className="text-sm sm:text-base text-[#475569] dark:text-slate-300 leading-relaxed">
                        {m.description}
                      </p>

                      <div className="space-y-2 pt-2">
                        {m.bullets.map((b, i) => (
                          <div key={i} className="flex items-start gap-2.5 text-xs sm:text-sm text-[#334155] dark:text-slate-200 font-medium">
                            <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0 mt-0.5" />
                            <span>{b}</span>
                          </div>
                        ))}
                      </div>

                      <div className="pt-3">
                        {m.isExternal ? (
                          <a
                            href={m.linkUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-2 px-5 py-3 rounded-xl font-bold text-white bg-gradient-to-r from-[#2563EB] to-[#1E3A8A] hover:shadow-md transition-all hover:scale-105 text-sm"
                          >
                            <Sparkles className="h-4 w-4" />
                            <span>{m.linkText}</span>
                            <ExternalLink className="h-4 w-4" />
                          </a>
                        ) : (
                          <Link
                            to={m.linkUrl}
                            className="inline-flex items-center gap-2 px-5 py-3 rounded-xl font-bold text-white bg-gradient-to-r from-[#2563EB] to-[#1E3A8A] hover:shadow-md transition-all hover:scale-105 text-sm"
                          >
                            <span>{m.linkText}</span>
                            <ArrowRight className="h-4 w-4" />
                          </Link>
                        )}
                      </div>
                    </div>

                    <div className="lg:col-span-5 flex justify-center">
                      <div className="w-full max-w-md p-5 rounded-3xl bg-slate-50 dark:bg-slate-800/80 border border-[#D9E2F0] dark:border-slate-700 shadow-inner space-y-3.5">
                        <div className="flex items-center justify-between pb-2.5 border-b border-slate-200 dark:border-slate-700">
                          <span className="text-xs font-bold text-[#1E3A8A] dark:text-sky-300 uppercase">
                            Clinical Specifications
                          </span>
                          <span className="w-2.5 h-2.5 rounded-full bg-[#2563EB]" />
                        </div>
                        <div className="space-y-2.5 text-xs">
                          <div className="p-3 rounded-xl bg-white dark:bg-slate-800 shadow-2xs space-y-1 border border-slate-100 dark:border-slate-700">
                            <span className="font-semibold text-slate-500 dark:text-slate-400">Regulatory Framework:</span>
                            <p className="font-bold text-[#0F172A] dark:text-white">CDSCO (Govt of India) + DailyMed (FDA)</p>
                          </div>
                          <div className="p-3 rounded-xl bg-white dark:bg-slate-800 shadow-2xs space-y-1 border border-slate-100 dark:border-slate-700">
                            <span className="font-semibold text-slate-500 dark:text-slate-400">Security Standard:</span>
                            <p className="font-bold text-[#0F172A] dark:text-white">HIPAA Compliant • 256-Bit TLS</p>
                          </div>
                          <div className="p-3 rounded-xl bg-white dark:bg-slate-800 shadow-2xs space-y-1 border border-slate-100 dark:border-slate-700">
                            <span className="font-semibold text-slate-500 dark:text-slate-400">Interoperability:</span>
                            <p className="font-bold text-[#0F172A] dark:text-white">Integrated EHR, LIMS & Inpatient Billing</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
          </AnimatePresence>
        </section>

        {/* =========================================================================
            4. CENTERS OF EXCELLENCE & SPECIALIZED DEPARTMENTS
        ========================================================================= */}
        <section id="specialties" className="py-20 px-4 sm:px-8 max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-14 space-y-3">
            <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-blue-50 dark:bg-blue-950/60 text-[#2563EB] dark:text-sky-300 border border-blue-200 dark:border-blue-900 text-xs font-bold uppercase tracking-wider">
              <Building2 className="h-3.5 w-3.5" />
              Specialties
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-[#0F172A] dark:text-white tracking-tight">
              World-Class <span className="text-[#2563EB] dark:text-sky-400">Medical Centers</span>
            </h2>
            <p className="text-base text-[#64748B] dark:text-slate-300 leading-relaxed">
              Equipped with modern surgical suites, advanced telemetry, and top clinicians.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {departments.map((dept, idx) => (
              <div
                key={idx}
                className="group relative overflow-hidden rounded-3xl border border-[#D9E2F0] dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs hover:shadow-xl hover:border-[#BAE6FD] dark:hover:border-sky-900 transition-all flex flex-col h-full"
              >
                <div className="aspect-[16/11] overflow-hidden relative">
                  <img
                    src={dept.image}
                    alt={dept.name}
                    className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute top-3 left-3 px-2 py-0.5 rounded-full bg-white/95 dark:bg-slate-900/95 backdrop-blur-md text-[10px] font-bold text-[#1E3A8A] dark:text-sky-300 border border-white/40 shadow-xs">
                    {dept.badge}
                  </div>
                </div>
                <div className="p-5 flex flex-col justify-between flex-1 space-y-3">
                  <div>
                    <span className="text-[11px] font-bold text-[#0284C7] dark:text-sky-400 uppercase tracking-wider">
                      {dept.doctors}
                    </span>
                    <h3 className="text-lg font-bold text-[#0F172A] dark:text-white mt-1 mb-1.5">
                      {dept.name}
                    </h3>
                    <p className="text-xs text-[#64748B] dark:text-slate-300 leading-relaxed">
                      {dept.description}
                    </p>
                  </div>
                  <div className="pt-2 border-t border-slate-100 dark:border-slate-800">
                    <Link
                      to="/appointments"
                      className="inline-flex items-center gap-1 text-xs font-bold text-[#2563EB] dark:text-sky-400 group-hover:translate-x-1 transition-transform"
                    >
                      <span>Consult Specialist</span>
                      <ChevronRight className="h-3.5 w-3.5" />
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* =========================================================================
            5. CLINICAL WORKFLOW / HOW IT WORKS
        ========================================================================= */}
        <section id="workflow" className="py-20 px-4 sm:px-8 max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-14 space-y-3">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-[#0F172A] dark:text-white tracking-tight">
              A Seamless <span className="text-[#2563EB] dark:text-sky-400">Patient Journey</span>
            </h2>
            <p className="text-base text-[#64748B] dark:text-slate-300">
              Eliminates administrative bottlenecks and guarantees diagnostic continuity.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {workflowSteps.map((step, idx) => {
              const Icon = step.icon;
              return (
                <div
                  key={idx}
                  className="aurora-card rounded-3xl p-6 relative space-y-3.5 hover:scale-[1.02] transition-transform bg-white/95 dark:bg-slate-900/95"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xl font-black text-[#2563EB]/40 dark:text-sky-400/40 font-mono">
                      {step.step}
                    </span>
                    <div className="w-9 h-9 rounded-2xl bg-blue-50 dark:bg-blue-950/60 flex items-center justify-center text-[#2563EB] dark:text-sky-300">
                      <Icon className="h-4.5 w-4.5" />
                    </div>
                  </div>
                  <h4 className="text-base font-bold text-[#0F172A] dark:text-white">
                    {step.title}
                  </h4>
                  <p className="text-xs text-[#64748B] dark:text-slate-300 leading-relaxed">
                    {step.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </section>

        {/* =========================================================================
            6. 24/7 EMERGENCY & CRITICAL HOTLINE BANNER
        ========================================================================= */}
        <section id="emergency" className="py-14 px-4 sm:px-8 max-w-7xl mx-auto">
          <div className="rounded-[2.5rem] bg-gradient-to-r from-[#1E3A8A] via-[#1E40AF] to-[#2563EB] text-white p-8 sm:p-12 shadow-xl relative overflow-hidden">
            <div className="relative z-10 grid lg:grid-cols-12 gap-8 items-center">
              <div className="lg:col-span-8 space-y-4">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/20 text-rose-200 border border-rose-400/30 text-xs font-bold uppercase tracking-wider">
                  <AlertTriangle className="h-3.5 w-3.5 text-rose-300" />
                  Immediate Medical Attention
                </div>
                <h3 className="text-3xl sm:text-4xl font-black tracking-tight text-white leading-tight">
                  24/7 Level 1 Emergency & Trauma Care
                </h3>
                <p className="text-sm sm:text-base text-blue-100/90 max-w-2xl leading-relaxed">
                  Severe chest pain, respiratory distress, stroke signs, or acute injury? Call emergency services immediately. Our rapid ambulance dispatch and emergency team operate 24/7.
                </p>
                <div className="flex flex-wrap items-center gap-3.5 pt-2">
                  <a
                    href="tel:108"
                    className="inline-flex items-center gap-2 px-6 py-3 rounded-2xl font-black text-rose-600 bg-white shadow-lg hover:bg-slate-50 transition-all hover:scale-105 text-sm"
                  >
                    <Phone className="h-4 w-4 text-rose-600 animate-bounce" />
                    <span>Emergency Hotline: 108 / 112</span>
                  </a>
                  <a
                    href="/ai-assistant"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-5 py-3 rounded-2xl font-bold text-white bg-white/10 hover:bg-white/20 border border-white/20 backdrop-blur-md transition-all text-sm"
                  >
                    <Sparkles className="h-4 w-4" />
                    <span>Emergency Screening AI</span>
                    <ExternalLink className="h-3.5 w-3.5" />
                  </a>
                </div>
              </div>

              <div className="lg:col-span-4 flex flex-col items-start lg:items-end space-y-3 text-sm text-blue-100">
                <div className="p-3.5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 w-full space-y-1">
                  <span className="text-[11px] font-bold uppercase text-sky-200">Hospital Address:</span>
                  <p className="font-semibold text-white text-xs sm:text-sm">123 Health Avenue, Medical District</p>
                  <p className="text-[11px] text-blue-200">Main Emergency Gate 1 • Rapid Ambulance Bay</p>
                </div>
                <div className="p-3.5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 w-full space-y-1">
                  <span className="text-[11px] font-bold uppercase text-sky-200">General Enquiries:</span>
                  <p className="font-semibold text-white text-xs sm:text-sm">1-800-VELORA-CARE</p>
                  <p className="text-[11px] text-blue-200">support@veloracare.com</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* =========================================================================
            7. FREQUENTLY ASKED QUESTIONS (INTERACTIVE ACCORDION)
        ========================================================================= */}
        <section id="faq" className="py-20 px-4 sm:px-8 max-w-4xl mx-auto">
          <div className="text-center mb-12 space-y-2.5">
            <h2 className="text-3xl sm:text-4xl font-black text-[#0F172A] dark:text-white tracking-tight">
              Frequently Asked <span className="text-[#2563EB] dark:text-sky-400">Questions</span>
            </h2>
            <p className="text-sm sm:text-base text-[#64748B] dark:text-slate-300">
              Clear answers regarding clinical workflows, AI safety guardrails, and patient records.
            </p>
          </div>

          <div className="space-y-3">
            {faqs.map((faq, idx) => {
              const isOpen = activeFaq === idx;
              return (
                <div
                  key={idx}
                  className="aurora-card rounded-2xl border border-[#D9E2F0] dark:border-slate-800 overflow-hidden transition-all bg-white dark:bg-slate-900"
                >
                  <button
                    onClick={() => setActiveFaq(isOpen ? null : idx)}
                    className="w-full flex items-center justify-between p-5 text-left text-sm sm:text-base font-bold text-[#0F172A] dark:text-white focus:outline-none"
                  >
                    <span>{faq.q}</span>
                    <ChevronDown
                      className={`h-4.5 w-4.5 text-[#2563EB] shrink-0 transition-transform duration-300 ${
                        isOpen ? 'rotate-180' : ''
                      }`}
                    />
                  </button>
                  <AnimatePresence>
                    {isOpen && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        className="px-5 pb-5 text-xs sm:text-sm text-[#475569] dark:text-slate-300 leading-relaxed border-t border-slate-100 dark:border-slate-800 pt-3"
                      >
                        {faq.a}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              );
            })}
          </div>
        </section>

        {/* =========================================================================
            8. FOOTER
        ========================================================================= */}
        <footer className="border-t border-[#D9E2F0]/80 dark:border-slate-800 bg-white dark:bg-slate-950 py-12 px-4 sm:px-8">
          <div className="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8 mb-10">
            <div className="col-span-2 space-y-3.5">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-[#2563EB] to-[#1E3A8A] flex items-center justify-center text-white">
                  <HeartPulse className="h-4.5 w-4.5" />
                </div>
                <span className="text-xl font-black bg-gradient-to-r from-[#1E3A8A] via-[#2563EB] to-[#0284C7] dark:from-white dark:to-sky-300 bg-clip-text text-transparent">
                  Velora Care
                </span>
              </div>
              <p className="text-xs sm:text-sm text-[#64748B] dark:text-slate-400 max-w-sm leading-relaxed">
                Hospital Management Operating System & Grounded Clinical AI Assistant. Delivering modern, reliable healthcare infrastructure.
              </p>
              <div className="text-xs text-[#64748B] dark:text-slate-400">
                Emergency Hotline: <strong>108 / 112</strong>
              </div>
            </div>

            <div className="space-y-2.5">
              <h5 className="text-xs font-bold uppercase tracking-wider text-[#1E3A8A] dark:text-sky-300">Ecosystem</h5>
              <ul className="space-y-2 text-xs font-medium text-[#475569] dark:text-slate-400">
                <li><a href="/ai-assistant" target="_blank" rel="noopener noreferrer" className="hover:text-[#2563EB]">AI Health Assistant</a></li>
                <li><Link to="/appointments" className="hover:text-[#2563EB]">Appointments</Link></li>
                <li><Link to="/beds" className="hover:text-[#2563EB]">Bed Management</Link></li>
                <li><Link to="/lab-requests" className="hover:text-[#2563EB]">Laboratory LIMS</Link></li>
                <li><Link to="/billing" className="hover:text-[#2563EB]">Inpatient Billing</Link></li>
              </ul>
            </div>

            <div className="space-y-2.5">
              <h5 className="text-xs font-bold uppercase tracking-wider text-[#1E3A8A] dark:text-sky-300">Specialties</h5>
              <ul className="space-y-2 text-xs font-medium text-[#475569] dark:text-slate-400">
                <li><Link to="/departments" className="hover:text-[#2563EB]">Cardiology</Link></li>
                <li><Link to="/departments" className="hover:text-[#2563EB]">Neurology</Link></li>
                <li><Link to="/departments" className="hover:text-[#2563EB]">Pediatrics</Link></li>
                <li><Link to="/departments" className="hover:text-[#2563EB]">Orthopedics</Link></li>
              </ul>
            </div>

            <div className="space-y-2.5">
              <h5 className="text-xs font-bold uppercase tracking-wider text-[#1E3A8A] dark:text-sky-300">Portals</h5>
              <ul className="space-y-2 text-xs font-medium text-[#475569] dark:text-slate-400">
                <li><Link to="/login" className="hover:text-[#2563EB]">Staff Login</Link></li>
                <li><Link to="/register" className="hover:text-[#2563EB]">Patient Portal</Link></li>
                <li><Link to="/profile" className="hover:text-[#2563EB]">Health Record</Link></li>
              </ul>
            </div>
          </div>

          <div className="max-w-7xl mx-auto pt-6 border-t border-[#D9E2F0]/60 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-[#64748B] dark:text-slate-400">
            <div>
              © {new Date().getFullYear()} Velora Care Hospital Management System. All rights reserved.
            </div>
            <div className="flex gap-5 text-slate-400">
              <span>HIPAA Compliant</span>
              <span>CDSCO & DailyMed Grounded</span>
              <span>ISO 27001 Security</span>
            </div>
          </div>
        </footer>
      </main>

      {/* Global CSS for animated EKG scroll */}
      <style>{`
        @keyframes ekg-scroll {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-ekg-scroll {
          animation: ekg-scroll 24s linear infinite;
        }
        .no-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .no-scrollbar {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
      `}</style>
    </div>
  );
}
