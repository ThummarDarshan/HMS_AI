import React, { useState } from 'react';
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';
import { Sparkles, HeartPulse, Activity } from 'lucide-react';

interface Chatbot3DAvatarProps {
  onInteract?: () => void;
  className?: string;
}

const GREETINGS = [
  "Hello Kishan! I'm your AI Health Assistant. Ask me about symptoms, medications, or hospital care!",
  "Always here to help with 24/7 clinical guidance & first aid protocols!",
  "Need to check a medication or book an appointment? Type your question below!",
  "Equipped with Velora Clinical AI to analyze health queries securely.",
];

/**
 * Unique, ultra-professional 3D Animated Healthcare Bot Avatar.
 * Features:
 * - Interactive 3D Perspective Tilt following mouse movement
 * - Continuous idle levitation (floating) with dynamic 3D ground shadow
 * - Two rotating 3D holographic orbital rings with gradient nodes
 * - On Click: 3D 360-degree spin + holographic shockwave + interactive greeting speech bubble!
 */
export const Chatbot3DAvatar: React.FC<Chatbot3DAvatarProps> = ({
  onInteract,
  className = '',
}) => {
  const [isSpinning, setIsSpinning] = useState(false);
  const [greetingIndex, setGreetingIndex] = useState(0);
  const [showBubble, setShowBubble] = useState(true);

  // Mouse tilt tracking
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const rotateX = useSpring(useTransform(mouseY, [-60, 60], [14, -14]), {
    stiffness: 150,
    damping: 18,
  });
  const rotateY = useSpring(useTransform(mouseX, [-60, 60], [-16, 16]), {
    stiffness: 150,
    damping: 18,
  });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    mouseX.set(e.clientX - centerX);
    mouseY.set(e.clientY - centerY);
  };

  const handleMouseLeave = () => {
    mouseX.set(0);
    mouseY.set(0);
  };

  const handleClick = () => {
    if (isSpinning) return;
    setIsSpinning(true);
    setGreetingIndex((prev) => (prev + 1) % GREETINGS.length);
    setShowBubble(true);
    onInteract?.();
    setTimeout(() => {
      setIsSpinning(false);
    }, 1000);
  };

  return (
    <div
      className={`relative flex flex-col items-center justify-center select-none ${className}`}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
      {/* Interactive Speech Bubble Tooltip above the 3D Bot */}
      {showBubble && (
        <motion.div
          initial={{ opacity: 0, y: 10, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.3 }}
          className="relative mb-3 max-w-xs sm:max-w-sm px-3.5 py-1.5 rounded-2xl bg-card/95 border border-primary/30 shadow-lg shadow-primary/10 backdrop-blur-md text-center z-20 cursor-pointer"
          onClick={() => setGreetingIndex((prev) => (prev + 1) % GREETINGS.length)}
          title="Click bot or bubble for tips"
        >
          <div className="flex items-center justify-center gap-1.5 text-xs font-semibold text-primary">
            <Sparkles className="h-3 w-3 animate-spin-slow" />
            <span className="text-[11px] text-foreground font-medium">
              {GREETINGS[greetingIndex]}
            </span>
          </div>
          {/* Speech bubble pointer arrow */}
          <div className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-3 h-3 bg-card border-r border-b border-primary/30 rotate-45" />
        </motion.div>
      )}

      {/* Main 3D Floating Stage with Perspective */}
      <div
        className="relative w-28 h-28 sm:w-32 sm:h-32 flex items-center justify-center cursor-pointer group"
        style={{ perspective: 1000 }}
        onClick={handleClick}
        title="Click to interact with 3D AI Assistant!"
      >
        {/* Holographic Shockwave Ripple on Click */}
        {isSpinning && (
          <motion.div
            initial={{ scale: 0.8, opacity: 0.9 }}
            animate={{ scale: 2.2, opacity: 0 }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
            className="absolute w-28 h-28 rounded-full border-2 border-cyan-400 bg-cyan-400/20 pointer-events-none"
          />
        )}

        {/* 3D Orbital Ring 1: Cyan/Blue Energy Orbit */}
        <motion.div
          animate={{ rotateZ: 360 }}
          transition={{ duration: 12, repeat: Infinity, ease: 'linear' }}
          className="absolute w-32 h-32 sm:w-36 sm:h-36 rounded-full border border-cyan-400/35 border-dashed pointer-events-none"
          style={{ transform: 'rotateX(70deg)' }}
        >
          {/* Orbiting Satellite Light Node */}
          <span className="absolute top-0 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_8px_#22d3ee]" />
        </motion.div>

        {/* 3D Orbital Ring 2: Emerald/Cyan Counter-Orbit */}
        <motion.div
          animate={{ rotateZ: -360 }}
          transition={{ duration: 16, repeat: Infinity, ease: 'linear' }}
          className="absolute w-28 h-28 sm:w-32 sm:h-32 rounded-full border border-primary/30 pointer-events-none"
          style={{ transform: 'rotateX(-65deg) rotateY(20deg)' }}
        >
          <span className="absolute bottom-0 left-1/2 -translate-x-1/2 w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399]" />
        </motion.div>

        {/* Entrance motion wrapper on initial open */}
        <motion.div
          initial={{ scale: 0.2, rotateY: -180, opacity: 0 }}
          animate={{ scale: 1, rotateY: 0, opacity: 1 }}
          transition={{ type: 'spring', damping: 14, stiffness: 120, duration: 0.8 }}
          className="relative w-20 h-20 sm:w-24 sm:h-24 flex items-center justify-center"
        >
          {/* Levitating 3D Bot Avatar Container */}
          <motion.div
            animate={{
              y: [0, -10, 0],
              rotateZ: [-1, 1, -1],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: 'easeInOut',
            }}
            style={{
              rotateX,
              rotateY,
              transformStyle: 'preserve-3d',
            }}
            className="w-full h-full relative flex items-center justify-center"
          >
            {/* Inner 3D Spin Animation on Click */}
            <motion.div
              animate={
                isSpinning
                  ? {
                      rotateY: [0, 360],
                      scale: [1, 1.18, 1],
                    }
                  : {}
              }
              transition={{ duration: 0.85, ease: 'easeInOut' }}
              className="w-full h-full relative flex items-center justify-center filter drop-shadow-[0_12px_24px_rgba(37,99,235,0.35)]"
            >
              {/* SVG Vector 3D Robot Doctor Character */}
              <svg
                viewBox="0 0 64 64"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="w-full h-full select-none"
              >
                <defs>
                  {/* 3D Sphere Spherical Gradient */}
                  <radialGradient id="botSphere3D" cx="35%" cy="30%" r="70%">
                    <stop offset="0%" stopColor="#60A5FA" />
                    <stop offset="45%" stopColor="#2563EB" />
                    <stop offset="85%" stopColor="#1E3A8A" />
                    <stop offset="100%" stopColor="#0F172A" />
                  </radialGradient>

                  {/* 3D Ceramic Head Highlight */}
                  <linearGradient id="headCeramic3D" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#FFFFFF" />
                    <stop offset="70%" stopColor="#F1F5F9" />
                    <stop offset="100%" stopColor="#CBD5E1" />
                  </linearGradient>

                  {/* Glowing Cyan Visor */}
                  <linearGradient id="eyeGlow3D" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#38BDF8" />
                    <stop offset="100%" stopColor="#22D3EE" />
                  </linearGradient>

                  <filter id="soft3DShadow" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="2" stdDeviation="2" floodColor="#0F172A" floodOpacity="0.3" />
                  </filter>
                </defs>

                {/* 3D Outer Sphere Body / Halo */}
                <circle cx="32" cy="32" r="30" fill="url(#botSphere3D)" />

                {/* Glass Rim Shimmer */}
                <circle cx="32" cy="32" r="29" stroke="white" strokeWidth="1.5" strokeOpacity="0.3" />

                {/* Top Spherical Ambient Light Dome */}
                <ellipse cx="32" cy="16" rx="18" ry="9" fill="white" fillOpacity="0.16" />

                {/* Antenna with 3D Light Sensor */}
                <line x1="32" y1="16" x2="32" y2="10" stroke="#93C5FD" strokeWidth="2.2" strokeLinecap="round" />
                <circle cx="32" cy="9" r="3.2" fill="#38BDF8" filter="url(#soft3DShadow)" />
                <circle cx="32" cy="9" r="1.4" fill="#FFFFFF" />

                {/* Stethoscope Headset Arch */}
                <path
                  d="M 14 30 C 14 16 50 16 50 30"
                  fill="none"
                  stroke="#60A5FA"
                  strokeWidth="2.4"
                  strokeLinecap="round"
                  opacity="0.8"
                />

                {/* Ear Headset Metallic Nodes */}
                <rect x="10.5" y="26" width="5" height="11" rx="2.5" fill="#38BDF8" filter="url(#soft3DShadow)" />
                <rect x="48.5" y="26" width="5" height="11" rx="2.5" fill="#38BDF8" filter="url(#soft3DShadow)" />

                {/* Ceramic Robot Head with 3D Depth */}
                <g filter="url(#soft3DShadow)">
                  <rect x="15" y="16" width="34" height="28" rx="13" fill="url(#headCeramic3D)" />
                </g>

                {/* Medical Doctor Cross on Forehead */}
                <g transform="translate(32, 20)">
                  <rect x="-1.5" y="-3.5" width="3" height="7" rx="1" fill="#2563EB" />
                  <rect x="-3.5" y="-1.5" width="7" height="3" rx="1" fill="#2563EB" />
                </g>

                {/* Dark Visor Curved Glass Screen */}
                <rect x="18" y="25" width="28" height="14" rx="7" fill="#0F172A" />

                {/* Visor 3D Light Glare curve */}
                <path
                  d="M 21 28 Q 32 25 43 28"
                  stroke="#38BDF8"
                  strokeWidth="1.2"
                  opacity="0.35"
                  strokeLinecap="round"
                />

                {/* Expressive Glowing Curved AI Eyes */}
                <rect x="22.5" y="29.5" width="4.5" height="6" rx="2.25" fill="url(#eyeGlow3D)" />
                <circle cx="23.8" cy="31" r="1" fill="#FFFFFF" />

                <rect x="37" y="29.5" width="4.5" height="6" rx="2.25" fill="url(#eyeGlow3D)" />
                <circle cx="38.3" cy="31" r="1" fill="#FFFFFF" />

                {/* Stethoscope Tubing draped in front */}
                <path
                  d="M 21 44 C 21 51 27 55 32 55 C 37 55 43 51 43 44"
                  fill="none"
                  stroke="#FFFFFF"
                  strokeWidth="2.4"
                  strokeLinecap="round"
                />
                {/* Stethoscope Metallic Chest Bell with Cyan Core */}
                <circle cx="32" cy="55" r="3.2" fill="#38BDF8" stroke="#FFFFFF" strokeWidth="1.5" />
              </svg>

              {/* Glowing Online Pulse Node anchored at bottom-right */}
              <span className="absolute bottom-0.5 right-0.5 w-3.5 h-3.5 rounded-full bg-emerald-500 ring-2 ring-background z-10 shadow-[0_0_8px_#10b981]" />
            </motion.div>
          </motion.div>
        </motion.div>

        {/* Dynamic 3D Floor Shadow that expands/contracts with floating */}
        <motion.div
          animate={{
            scale: [1, 0.8, 1],
            opacity: [0.35, 0.18, 0.35],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
          className="absolute -bottom-2 w-20 sm:w-24 h-4 rounded-full bg-primary/30 blur-sm pointer-events-none"
        />
      </div>

      {/* Interactive Micro Label below */}
      <div className="mt-3 flex items-center gap-1.5 text-[11px] font-medium text-muted-foreground group-hover:text-primary transition-colors cursor-pointer" onClick={handleClick}>
        <Activity className="h-3 w-3 text-primary animate-pulse" />
        <span>Click for 3D Interaction & Advice</span>
      </div>
    </div>
  );
};
