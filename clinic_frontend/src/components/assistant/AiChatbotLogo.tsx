import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface AiChatbotLogoProps {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  showStatus?: boolean;
  statusColor?: string;
  interactive?: boolean;
}

const SIZE_MAP = {
  xs: { box: 'w-6 h-6', dot: 'w-2 h-2' },
  sm: { box: 'w-8 h-8', dot: 'w-2.5 h-2.5' },
  md: { box: 'w-10 h-10', dot: 'w-3 h-3' },
  lg: { box: 'w-12 h-12', dot: 'w-3.5 h-3.5' },
  xl: { box: 'w-16 h-16', dot: 'w-4 h-4' },
};

/**
 * Dedicated Professional Medical AI Chatbot Logo with subtle 3D interactive animation.
 */
export const AiChatbotLogo: React.FC<AiChatbotLogoProps> = ({
  size = 'md',
  className = '',
  showStatus = false,
  statusColor = 'bg-emerald-500',
  interactive = true,
}) => {
  const current = SIZE_MAP[size] || SIZE_MAP.md;
  const [isSpinning, setIsSpinning] = useState(false);

  const handleClick = () => {
    if (!interactive || isSpinning) return;
    setIsSpinning(true);
    setTimeout(() => setIsSpinning(false), 800);
  };

  return (
    <motion.div
      onClick={handleClick}
      whileHover={interactive ? { scale: 1.08, rotateY: 15 } : {}}
      animate={isSpinning ? { rotateY: 360, scale: [1, 1.15, 1] } : {}}
      transition={{ duration: 0.7, ease: 'easeInOut' }}
      style={{ perspective: 600, transformStyle: 'preserve-3d' }}
      className={`relative inline-flex items-center justify-center flex-shrink-0 select-none ${current.box} ${className} ${interactive ? 'cursor-pointer' : ''}`}
      title={interactive ? 'AI Health Assistant - Click for 3D spin!' : undefined}
    >
      <svg
        viewBox="0 0 48 48"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full drop-shadow-md"
      >
        <defs>
          {/* Base Background: Deep Medical Navy to Royal Blue to Cyan */}
          <linearGradient id="hmsAvatarBg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#1E3A8A" />
            <stop offset="55%" stopColor="#2563EB" />
            <stop offset="100%" stopColor="#0284C7" />
          </linearGradient>

          {/* Cyan Glow Gradient for Visor & Nodes */}
          <linearGradient id="cyanGlow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#38BDF8" />
            <stop offset="100%" stopColor="#22D3EE" />
          </linearGradient>

          {/* Ceramic White Shading */}
          <linearGradient id="ceramicHead" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#FFFFFF" />
            <stop offset="100%" stopColor="#E2E8F0" />
          </linearGradient>

          {/* Soft Drop Shadow for the Head */}
          <filter id="headShadow" x="-15%" y="-15%" width="130%" height="130%">
            <feDropShadow dx="0" dy="1.5" stdDeviation="1.5" floodColor="#0F172A" floodOpacity="0.25" />
          </filter>
        </defs>

        {/* 1. Base Circular Avatar Container */}
        <circle cx="24" cy="24" r="22" fill="url(#hmsAvatarBg)" />

        {/* 2. Glass Rim Highlight */}
        <circle
          cx="24"
          cy="24"
          r="21.25"
          stroke="white"
          strokeOpacity="0.25"
          strokeWidth="1.2"
        />

        {/* 3. Top Ambient Light Flare */}
        <ellipse cx="24" cy="11" rx="14" ry="7" fill="white" opacity="0.12" />

        {/* ================= DEDICATED MEDICAL AI ROBOT LOGO ================= */}
        <g>
          {/* Top Antenna / AI Intelligence Sensor */}
          <line x1="24" y1="12" x2="24" y2="8" stroke="#93C5FD" strokeWidth="1.6" strokeLinecap="round" />
          <circle cx="24" cy="7" r="2.2" fill="#38BDF8" />
          <circle cx="24" cy="7" r="1" fill="#FFFFFF" />

          {/* Stethoscope Headset Band */}
          <path
            d="M 11 22 C 11 12 37 12 37 22"
            fill="none"
            stroke="#60A5FA"
            strokeWidth="1.6"
            strokeLinecap="round"
            opacity="0.7"
          />
          {/* Headset Audio Ear Nodes */}
          <rect x="8.5" y="19" width="3.5" height="7.5" rx="1.75" fill="#38BDF8" />
          <rect x="36" y="19" width="3.5" height="7.5" rx="1.75" fill="#38BDF8" />

          {/* Bot Ceramic White Head */}
          <g filter="url(#headShadow)">
            <rect x="11.5" y="12" width="25" height="21" rx="9" fill="url(#ceramicHead)" />
          </g>

          {/* Medical Cross on Forehead */}
          <g transform="translate(24, 15)">
            <rect x="-1" y="-2" width="2" height="4" rx="0.5" fill="#2563EB" />
            <rect x="-2" y="-1" width="4" height="2" rx="0.5" fill="#2563EB" />
          </g>

          {/* Dark Visor Screen */}
          <rect x="14" y="18" width="20" height="11" rx="5.5" fill="#0F172A" />

          {/* Visor Glass Reflection Curve */}
          <path
            d="M 16.5 20 Q 24 18 31.5 20"
            stroke="#38BDF8"
            strokeWidth="0.8"
            opacity="0.3"
            strokeLinecap="round"
          />

          {/* Expressive Glowing AI Curved Eyes */}
          <g>
            {/* Left Eye: Friendly Arced Pill */}
            <rect x="17.5" y="21.5" width="3.5" height="4.5" rx="1.75" fill="url(#cyanGlow)" />
            <circle cx="18.5" cy="22.5" r="0.75" fill="#FFFFFF" />

            {/* Right Eye: Friendly Arced Pill */}
            <rect x="27" y="21.5" width="3.5" height="4.5" rx="1.75" fill="url(#cyanGlow)" />
            <circle cx="28" cy="22.5" r="0.75" fill="#FFFFFF" />
          </g>

          {/* Stethoscope Tubing Drape around Neck */}
          <path
            d="M 16 33.5 C 16 38.5 20.5 41.5 24 41.5 C 27.5 41.5 32 38.5 32 33.5"
            fill="none"
            stroke="#FFFFFF"
            strokeWidth="1.8"
            strokeLinecap="round"
          />
          {/* Stethoscope Chest Piece Bell */}
          <circle cx="24" cy="41" r="2.2" fill="#38BDF8" stroke="#FFFFFF" strokeWidth="1" />
        </g>
      </svg>

      {/* Online Status Indicator (Cleanly anchored to bottom-right corner) */}
      {showStatus && (
        <span
          className={`absolute bottom-0 right-0 ${current.dot} rounded-full ${statusColor} ring-2 ring-card z-10`}
          title="Online"
        />
      )}
    </motion.div>
  );
};
