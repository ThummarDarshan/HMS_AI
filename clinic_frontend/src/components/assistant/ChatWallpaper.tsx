import React from 'react';

export type ChatBackgroundTheme =
  | 'clinical-doodle' // Exact match to User's 2nd Image
  | 'soft-pearl'      // Clean minimalist clinical pearl
  | 'teal-breeze'     // Soothing fresh health mint/teal
  | 'whatsapp-light'; // Authentic messaging slate

interface ChatWallpaperProps {
  theme?: ChatBackgroundTheme;
}

/**
 * Recreates the exact light-theme medical doodle wallpaper from the user's reference image:
 * Clean, spacious icons: Medical Cross, Heart, Stethoscope, Shield with checkmark,
 * Chat Bubble, Medicine Capsule, and decorative sparkles & micro-dots.
 */
export const ChatWallpaper: React.FC<ChatWallpaperProps> = ({
  theme = 'clinical-doodle',
}) => {
  return (
    <div
      className="absolute inset-0 pointer-events-none select-none overflow-hidden transition-colors duration-500"
      aria-hidden="true"
    >
      {/* 1. Base Gradient Layer based on selected theme */}
      {theme === 'clinical-doodle' && (
        /* Exact match to User Reference Image: soft clinical luminous light blue-gray */
        <div className="absolute inset-0 bg-gradient-to-b from-[#f0f4f9] via-[#edf3f8] to-[#e7eef6] dark:from-[#0b141a] dark:via-[#0f172a] dark:to-[#0b141a]" />
      )}

      {theme === 'soft-pearl' && (
        /* Clean minimalist pearl / light slate */
        <div className="absolute inset-0 bg-gradient-to-b from-[#f8fafc] via-[#f1f5f9] to-[#e2e8f0] dark:from-[#090d16] dark:via-[#0f172a] dark:to-[#090d16]" />
      )}

      {theme === 'teal-breeze' && (
        /* Soothing clinical cyan/teal light tint */
        <div className="absolute inset-0 bg-gradient-to-b from-[#f0fdfa] via-[#e6f7f6] to-[#ddf2f1] dark:from-[#041a1a] dark:via-[#0f2425] dark:to-[#041a1a]" />
      )}

      {theme === 'whatsapp-light' && (
        /* Classic messaging neutral light */
        <div className="absolute inset-0 bg-gradient-to-b from-[#efeae2] via-[#e5ddd5] to-[#dbd2c7] dark:from-[#0b141a] dark:via-[#111b21] dark:to-[#0b141a]" />
      )}

      {/* 2. Spacious Medical Doodle SVG Pattern (Precisely matching 2nd reference image) */}
      <svg
        className={`absolute inset-0 w-full h-full transition-opacity duration-300 ${
          theme === 'teal-breeze'
            ? 'opacity-[0.42] dark:opacity-[0.20] text-[#0d9488] dark:text-[#5eead4]'
            : 'opacity-[0.38] dark:opacity-[0.22] text-[#8fa7c2] dark:text-[#94a3b8]'
        }`}
        xmlns="http://www.w3.org/2000/svg"
        width="100%"
        height="100%"
      >
        <defs>
          <pattern
            id="clinical-doodle-pattern"
            width="240"
            height="180"
            patternUnits="userSpaceOnUse"
          >
            {/* ================= 1. Medical Cross (+) ================= */}
            <path
              d="M 22 18 h 6 v -6 h 6 v 6 h 6 v 6 h -6 v 6 h -6 v -6 h -6 z"
              fill="currentColor"
              opacity="0.8"
            />
            {/* Secondary Cross offset */}
            <path
              d="M 142 108 h 5 v -5 h 5 v 5 h 5 v 5 h -5 v 5 h -5 v -5 h -5 z"
              fill="currentColor"
              opacity="0.65"
            />

            {/* ================= 2. Medical Heart Outline ================= */}
            <path
              d="M 85 22 c -4 -5 -11 -5 -15 0 c -4 -5 -11 -5 -15 0 c -5 6 0 13 15 24 c 15 -11 20 -18 15 -24 z"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            {/* Secondary Heart */}
            <path
              d="M 205 112 c -3.5 -4 -9.5 -4 -13 0 c -3.5 -4 -9.5 -4 -13 0 c -4 5 0 11 13 20 c 13 -9 17 -15 13 -20 z"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.6"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            {/* ================= 3. Shield with Checkmark ================= */}
            <g transform="translate(145, 16)">
              <path
                d="M 14 0 C 14 0 9 2 0 2 C -9 2 -14 0 -14 0 C -14 11 -9 22 0 27 C 9 22 14 11 14 0 Z"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.7"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M -4 13 L -1 16 L 5 9"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </g>

            {/* ================= 4. Stethoscope ================= */}
            <g transform="translate(35, 95)">
              <path
                d="M 0 0 C 0 10 6 16 14 16 C 22 16 28 10 28 0"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
              />
              <path
                d="M 14 16 L 14 26 C 14 30 18 33 22 33 L 26 33"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
              />
              <circle cx="28" cy="33" r="3.5" fill="none" stroke="currentColor" strokeWidth="1.6" />
            </g>

            {/* ================= 5. Capsule / Medicine Pill (angled ~45°) ================= */}
            <g transform="translate(100, 105) rotate(-35)">
              <rect
                x="-14"
                y="-6"
                width="28"
                height="12"
                rx="6"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.8"
              />
              <line
                x1="0"
                y1="-6"
                x2="0"
                y2="6"
                stroke="currentColor"
                strokeWidth="1.6"
              />
            </g>

            {/* ================= 6. Speech / Chat Bubble ================= */}
            <path
              d="M 215 32 C 215 22 203 15 190 15 C 177 15 165 22 165 32 C 165 37 169 42 176 45 L 174 53 L 182 48 C 185 49 187 49 190 49 C 203 49 215 42 215 32 Z"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.7"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            {/* ================= 7. Four-Point Sparkle Stars (✦) ================= */}
            {/* Top middle sparkle */}
            <path
              d="M 112 18 L 114 23 L 119 25 L 114 27 L 112 32 L 110 27 L 105 25 L 110 23 Z"
              fill="currentColor"
              opacity="0.75"
            />
            {/* Bottom sparkle */}
            <path
              d="M 230 85 L 231.5 89 L 235.5 90.5 L 231.5 92 L 230 96 L 228.5 92 L 224.5 90.5 L 228.5 89 Z"
              fill="currentColor"
              opacity="0.7"
            />
            {/* Left accent sparkle */}
            <path
              d="M 18 80 L 19.5 83 L 22.5 84.5 L 19.5 86 L 18 89 L 16.5 86 L 13.5 84.5 L 16.5 83 Z"
              fill="currentColor"
              opacity="0.6"
            />

            {/* ================= 8. Three Dots Accent (...) ================= */}
            <g transform="translate(62, 70)" opacity="0.7">
              <circle cx="0" cy="0" r="1.6" fill="currentColor" />
              <circle cx="6" cy="0" r="1.6" fill="currentColor" />
              <circle cx="12" cy="0" r="1.6" fill="currentColor" />
            </g>
            <g transform="translate(165, 145)" opacity="0.65">
              <circle cx="0" cy="0" r="1.5" fill="currentColor" />
              <circle cx="5.5" cy="0" r="1.5" fill="currentColor" />
              <circle cx="11" cy="0" r="1.5" fill="currentColor" />
            </g>

            {/* ================= 9. Delicate Micro Accents ================= */}
            <circle cx="48" cy="18" r="1.2" fill="currentColor" opacity="0.6" />
            <circle cx="130" cy="55" r="1.3" fill="currentColor" opacity="0.5" />
            <circle cx="95" cy="155" r="1.2" fill="currentColor" opacity="0.5" />
            <circle cx="230" cy="150" r="1.3" fill="currentColor" opacity="0.6" />
          </pattern>
        </defs>

        <rect width="100%" height="100%" fill="url(#clinical-doodle-pattern)" />
      </svg>
    </div>
  );
};
