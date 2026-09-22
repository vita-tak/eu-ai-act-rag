"use client";

const SUGGESTIONS = [
  "What is a high-risk AI system?",
  "Classify my AI system's risk level",
  "What obligations apply to high-risk AI systems?",
] as const;

interface SuggestionChipsProps {
  onSelect: (text: string) => void;
  disabled: boolean;
}

export function SuggestionChips({ onSelect, disabled }: SuggestionChipsProps) {
  return (
    <section aria-labelledby="suggestions-heading" className="pb-10">
      <h2 id="suggestions-heading" className="text-[0.92rem] font-semibold text-[var(--ink-slate)]">
        Suggestions
      </h2>
      <ul className="mt-3 grid grid-cols-1 gap-[15px] sm:grid-cols-3">
        {SUGGESTIONS.map((suggestion) => (
          <li key={suggestion} className="flex">
            <button
              type="button"
              onClick={() => onSelect(suggestion)}
              disabled={disabled}
              className="w-full rounded-lg surface-ring border border-[var(--hairline)] bg-[var(--surface)] px-4 py-2.5 text-left text-[0.9375rem] leading-snug text-ink transition-colors hover:bg-[var(--surface-strong)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink disabled:opacity-50"
            >
              {suggestion}
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
