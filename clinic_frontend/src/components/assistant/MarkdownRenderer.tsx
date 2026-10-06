import React from 'react';
import ReactMarkdown from 'react-markdown';

interface MarkdownRendererProps {
  content: string;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  // Replace double equal signs ==highlight== with bold or clean format if any LLM output contains it
  const cleanContent = content.replace(/==(.*?)==/g, '**$1**');

  return (
    <div className="prose prose-slate dark:prose-invert max-w-none text-[#334155] dark:text-slate-200 leading-relaxed text-sm sm:text-[15px]">
      <ReactMarkdown
        components={{
          h1: ({ node, ...props }) => (
            <h1 className="text-lg sm:text-xl font-bold text-[#1E3A8A] dark:text-white mt-4 mb-2 flex items-center gap-2" {...props} />
          ),
          h2: ({ node, ...props }) => (
            <h2 className="text-base sm:text-lg font-bold text-[#1E3A8A] dark:text-white mt-4 mb-2 pb-1.5 border-b border-[#D9E2F0] dark:border-slate-800 flex items-center gap-2" {...props} />
          ),
          h3: ({ node, ...props }) => (
            <h3 className="text-sm sm:text-base font-bold text-[#1E3A8A] dark:text-sky-200 mt-3 mb-1.5 flex items-center gap-1.5" {...props} />
          ),
          p: ({ node, ...props }) => (
            <p className="mb-2.5 last:mb-0 leading-relaxed text-[#334155] dark:text-slate-200 font-normal" {...props} />
          ),
          strong: ({ node, ...props }) => (
            <strong className="font-bold text-[#1E3A8A] dark:text-white" {...props} />
          ),
          ul: ({ node, ...props }) => (
            <ul className="my-2.5 ml-4 space-y-1.5 list-disc list-outside text-[#334155] dark:text-slate-200" {...props} />
          ),
          ol: ({ node, ...props }) => (
            <ol className="my-2.5 ml-4 space-y-1.5 list-decimal list-outside text-[#334155] dark:text-slate-200" {...props} />
          ),
          li: ({ node, ...props }) => (
            <li className="pl-1 leading-relaxed text-[#334155] dark:text-slate-200" {...props} />
          ),
          blockquote: ({ node, ...props }) => (
            <blockquote className="my-3 border-l-4 border-[#2563EB] pl-3.5 italic text-[#1E3A8A] dark:text-blue-200 bg-[#EFF6FF]/70 dark:bg-blue-950/30 py-1.5 rounded-r-xl" {...props} />
          ),
          code: ({ node, ...props }) => (
            <code className="bg-[#F1F5F9] dark:bg-slate-800 px-1.5 py-0.5 rounded text-xs font-mono text-[#2563EB] dark:text-sky-300 font-semibold" {...props} />
          ),
          hr: () => (
            <hr className="my-4 border-[#D9E2F0] dark:border-slate-800" />
          ),
        }}
      >
        {cleanContent}
      </ReactMarkdown>
    </div>
  );
};
