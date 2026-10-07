import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Sparkles,
  Lock,
  Stethoscope,
  Pill,
  ShieldCheck,
  ArrowRight,
  Activity,
} from 'lucide-react';
import { Chatbot3DCanvas } from './Chatbot3DCanvas';

interface Chatbot3DLoadingScreenProps {
  onComplete: () => void;
  patientName?: string;
}

const LOADING_PHASES = [
  {
    min: 0,
    max: 28,
    text: 'Calibrating multi-turn symptom triage engine...',
    icon: Stethoscope,
  },
  {
    min: 28,
    max: 62,
    text: 'Connecting CDSCO verified pharmacology database...',
    icon: Pill,
  },
  {
    min: 62,
    max: 90,
    text: 'Arming red-flag emergency screening & safety grid...',
    icon: ShieldCheck,
  },
  {
    min: 90,
    max: 100,
    text: 'Velora Clinical AI ready • Entering consultation...',
    icon: Sparkles,
  },
];

export const Chatbot3DLoadingScreen: React.FC<Chatbot3DLoadingScreenProps> = ({
  onComplete,
  patientName = 'Patient',
}) => {
  const [progress, setProgress] = useState(0);
  const [isFinishing, setIsFinishing] = useState(false);

  // Smooth loading progression over ~2.4 seconds
  useEffect(() => {
    const startTime = Date.now();
    const duration = 2400;

    const interval = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const rawProgress = Math.min(100, Math.round((elapsed / duration) * 100));
      setProgress(rawProgress);

      if (rawProgress >= 100) {
        clearInterval(interval);
        setTimeout(() => {
          setIsFinishing(true);
          setTimeout(() => {
            onComplete();
          }, 400);
        }, 250);
      }
    }, 25);

    return () => clearInterval(interval);
  }, [onComplete]);

  // Current active loading phase
  const currentPhase =
    LOADING_PHASES.find((p) => progress >= p.min && progress <= p.max) ||
    LOADING_PHASES[0];
  const PhaseIcon = currentPhase.icon;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: isFinishing ? 0 : 1, scale: isFinishing ? 1.02 : 1 }}
        exit={{ opacity: 0, scale: 1.04 }}
        transition={{ duration: 0.4, ease: 'easeInOut' }}
        className="relative flex flex-col items-center justify-between min-h-[calc(100vh-6.8rem)] w-full rounded-2xl sm:rounded-3xl border border-border/80 bg-gradient-to-b from-card/90 via-card/80 to-background/90 backdrop-blur-2xl shadow-xl overflow-hidden select-none p-4 sm:p-6"
      >
        {/* Soft, Clean Ambient Glow Background */}
        <div className="absolute top-1/4 left-1/3 w-80 h-80 rounded-full bg-cyan-500/10 blur-[100px] pointer-events-none" />
        <div className="absolute bottom-1/4 right-1/3 w-80 h-80 rounded-full bg-primary/10 blur-[110px] pointer-events-none" />

        {/* ================= Top Bar: Clean & Balanced ================= */}
        <div className="relative z-10 w-full flex items-center justify-between px-2 sm:px-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-xs font-semibold text-primary backdrop-blur-md shadow-xs">
            <Sparkles className="w-3.5 h-3.5 text-cyan-500 animate-spin-slow" />
            <span>Velora Clinical AI</span>
          </div>

          <div className="flex items-center gap-2 text-xs text-muted-foreground font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="font-semibold text-emerald-600 dark:text-emerald-400">Online</span>
            <span className="text-border">•</span>
            <span className="inline-flex items-center gap-1">
              <Lock className="w-3 h-3 text-cyan-500" />
              <span>Private Session</span>
            </span>
          </div>
        </div>

        {/* ================= Center: 3D Robot & Friendly Bubble ================= */}
        <div className="relative flex-1 flex flex-col items-center justify-center my-1 sm:my-2">
          {/* Friendly Floating Greeting Speech Bubble */}
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35 }}
            className="relative mb-2 px-3.5 py-1.5 rounded-2xl bg-card/95 border border-primary/25 shadow-md shadow-primary/5 backdrop-blur-md text-center z-10"
          >
            <div className="flex items-center gap-1.5 text-xs font-medium text-foreground">
              <span className="text-primary font-semibold">Hello {patientName}!</span>
              <span className="text-muted-foreground">Preparing your consultation...</span>
            </div>
            {/* Bubble pointer tail */}
            <div className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-2 h-2 bg-card border-r border-b border-primary/25 rotate-45" />
          </motion.div>

          {/* 3D Medical Robot Canvas (Properly Sized & Prominent) */}
          <div className="relative w-72 h-64 sm:w-80 sm:h-72 flex items-center justify-center">
            <Chatbot3DCanvas progress={progress} className="w-full h-full" />
          </div>
        </div>

        {/* ================= Bottom: Structured Title, Progress & Features ================= */}
        <div className="relative z-10 w-full max-w-md text-center space-y-3 px-2 pb-1">
          {/* Main Title & Subtitle */}
          <div>
            <h3 className="text-base sm:text-lg font-bold text-foreground tracking-tight">
              AI Health & Clinical Assistant
            </h3>
            <p className="text-xs text-muted-foreground mt-0.5 max-w-sm mx-auto">
              Your 24/7 companion for symptom assessment, verified medication monographs & protocols
            </p>
          </div>

          {/* Dynamic Progress Bar with Phase Details */}
          <div className="w-full space-y-1.5">
            <div className="flex items-center justify-between text-xs px-0.5 font-medium">
              <span className="text-cyan-600 dark:text-cyan-400 flex items-center gap-1.5 truncate">
                <PhaseIcon className="w-3.5 h-3.5 flex-shrink-0 animate-pulse text-cyan-500" />
                <span className="truncate">{currentPhase.text}</span>
              </span>
              <span className="font-mono text-foreground font-bold ml-2">{progress}%</span>
            </div>

            <div className="relative w-full h-2 rounded-full bg-muted/80 overflow-hidden p-0.5 border border-border/70 shadow-inner">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-cyan-500 via-primary to-emerald-400 shadow-sm"
                style={{ width: `${progress}%` }}
                transition={{ ease: 'linear' }}
              />
            </div>
          </div>

          {/* Three Clean Feature Pills (Proper Medium, Professional) */}
          <div className="flex items-center justify-center gap-2 pt-0.5 flex-wrap">
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-card/80 border border-border/70 text-[11px] font-medium text-muted-foreground">
              <Stethoscope className="w-3 h-3 text-cyan-500" />
              <span>Multi-Turn Triage</span>
            </span>
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-card/80 border border-border/70 text-[11px] font-medium text-muted-foreground">
              <Pill className="w-3 h-3 text-emerald-500" />
              <span>CDSCO Verified</span>
            </span>
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-card/80 border border-border/70 text-[11px] font-medium text-muted-foreground">
              <ShieldCheck className="w-3 h-3 text-primary" />
              <span>100% Confidential</span>
            </span>
          </div>

          {/* Subtle Quick Skip Button */}
          <div className="pt-1">
            <button
              onClick={onComplete}
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-semibold text-muted-foreground hover:text-foreground hover:bg-muted/70 transition-all active:scale-95 group"
            >
              <span>Enter Consultation</span>
              <ArrowRight className="w-3 h-3 transition-transform group-hover:translate-x-0.5" />
            </button>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};
